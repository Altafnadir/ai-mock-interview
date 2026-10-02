import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.core.logging import logger

def _get_logo_base64() -> str:
    """Retrieves brand logo base64 string for inline email headers."""
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "reports", "assets", "logo-full.png"),
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "public", "brand", "logo-full.png"),
        os.path.join(os.path.dirname(__file__), "..", "reports", "assets", "logo-icon.png"),
    ]
    for p in possible_paths:
        norm = os.path.abspath(p)
        if os.path.exists(norm):
            try:
                with open(norm, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""

def _build_email_header_html() -> str:
    b64 = _get_logo_base64()
    if b64:
        return f"""
        <div style="text-align: center; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; margin-bottom: 20px;">
            <img src="data:image/png;base64,{b64}" alt="Mock Interview AI" width="180" style="display: inline-block; max-width: 180px; height: auto;" />
        </div>
        """
    return """
    <div style="text-align: center; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; margin-bottom: 20px;">
        <h1 style="color: #1858e8; margin: 0; font-size: 22px; font-weight: bold;">Mock Interview AI</h1>
        <p style="color: #64748b; margin: 4px 0 0 0; font-size: 12px;">Practice. Analyze. Get Hired.</p>
    </div>
    """

def send_otp_email(to_email: str, otp_code: str, purpose: str = "registration") -> bool:
    """
    Sends an OTP email with branded header and fallback.
    """
    logger.info(f"[OTP GENERATED] To: {to_email} | Purpose: {purpose} | Code: [{otp_code}]")
    print("\n==========================================")
    print("[EMAIL OTP NOTIFICATION]")
    print(f"To: {to_email}")
    print("Subject: Your Mock Interview AI Verification Code")
    print(f"Code: {otp_code}")
    print(f"Purpose: {purpose}")
    print("Valid for 15 minutes.")
    print("==========================================\n")

    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your Verification Code: {otp_code} - Mock Interview AI"
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = to_email

        header_html = _build_email_header_html()
        html_content = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 580px; margin: auto; padding: 28px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff;">
            {header_html}
            <h2 style="color: #0f172a; font-size: 18px; margin-top: 0;">Verification Code</h2>
            <p style="color: #475569; font-size: 14px; line-height: 1.5;">Hello,</p>
            <p style="color: #475569; font-size: 14px; line-height: 1.5;">Your one-time verification code for <strong>{purpose}</strong> is:</p>
            <div style="background: #f1f5f9; padding: 18px; text-align: center; border-radius: 8px; font-size: 32px; font-weight: 800; letter-spacing: 6px; color: #1858e8; margin: 20px 0;">
                {otp_code}
            </div>
            <p style="color: #64748b; font-size: 13px; line-height: 1.4;">This code expires in 15 minutes. If you did not request this, please disregard this email.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 24px 0 16px 0;">
            <p style="color: #94a3b8; font-size: 11px; text-align: center; margin: 0;">Mock Interview AI &bull; GIMS, PMAS-Arid Agriculture University (Project: GIMS-BSSE-F202206)</p>
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

    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Reset Your Password - Mock Interview AI"
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = to_email

        header_html = _build_email_header_html()
        html_content = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 580px; margin: auto; padding: 28px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff;">
            {header_html}
            <h2 style="color: #0f172a; font-size: 18px; margin-top: 0;">Password Reset Request</h2>
            <p style="color: #475569; font-size: 14px; line-height: 1.5;">We received a request to reset your password. Click the button below to choose a new password:</p>
            <div style="text-align: center; margin: 24px 0;">
                <a href="{reset_link}" style="background-color: #1858e8; color: #ffffff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px; display: inline-block;">Reset Password</a>
            </div>
            <p style="color: #64748b; font-size: 12px;">If you did not request a password reset, you can safely ignore this email.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 24px 0 16px 0;">
            <p style="color: #94a3b8; font-size: 11px; text-align: center; margin: 0;">Mock Interview AI &bull; GIMS, PMAS-Arid Agriculture University (Project: GIMS-BSSE-F202206)</p>
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
        logger.error(f"Failed to send password reset email via SMTP: {e}.")
        return True

def send_report_email(
    to_email: str,
    candidate_name: str,
    session_id: str,
    overall_score: float,
    verdict: str,
    pdf_path: str = ""
) -> bool:
    """Sends candidate performance report email with overall score and branded feedback."""
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
        msg["Subject"] = f"Your Performance Report ({overall_score}/100) - Mock Interview AI"
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = to_email

        header_html = _build_email_header_html()
        html_content = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 580px; margin: auto; padding: 28px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff;">
            {header_html}
            <h2 style="color: #0f172a; font-size: 18px; margin-top: 0;">Performance Evaluation Report</h2>
            <p style="color: #475569; font-size: 14px; line-height: 1.5;">Dear {candidate_name},</p>
            <p style="color: #475569; font-size: 14px; line-height: 1.5;">Your AI-analyzed mock interview evaluation report is ready:</p>
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                <span style="font-size: 38px; font-weight: 800; color: #1858e8;">{overall_score:.1f}</span>
                <span style="font-size: 16px; color: #64748b;">/ 100</span>
                <p style="margin: 8px 0 0 0; font-weight: bold; font-size: 15px; color: #0f172a;">{verdict}</p>
            </div>
            <p style="color: #475569; font-size: 14px; line-height: 1.5;">Sign in to your candidate portal to view your comprehensive video, vocal acoustics, and STAR competency breakdown.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 24px 0 16px 0;">
            <p style="color: #94a3b8; font-size: 11px; text-align: center; margin: 0;">Mock Interview AI &bull; GIMS, PMAS-Arid Agriculture University (Project: GIMS-BSSE-F202206)</p>
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
