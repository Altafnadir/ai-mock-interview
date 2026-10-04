import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

from app.db.session import SessionLocal
from app.db.models.user import User, CandidateProfile
from app.core.security import get_password_hash, create_access_token

def get_candidate_token():
    test_email = "test_interview_candidate@gims.edu.pk"
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == test_email).first()
        if not user:
            user = User(
                email=test_email,
                full_name="Interview Test Candidate",
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

def test_meta_endpoints():
    # 1. Job Roles
    roles_resp = client.get("/api/v1/meta/job-roles")
    assert roles_resp.status_code == 200
    roles = roles_resp.json()
    assert len(roles) >= 11
    assert any(r["name"] == "Full Stack Developer" for r in roles)

    # 2. Categories
    cats_resp = client.get("/api/v1/meta/categories")
    assert cats_resp.status_code == 200
    cats = cats_resp.json()
    assert len(cats) >= 4
    assert any(c["name"] == "Technical" for c in cats)

    # 3. Difficulties
    diffs_resp = client.get("/api/v1/meta/difficulties")
    assert diffs_resp.status_code == 200
    diffs = diffs_resp.json()
    assert len(diffs) >= 3

    # 4. All Meta
    all_resp = client.get("/api/v1/meta/all")
    assert all_resp.status_code == 200
    all_data = all_resp.json()
    assert "job_roles" in all_data
    assert "categories" in all_data
    assert "difficulties" in all_data

def test_interview_session_lifecycle():
    token = get_candidate_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Fetch metadata IDs
    meta = client.get("/api/v1/meta/all").json()
    role_id = meta["job_roles"][0]["id"]
    category_id = meta["categories"][0]["id"]
    difficulty_id = meta["difficulties"][0]["id"]

    # 2. Create Interview Session (3 questions)
    create_payload = {
        "job_role_id": role_id,
        "category_id": category_id,
        "difficulty_id": difficulty_id,
        "total_questions": 3,
        "mode": "video"
    }
    create_resp = client.post("/api/v1/interviews", json=create_payload, headers=headers)
    assert create_resp.status_code == 201
    session = create_resp.json()
    session_id = session["id"]
    assert session["status"] == "created"
    assert session["total_questions"] == 3
    assert len(session["questions"]) == 3

    # 3. Start Interview
    start_resp = client.post(f"/api/v1/interviews/{session_id}/start", headers=headers)
    assert start_resp.status_code == 200
    started_session = start_resp.json()
    assert started_session["status"] == "in_progress"
    assert started_session["started_at"] is not None

    # 4. Get Current Question
    curr_resp = client.get(f"/api/v1/interviews/{session_id}/current", headers=headers)
    assert curr_resp.status_code == 200
    curr_q = curr_resp.json()
    assert curr_q is not None
    assert curr_q["order_index"] == 1
    assert curr_q["status"] == "pending"

    # 5. Repeat Question
    rep_resp = client.post(f"/api/v1/interviews/{session_id}/repeat", headers=headers)
    assert rep_resp.status_code == 200
    assert rep_resp.json()["question_id"] == curr_q["id"]

    # 6. Answer Question 1
    ans_payload = {
        "transcript": "In our team project, um, we used FastAPI and React to build a secure interview system, like, basically handling requests smoothly.",
        "duration_seconds": 45.0
    }
    ans_resp = client.post(f"/api/v1/interviews/{session_id}/answer", json=ans_payload, headers=headers)
    assert ans_resp.status_code == 200
    answered_q = ans_resp.json()
    assert answered_q["status"] == "answered"
    assert answered_q["answer"] is not None
    assert answered_q["answer"]["filler_word_count"] >= 3  # "um", "like", "basically"
    assert answered_q["answer"]["word_count"] > 10

    # 7. Get Progress after 1 answer
    prog1 = client.get(f"/api/v1/interviews/{session_id}/progress", headers=headers).json()
    assert prog1["answered_questions"] == 1
    assert prog1["total_questions"] == 3
    assert prog1["is_completed"] == False

    # 8. Skip Question 2
    skip_resp = client.post(f"/api/v1/interviews/{session_id}/skip", headers=headers)
    assert skip_resp.status_code == 200
    skipped_q = skip_resp.json()
    assert skipped_q["status"] == "skipped"

    # 9. Answer Question 3
    ans3_payload = {
        "transcript": "To optimize database queries, we utilized PostgreSQL indexes and connection pooling.",
        "duration_seconds": 30.0
    }
    ans3_resp = client.post(f"/api/v1/interviews/{session_id}/answer", json=ans3_payload, headers=headers)
    assert ans3_resp.status_code == 200
    assert ans3_resp.json()["status"] == "answered"

    # 10. Check Progress after all answered/skipped
    prog2 = client.get(f"/api/v1/interviews/{session_id}/progress", headers=headers).json()
    assert prog2["answered_questions"] == 3

    # 11. End Interview
    end_resp = client.post(f"/api/v1/interviews/{session_id}/end", headers=headers)
    assert end_resp.status_code == 200
    ended_session = end_resp.json()
    assert ended_session["status"] == "completed"
    assert ended_session["ended_at"] is not None
    assert ended_session["duration_seconds"] >= 0

    # 12. Check Status
    status_resp = client.get(f"/api/v1/interviews/{session_id}/status", headers=headers)
    assert status_resp.status_code == 200
    st = status_resp.json()
    assert st["status"] in ["completed", "analyzed", "processing"]
    assert st["progress_percentage"] >= 50

def test_dynamic_followup_and_session_management():
    token = get_candidate_token()
    headers = {"Authorization": f"Bearer {token}"}

    meta = client.get("/api/v1/meta/all").json()
    role_id = meta["job_roles"][0]["id"]
    category_id = meta["categories"][0]["id"]
    difficulty_id = meta["difficulties"][0]["id"]

    # 1. Create Session
    create_resp = client.post("/api/v1/interviews", json={
        "job_role_id": role_id,
        "category_id": category_id,
        "difficulty_id": difficulty_id,
        "total_questions": 2
    }, headers=headers)
    assert create_resp.status_code == 201
    session_id = create_resp.json()["id"]

    # Start
    client.post(f"/api/v1/interviews/{session_id}/start", headers=headers)

    # 2. Answer with dynamic follow-up requested
    ans_resp = client.post(f"/api/v1/interviews/{session_id}/answer", json={
        "transcript": "I designed the backend database schema using PostgreSQL and added indexes to solve slow query latency under load.",
        "duration_seconds": 35.0,
        "generate_followup": True
    }, headers=headers)
    assert ans_resp.status_code == 200

    # Verify session now has follow-up question
    detail = client.get(f"/api/v1/interviews/{session_id}", headers=headers).json()
    assert len(detail["questions"]) >= 2
    assert any(q["source"] == "followup" for q in detail["questions"])

    # 3. Test recording upload
    import io
    fake_audio = io.BytesIO(b"RIFF....WAVEfmt ....data....")
    rec_resp = client.post(
        f"/api/v1/interviews/{session_id}/recording",
        files={"audio_file": ("answer.wav", fake_audio.getvalue(), "audio/wav")},
        headers=headers
    )
    assert rec_resp.status_code == 200
    assert "audio_path" in rec_resp.json()

    # 4. Test reprocess
    rep_resp = client.post(f"/api/v1/interviews/{session_id}/reprocess", headers=headers)
    assert rep_resp.status_code == 200

    # 5. Delete session
    del_resp = client.delete(f"/api/v1/interviews/{session_id}", headers=headers)
    assert del_resp.status_code == 200
    assert "deleted successfully" in del_resp.json()["message"]

