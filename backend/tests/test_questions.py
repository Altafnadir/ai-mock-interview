from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.models.user import User, CandidateProfile
from app.core.security import get_password_hash, create_access_token

client = TestClient(app)

def get_candidate_headers():
    test_email = "test_qgen_candidate@gims.edu.pk"
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == test_email).first()
        if not user:
            user = User(
                email=test_email,
                full_name="QGen Test Candidate",
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
        token = create_access_token(user.id)
        return {"Authorization": f"Bearer {token}"}
    finally:
        db.close()

def test_generate_questions_preview():
    headers = get_candidate_headers()
    payload = {
        "role": "Frontend Developer",
        "level": "2-5 Years",
        "type": "Technical",
        "difficulty": "Medium",
        "count": 5
    }
    response = client.post("/api/v1/questions/generate-preview", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) >= 1
    assert data["role"] == "Frontend Developer"
    assert data["type"] == "Technical"
    for q in data["questions"]:
        assert "question_text" in q
        assert "order_index" in q

def test_create_interview_with_custom_questions():
    headers = get_candidate_headers()
    # Fetch metadata for job_role, category, difficulty
    meta_resp = client.get("/api/v1/meta", headers=headers)
    assert meta_resp.status_code == 200
    meta = meta_resp.json()
    
    role_id = meta["job_roles"][0]["id"]
    category_id = meta["interview_categories"][0]["id"]
    difficulty_id = meta["difficulty_levels"][0]["id"]

    custom_qs = [
        "Explain how the React Virtual DOM diffing algorithm works.",
        "What is the difference between useMemo and useCallback?",
        "How would you optimize the performance of a large React list?"
    ]

    create_payload = {
        "job_role_id": role_id,
        "category_id": category_id,
        "difficulty_id": difficulty_id,
        "total_questions": len(custom_qs),
        "custom_questions": custom_qs,
        "mode": "video"
    }

    create_resp = client.post("/api/v1/interviews", json=create_payload, headers=headers)
    assert create_resp.status_code == status.HTTP_201_CREATED
    session_data = create_resp.json()
    assert session_data["total_questions"] == 3
    assert len(session_data["questions"]) == 3
    assert session_data["questions"][0]["question_text"] == custom_qs[0]
    assert session_data["questions"][0]["source"] == "custom"
