from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import Any

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User, CandidateProfile
from app.schemas.profile import UserProfileResponse, CandidateProfileResponse, CandidateProfileUpdate
from app.services.storage import storage_service

router = APIRouter()

@router.get("", response_model=UserProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Fetch current user profile and candidate details."""
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        db.refresh(current_user)

    return current_user

@router.put("", response_model=CandidateProfileResponse)
def update_profile(
    profile_in: CandidateProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Update candidate profile attributes (skills, education, experience, roles)."""
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(user_id=current_user.id)
        db.add(profile)

    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile

@router.post("/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Upload or update user profile picture."""
    allowed_exts = [".jpg", ".jpeg", ".png", ".webp"]
    # Remove previous avatar if exists
    if current_user.profile_picture_path:
        storage_service.delete_file(current_user.profile_picture_path)

    stored_path, original_filename = storage_service.save_upload_file(
        file=file,
        folder="avatars",
        allowed_extensions=allowed_exts
    )

    current_user.profile_picture_path = stored_path
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Avatar uploaded successfully",
        "profile_picture_path": stored_path,
        "filename": original_filename
    }

@router.delete("/avatar")
def delete_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Remove user profile picture."""
    if current_user.profile_picture_path:
        storage_service.delete_file(current_user.profile_picture_path)
        current_user.profile_picture_path = None
        db.commit()

    return {"message": "Avatar removed successfully"}
