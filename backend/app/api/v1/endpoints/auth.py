import random
import string
import uuid
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.deps import get_db, get_current_user
from app.db.models.user import (
    User,
    CandidateProfile,
    OTPCode,
    PasswordResetToken,
    RefreshToken,
    LoginHistory,
)
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    GoogleLoginRequest,
    OTPVerifyRequest,
    OTPResendRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    RefreshTokenRequest,
    UserResponse,
    TokenResponse,
    MessageResponse,
)
from app.services.email import send_otp_email, send_password_reset_email

router = APIRouter()

def generate_numeric_otp(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))

def log_login_attempt(db: Session, email: str, request: Request, success: bool):
    try:
        ip = request.client.host if request.client else "127.0.0.1"
        history = LoginHistory(email=email, ip_address=ip, success=success)
        db.add(history)
        db.commit()
    except Exception:
        db.rollback()

@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new candidate account and send verification OTP email"""
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        if existing_user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email already exists."
            )
        # Update existing unverified user password
        existing_user.password_hash = get_password_hash(user_in.password)
        existing_user.full_name = user_in.full_name
        user = existing_user
    else:
        user = User(
            full_name=user_in.full_name,
            email=user_in.email.lower(),
            password_hash=get_password_hash(user_in.password),
            role="candidate",
            is_active=True,
            is_email_verified=False,
            auth_provider="local"
        )
        db.add(user)
        db.flush()
        # Initialize profile
        profile = CandidateProfile(user_id=user.id)
        db.add(profile)

    # Invalidate old OTPs for this email
    db.query(OTPCode).filter(OTPCode.email == user.email, OTPCode.used == False).update({"used": True})

    # Generate fresh OTP
    otp = generate_numeric_otp(6)
    otp_record = OTPCode(
        email=user.email,
        code_hash=get_password_hash(otp),
        purpose="register",
        expires_at=datetime.utcnow() + timedelta(minutes=15),
        used=False
    )
    db.add(otp_record)
    db.commit()

    # Dispatch email
    send_otp_email(to_email=user.email, otp_code=otp, purpose="Registration Verification")

    return MessageResponse(
        message="Registration successful. Please enter the 6-digit verification code sent to your email.",
        detail=f"OTP sent to {user.email}"
    )

@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(payload: OTPVerifyRequest, request: Request, db: Session = Depends(get_db)):
    """Verify email OTP code and return authentication JWT tokens"""
    email = payload.email.lower()
    otp_records = (
        db.query(OTPCode)
        .filter(OTPCode.email == email, OTPCode.used == False, OTPCode.purpose == payload.purpose)
        .order_by(OTPCode.created_at.desc())
        .all()
    )

    valid_record = None
    now = datetime.utcnow()
    for rec in otp_records:
        if rec.expires_at > now and verify_password(payload.code, rec.code_hash):
            valid_record = rec
            break

    if not valid_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code."
        )

    # Mark OTP as consumed
    valid_record.used = True

    # Activate & verify user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    user.is_email_verified = True
    user.last_login_at = now
    db.commit()

    # Issue tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # Store refresh token
    ref_record = RefreshToken(
        user_id=user.id,
        token_hash=get_password_hash(refresh_token),
        expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    )
    db.add(ref_record)
    db.commit()

    log_login_attempt(db, email, request, success=True)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )

@router.post("/resend-otp", response_model=MessageResponse)
def resend_otp(payload: OTPResendRequest, db: Session = Depends(get_db)):
    """Issue a new OTP verification code"""
    email = payload.email.lower()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # Mark previous as used
    db.query(OTPCode).filter(OTPCode.email == email, OTPCode.used == False).update({"used": True})

    otp = generate_numeric_otp(6)
    otp_record = OTPCode(
        email=email,
        code_hash=get_password_hash(otp),
        purpose=payload.purpose,
        expires_at=datetime.utcnow() + timedelta(minutes=15),
        used=False
    )
    db.add(otp_record)
    db.commit()

    send_otp_email(to_email=email, otp_code=otp, purpose=payload.purpose)

    return MessageResponse(
        message=f"A fresh verification code has been dispatched to {email}."
    )

@router.post("/login", response_model=TokenResponse)
def login(login_in: UserLogin, request: Request, db: Session = Depends(get_db)):
    """Authenticate with email and password, issuing access & refresh tokens"""
    email = login_in.email.lower()
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(login_in.password, user.password_hash):
        log_login_attempt(db, email, request, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Please contact support."
        )

    if not user.is_email_verified:
        # Trigger an OTP automatically so user can complete registration
        otp = generate_numeric_otp(6)
        db.add(OTPCode(
            email=email,
            code_hash=get_password_hash(otp),
            purpose="register",
            expires_at=datetime.utcnow() + timedelta(minutes=15)
        ))
        db.commit()
        send_otp_email(to_email=email, otp_code=otp, purpose="Registration Verification")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. A verification code has been resent to your inbox."
        )

    now = datetime.utcnow()
    user.last_login_at = now
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    db.add(RefreshToken(
        user_id=user.id,
        token_hash=get_password_hash(refresh_token),
        expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    ))
    db.commit()

    log_login_attempt(db, email, request, success=True)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )

@router.post("/google", response_model=TokenResponse)
def google_auth(payload: GoogleLoginRequest, request: Request, db: Session = Depends(get_db)):
    """Exchange Google ID token for application JWT session"""
    email = None
    full_name = "Google User"

    # In production, verify Google token using google-auth library
    if settings.GOOGLE_CLIENT_ID:
        try:
            from google.oauth2 import id_token
            from google.auth.transport import requests as google_requests
            id_info = id_token.verify_oauth2_token(
                payload.id_token, google_requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            email = id_info.get("email")
            full_name = id_info.get("name", "Google User")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid Google ID token: {str(e)}"
            )
    else:
        # Development fallback / test token handler
        email = f"google_user_{payload.id_token[:8]}@gmail.com"

    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not extract email from token.")

    email = email.lower()
    user = db.query(User).filter(User.email == email).first()
    now = datetime.utcnow()

    if not user:
        user = User(
            full_name=full_name,
            email=email,
            password_hash=None,
            role="candidate",
            is_active=True,
            is_email_verified=True,
            auth_provider="google",
            last_login_at=now
        )
        db.add(user)
        db.flush()
        db.add(CandidateProfile(user_id=user.id))
    else:
        user.last_login_at = now

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    db.add(RefreshToken(
        user_id=user.id,
        token_hash=get_password_hash(refresh_token),
        expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    ))
    db.commit()

    log_login_attempt(db, email, request, success=True)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token_endpoint(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Exchange valid refresh token for rotated access & refresh tokens"""
    decoded = decode_token(payload.refresh_token)
    if not decoded or decoded.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token.")

    user_id = decoded.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive or not found.")

    # Check active refresh token in database
    active_tokens = db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.utcnow()
    ).all()

    matched_token = None
    for tok in active_tokens:
        if verify_password(payload.refresh_token, tok.token_hash):
            matched_token = tok
            break

    if not matched_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has been revoked or expired.")

    # Rotate token: revoke old
    matched_token.revoked = True

    # Issue new pair
    now = datetime.utcnow()
    new_access = create_access_token(user.id)
    new_refresh = create_refresh_token(user.id)

    db.add(RefreshToken(
        user_id=user.id,
        token_hash=get_password_hash(new_refresh),
        expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    ))
    db.commit()

    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        user=UserResponse.model_validate(user)
    )

@router.post("/logout", response_model=MessageResponse)
def logout(payload: RefreshTokenRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Revoke user refresh token"""
    active_tokens = db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
        RefreshToken.revoked == False
    ).all()

    for tok in active_tokens:
        if verify_password(payload.refresh_token, tok.token_hash):
            tok.revoked = True
    db.commit()

    return MessageResponse(message="Successfully logged out.")

@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Generate and dispatch password reset token"""
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if user and user.is_active:
        raw_token = str(uuid.uuid4()) + str(uuid.uuid4())
        reset_entry = PasswordResetToken(
            user_id=user.id,
            token_hash=get_password_hash(raw_token),
            expires_at=datetime.utcnow() + timedelta(hours=1),
            used=False
        )
        db.add(reset_entry)
        db.commit()
        send_password_reset_email(to_email=user.email, reset_token=raw_token)

    return MessageResponse(
        message="If this email is registered in our system, a password reset link has been dispatched."
    )

@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset user password using token"""
    now = datetime.utcnow()
    tokens = db.query(PasswordResetToken).filter(
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > now
    ).all()

    matched_reset = None
    for t in tokens:
        if verify_password(payload.token, t.token_hash):
            matched_reset = t
            break

    if not matched_reset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset link."
        )

    matched_reset.used = True
    user = db.query(User).filter(User.id == matched_reset.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    user.password_hash = get_password_hash(payload.new_password)
    # Revoke all existing refresh tokens for security
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).update({"revoked": True})
    db.commit()

    return MessageResponse(
        message="Password has been successfully updated. You may now log in with your new password."
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user details and role"""
    return UserResponse.model_validate(current_user)
