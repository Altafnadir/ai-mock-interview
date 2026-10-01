import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def get_candidate_token():
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "candidate@gims.edu.pk",
        "password": "CandidatePassword123!"
    })
    assert login_resp.status_code == 200
    return login_resp.json()["access_token"]

def test_report_generation_pdf_and_share_flow():
    token = get_candidate_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create and complete an interview session
    meta = client.get("/api/v1/meta/all").json()
    create_resp = client.post("/api/v1/interviews", json={
        "job_role_id": meta["job_roles"][0]["id"],
        "category_id": meta["categories"][0]["id"],
        "difficulty_id": meta["difficulties"][0]["id"],
        "total_questions": 2,
        "mode": "video"
    }, headers=headers)
    assert create_resp.status_code == 201
    session_id = create_resp.json()["id"]

    client.post(f"/api/v1/interviews/{session_id}/start", headers=headers)

    ans1 = {
        "transcript": "In my previous role, we designed a microservices architecture using FastAPI, Docker, and PostgreSQL, improving deployment throughput by 40%.",
        "duration_seconds": 45.0
    }
    client.post(f"/api/v1/interviews/{session_id}/answer", json=ans1, headers=headers)

    ans2 = {
        "transcript": "To secure communication, we configured JWT rotation, CORS middleware, and automated rate limiting.",
        "duration_seconds": 35.0
    }
    client.post(f"/api/v1/interviews/{session_id}/answer", json=ans2, headers=headers)

    client.post(f"/api/v1/interviews/{session_id}/end", headers=headers)

    # 2. Get Session Report (triggers pipeline and PDF generation)
    report_resp = client.get(f"/api/v1/reports/{session_id}", headers=headers)
    assert report_resp.status_code == 200
    report = report_resp.json()
    assert report["session_id"] == session_id
    assert 0 <= report["overall_score"] <= 100
    assert report["final_verdict"] in [
        "Strong Hire / Recommended",
        "Hire / Qualified",
        "Borderline / Needs Practice",
        "Needs Significant Improvement"
    ]
    assert len(report["strengths"]) > 0
    assert len(report["recommendations"]) > 0
    assert report["pdf_path"] is not None

    # 3. Download PDF Report
    pdf_resp = client.get(f"/api/v1/reports/{session_id}/pdf", headers=headers)
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert len(pdf_resp.content) > 1000  # valid PDF binary

    # 4. Generate Public Share Link
    share_resp = client.post(f"/api/v1/reports/{session_id}/share", headers=headers)
    assert share_resp.status_code == 200
    share_data = share_resp.json()
    share_token = share_data["token"]
    assert len(share_token) > 10
    assert "/shared/" in share_data["share_url"]

    # 5. Access Public Report (unauthenticated, no headers)
    public_resp = client.get(f"/api/v1/reports/public/{share_token}")
    assert public_resp.status_code == 200
    pub_data = public_resp.json()
    assert pub_data["session_id"] == session_id
    assert pub_data["overall_score"] == report["overall_score"]

    # 6. Download Public PDF Report (unauthenticated, no headers)
    public_pdf_resp = client.get(f"/api/v1/reports/public/{share_token}/pdf")
    assert public_pdf_resp.status_code == 200
    assert public_pdf_resp.headers["content-type"] == "application/pdf"
    assert len(public_pdf_resp.content) > 1000
