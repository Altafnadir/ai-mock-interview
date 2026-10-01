import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.db.session import SessionLocal
from app.db.models.user import OTPCode, User

client = TestClient(app)

def test_admin_login():
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@gims.edu.pk",
        "password": "AdminSecurePassword123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["role"] == "admin"
    assert data["user"]["email"] == "admin@gims.edu.pk"

    # Test GET /auth/me with access token
    token = data["access_token"]
    me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "admin@gims.edu.pk"

def test_candidate_registration_and_otp_flow():
    test_email = "new_test_candidate@gims.edu.pk"
    
    # 1. Register
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": test_email,
        "full_name": "Test Candidate",
        "password": "SecurePassword123!"
    })
    assert reg_resp.status_code == 201
    assert "verification code" in reg_resp.json()["message"]

    # 2. Query DB for generated OTP
    db = SessionLocal()
    try:
        otp_entry = db.query(OTPCode).filter(
            OTPCode.email == test_email,
            OTPCode.used == False
        ).order_by(OTPCode.created_at.desc()).first()
        assert otp_entry is not None
        
        # Test invalid OTP code
        bad_verify = client.post("/api/v1/auth/verify-otp", json={
            "email": test_email,
            "code": "000000",
            "purpose": "register"
        })
        assert bad_verify.status_code == 400
    finally:
        db.close()

def test_token_refresh():
    # Login as admin
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "admin@gims.edu.pk",
        "password": "AdminSecurePassword123!"
    })
    refresh_token = login_resp.json()["refresh_token"]

    # Refresh
    ref_resp = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert ref_resp.status_code == 200
    ref_data = ref_resp.json()
    assert "access_token" in ref_data
    assert "refresh_token" in ref_data
    assert ref_data["refresh_token"] != refresh_token  # Rotated!
