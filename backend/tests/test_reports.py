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

def test_report_generation_all_3_pdfs_and_share_flow():
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
        "Excellent", "Good", "Needs Improvement", "Needs Significant Practice",
        "Strong Hire / Recommended", "Hire / Qualified", "Borderline / Needs Practice"
    ]
    assert len(report["strengths"]) > 0
    assert report["pdf_path"] is not None

    # 3. Download Full PDF Report
    pdf_resp = client.get(f"/api/v1/reports/{session_id}/pdf", headers=headers)
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert len(pdf_resp.content) > 1000

    # 4. Download 1-Page AI Performance Summary PDF
    summary_resp = client.get(f"/api/v1/reports/{session_id}/summary-pdf", headers=headers)
    assert summary_resp.status_code == 200
    assert summary_resp.headers["content-type"] == "application/pdf"
    assert len(summary_resp.content) > 1000

    # 5. Download Performance Poster PDF
    poster_resp = client.get(f"/api/v1/reports/{session_id}/poster", headers=headers)
    assert poster_resp.status_code == 200
    assert poster_resp.headers["content-type"] == "application/pdf"
    assert len(poster_resp.content) > 1000

    # 6. Generate Public Share Link
    share_resp = client.post(f"/api/v1/reports/{session_id}/share", headers=headers)
    assert share_resp.status_code == 200
    share_data = share_resp.json()
    share_token = share_data["token"]
    assert len(share_token) > 10
    assert "/shared/" in share_data["share_url"]

    # 7. Access Public Report (unauthenticated, both route variants)
    pub_resp1 = client.get(f"/api/v1/reports/public/{share_token}")
    assert pub_resp1.status_code == 200
    assert pub_resp1.json()["overall_score"] == report["overall_score"]

    pub_resp2 = client.get(f"/api/v1/public/reports/{share_token}")
    assert pub_resp2.status_code == 200
    assert pub_resp2.json()["session_id"] == session_id

    # 8. Download Public PDF Report
    public_pdf_resp = client.get(f"/api/v1/public/reports/{share_token}/pdf")
    assert public_pdf_resp.status_code == 200
    assert public_pdf_resp.headers["content-type"] == "application/pdf"
    assert len(public_pdf_resp.content) > 1000

    # 9. Email Report
    email_resp = client.post(f"/api/v1/reports/{session_id}/email", headers=headers)
    assert email_resp.status_code == 200

    # 10. Revoke Share Link
    revoke_resp = client.delete(f"/api/v1/reports/share/{share_token}", headers=headers)
    assert revoke_resp.status_code == 200
    assert revoke_resp.json()["is_revoked"] is True

    # 11. Accessing revoked share link returns 404
    revoked_check = client.get(f"/api/v1/public/reports/{share_token}")
    assert revoked_check.status_code == 404
