import sys
import os
import io
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.db.session import SessionLocal
from app.db.models.user import User

client = TestClient(app)

from app.core.security import get_password_hash, create_access_token
from app.db.models.user import CandidateProfile

def get_candidate_token():
    test_email = "test_profile_candidate@gims.edu.pk"
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == test_email).first()
        if not user:
            user = User(
                email=test_email,
                full_name="Profile Test User",
                password_hash=get_password_hash("TestPassword123!"),
                role="candidate",
                is_active=True,
                is_email_verified=True,
                auth_provider="local"
            )
            db.add(user)
            db.flush()
            profile = CandidateProfile(user_id=user.id, experience_level="beginner")
            db.add(profile)
            db.commit()
            db.refresh(user)
        return create_access_token(user.id)
    finally:
        db.close()

def test_get_and_update_candidate_profile():
    token = get_candidate_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Get Profile
    resp = client.get("/api/v1/profile", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test_profile_candidate@gims.edu.pk"
    assert "profile" in data

    # 2. Update Profile
    update_payload = {
        "phone": "+92 333 9876543",
        "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker"],
        "preferred_job_roles": ["Full Stack Developer", "Backend Developer"],
        "experience_level": "intermediate",
        "education": [
            {
                "degree": "BS Software Engineering",
                "institution": "PMAS Arid Agriculture University Rawalpindi",
                "year": "2024",
                "grade": "3.85 CGPA"
            }
        ],
        "work_experience": [
            {
                "role": "Junior Full Stack Engineer",
                "company": "Tech Solutions",
                "duration": "1 year",
                "description": "Developed microservices and frontend dashboards."
            }
        ],
        "certifications": ["AWS Certified Cloud Practitioner"]
    }
    update_resp = client.put("/api/v1/profile", json=update_payload, headers=headers)
    assert update_resp.status_code == 200
    updated_profile = update_resp.json()
    assert updated_profile["phone"] == "+92 333 9876543"
    assert "Python" in updated_profile["skills"]
    assert updated_profile["experience_level"] == "intermediate"

def test_resume_upload_and_analysis_flow():
    token = get_candidate_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Create a mock PDF file using reportlab or minimal PDF bytes
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 750, "Hamza Tariq - Full Stack Developer")
    c.drawString(100, 730, "Email: hamza@example.com | Phone: +92 300 1234567")
    c.drawString(100, 700, "EDUCATION")
    c.drawString(100, 680, "Bachelor of Science in Software Engineering, PMAS AAUR, 2024, CGPA 3.8")
    c.drawString(100, 650, "TECHNICAL SKILLS")
    c.drawString(100, 630, "Python, React, FastAPI, JavaScript, Docker, Git, PostgreSQL, REST API")
    c.drawString(100, 600, "EXPERIENCE")
    c.drawString(100, 580, "Software Engineer Intern at DevHouse (Jan 2023 - Jun 2023)")
    c.drawString(100, 560, "Engineered REST APIs with FastAPI and optimized queries, boosting speed by 30%.")
    c.drawString(100, 530, "PROJECTS")
    c.drawString(100, 510, "Mock Interview Platform - Built end-to-end interview simulation tool using React and Python.")
    c.drawString(100, 480, "CERTIFICATIONS")
    c.drawString(100, 460, "AWS Certified Cloud Practitioner")
    c.save()
    pdf_buffer.seek(0)

    # 1. Upload Resume
    upload_resp = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("hamza_resume.pdf", pdf_buffer.getvalue(), "application/pdf")},
        headers=headers
    )
    assert upload_resp.status_code == 201, f"Upload failed: {upload_resp.text}"
    resume_data = upload_resp.json()
    resume_id = resume_data["id"]
    assert resume_data["original_filename"] == "hamza_resume.pdf"
    assert resume_data["file_type"] == "pdf"
    assert "analysis" in resume_data
    analysis = resume_data["analysis"]
    assert analysis["status"] == "analyzed"
    assert len(analysis["extracted_skills"]) > 0
    assert "Python" in analysis["extracted_skills"]

    # 2. Get Resumes list
    list_resp = client.get("/api/v1/resumes", headers=headers)
    assert list_resp.status_code == 200
    resumes = list_resp.json()
    assert any(r["id"] == resume_id for r in resumes)

    # 3. Get Single Resume
    single_resp = client.get(f"/api/v1/resumes/{resume_id}", headers=headers)
    assert single_resp.status_code == 200
    assert single_resp.json()["id"] == resume_id

    # 4. Re-analyze against DevOps Engineer role
    reanalyze_resp = client.post(
        f"/api/v1/resumes/{resume_id}/analyze",
        json={"job_role_name": "DevOps Engineer"},
        headers=headers
    )
    assert reanalyze_resp.status_code == 200
    reanalyzed = reanalyze_resp.json()
    assert reanalyzed["status"] == "analyzed"
    missing_skills = [m["skill"] for m in reanalyzed["missing_skills"]]
    # DevOps needs Linux, Kubernetes, Terraform etc. which should be identified
    assert "Linux" in missing_skills or "Kubernetes" in missing_skills or "Terraform" in missing_skills

    # 4b. Test v2 /reanalyze endpoint
    v2_re = client.post(f"/api/v1/resumes/{resume_id}/reanalyze", headers=headers)
    assert v2_re.status_code == 200
    assert "resume_score" in v2_re.json()

    # 4c. Test v2 /analysis summary endpoint
    sum_an = client.get(f"/api/v1/resumes/{resume_id}/analysis", headers=headers)
    assert sum_an.status_code == 200
    assert "resume_score" in sum_an.json()
    assert "score_label" in sum_an.json()
    assert "top_skills" in sum_an.json()

    # 4d. Test v2 /analysis/full detail endpoint
    full_an = client.get(f"/api/v1/resumes/{resume_id}/analysis/full", headers=headers)
    assert full_an.status_code == 200
    assert "strengths" in full_an.json()
    assert "areas_to_improve" in full_an.json()
    assert "extracted_skills" in full_an.json()
    assert "extracted_education" in full_an.json()

    # 5. Delete Resume
    del_resp = client.delete(f"/api/v1/resumes/{resume_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Resume deleted successfully"

    # Verify 404 after deletion
    get_del = client.get(f"/api/v1/resumes/{resume_id}", headers=headers)
    assert get_del.status_code == 404
