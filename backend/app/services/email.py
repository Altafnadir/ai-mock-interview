import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.core.logging import logger

def send_otp_email(to_email: str, otp_code: str, purpose: str = "registration") -> bool:
    """
    Sends an OTP email. If SMTP is not configured or in development mode,
    the OTP is logged prominently to the console so registration/verification is frictionless.
    """
    logger.info(f"[OTP GENERATED] To: {to_email} | Purpose: {purpose} | Code: [{otp_code}]")
    print("\n==========================================")
    print("[EMAIL OTP NOTIFICATION]")
    print(f"To: {to_email}")
    print("Subject: Your GIMS AI Mock Interview OTP Code")
    print(f"Code: {otp_code}")
    print(f"Purpose: {purpose}")
    print("Valid for 15 minutes.")
    print("==========================================\n")

    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your Verification Code: {otp_code} - GIMS AI Mock Interview"
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = to_email

        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <h2 style="color: #2563eb;">AI-Based Mock Interview System</h2>
            <p>Hello,</p>
            <p>Your one-time verification code for <strong>{purpose}</strong> is:</p>
            <div style="background: #f1f5f9; padding: 16px; text-align: center; border-radius: 6px; font-size: 28px; font-weight: bold; letter-spacing: 4px; color: #1e293b;">
                {otp_code}
            </div>
            <p style="margin-top: 20px; color: #64748b; font-size: 14px;">This code will expire in 15 minutes. If you did not request this code, please ignore this email.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;">
            <p style="color: #94a3b8; font-size: 12px; text-align: center;">GIMS, PMAS-Arid Agriculture University (Project: GIMS-BSSE-F202206)</p>
        </div>
        """
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        logger.error(f"Failed to send email via SMTP: {e}. (Console fallback succeeded).")
        return True

def send_password_reset_email(to_email: str, reset_token: str) -> bool:
    reset_link = f"http://localhost:5173/reset-password?token={reset_token}"
    logger.info(f"[PASSWORD RESET LINK] To: {to_email} | Link: {reset_link}")
    print("\n==========================================")
    print("[PASSWORD RESET EMAIL]")
    print(f"To: {to_email}")
    print(f"Reset Link: {reset_link}")
    print("==========================================\n")
    return True

def send_report_email(
    to_email: str,
    candidate_name: str,
    session_id: str,
    overall_score: float,
    verdict: str,
    pdf_path: str = ""
) -> bool:
    """Sends candidate performance report email with overall score and feedback."""
    logger.info(f"[REPORT EMAIL] To: {to_email} | Score: {overall_score} | Verdict: {verdict}")
    print("\n==========================================")
    print("[INTERVIEW PERFORMANCE REPORT EMAIL]")
    print(f"To: {to_email} ({candidate_name})")
    print(f"Session ID: {session_id}")
    print(f"Overall Score: {overall_score}/100")
    print(f"Verdict: {verdict}")
    print(f"PDF Report: {pdf_path}")
    print("==========================================\n")

    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your Mock Interview Performance Report ({overall_score}/100) - GIMS"
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = to_email

        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <h2 style="color: #0284c7;">Mock Interview Performance Report</h2>
            <p>Dear {candidate_name},</p>
            <p>Your AI-analyzed mock interview evaluation report is ready:</p>
            <div style="background: #f8fafc; padding: 16px; border-radius: 6px; text-align: center; margin: 16px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #0284c7;">{overall_score}</span> / 100
                <p style="margin: 4px 0 0 0; font-weight: bold; color: #334155;">{verdict}</p>
            </div>
            <p>Log into your candidate portal to view your comprehensive video, voice, and STAR evaluations.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;">
            <p style="color: #94a3b8; font-size: 12px; text-align: center;">GIMS, PMAS-Arid Agriculture University (Project: GIMS-BSSE-F202206)</p>
        </div>
        """
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        logger.error(f"Failed to send report email via SMTP: {e}. (Console fallback succeeded).")
        return True
