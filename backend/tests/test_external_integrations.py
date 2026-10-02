import os
import smtplib
import pytest
from app.core.config import settings
from app.services.email import send_otp_email, send_report_email
from app.services.storage import storage_service

# --- UNIT TESTS (Mock-based / Fallback paths that always pass in test environments) ---

def test_email_service_fallback_when_credentials_empty():
    # When SMTP credentials are not provided, send_otp_email logs to console and returns True
    success = send_otp_email("candidate_test@example.com", "123456", "test_registration")
    assert success is True

def test_report_email_fallback_when_credentials_empty():
    success = send_report_email(
        to_email="candidate_test@example.com",
        candidate_name="Test Candidate",
        session_id="sess-mock-123",
        overall_score=85.5,
        verdict="Strong Candidate"
    )
    assert success is True

def test_storage_service_local_operations(tmp_path):
    # Tests local directory creation and path resolution
    resumes_dir = storage_service.subdirs.get("resumes")
    assert resumes_dir is not None
    assert resumes_dir.exists()

# --- INTEGRATION TESTS (Auto-skip when environment variables are missing) ---

@pytest.mark.skipif(
    not settings.SMTP_USER or not settings.SMTP_PASSWORD,
    reason="Live SMTP integration requires SMTP_USER and SMTP_PASSWORD to be configured in .env"
)
def test_live_smtp_connection():
    """Live test: verifies active TLS connection and authentication with configured SMTP host."""
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
        if settings.SMTP_TLS:
            server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        # Authentication successful
        assert True

@pytest.mark.skipif(
    not settings.GOOGLE_CLIENT_ID,
    reason="Live Google OAuth integration requires GOOGLE_CLIENT_ID to be configured in .env"
)
def test_live_google_oauth_configuration():
    """Live test: verifies Google client ID format and public token verification endpoint reachability."""
    import urllib.request
    assert settings.GOOGLE_CLIENT_ID.endswith(".apps.googleusercontent.com") or len(settings.GOOGLE_CLIENT_ID) > 10
    # Check that Google's public token certs endpoint is reachable
    req = urllib.request.Request("https://www.googleapis.com/oauth2/v3/certs", headers={"User-Agent": "FastAPI"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        assert resp.status == 200

@pytest.mark.skipif(
    settings.STORAGE_TYPE != "s3" or not settings.S3_ACCESS_KEY or not settings.S3_SECRET_KEY,
    reason="Live S3/MinIO integration requires STORAGE_TYPE=s3, S3_ACCESS_KEY, and S3_SECRET_KEY in .env"
)
def test_live_s3_storage_connection():
    """Live test: verifies S3 or MinIO bucket connectivity using boto3."""
    import boto3
    s3_kwargs = {
        "aws_access_key_id": settings.S3_ACCESS_KEY,
        "aws_secret_access_key": settings.S3_SECRET_KEY,
    }
    if settings.S3_ENDPOINT_URL:
        s3_kwargs["endpoint_url"] = settings.S3_ENDPOINT_URL

    s3_client = boto3.client("s3", **s3_kwargs)
    # List buckets to confirm authentication
    buckets = s3_client.list_buckets()
    assert "Buckets" in buckets
