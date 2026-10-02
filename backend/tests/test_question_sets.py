import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.interview import QuestionSet, Question
from app.core.security import create_access_token

@pytest.fixture
def admin_auth_client():
    client = TestClient(app)
    with SessionLocal() as db:
        admin_user = db.query(User).filter(User.role == "admin").first()
        if not admin_user:
            admin_user = User(
                email="admin_qset_test@gims.edu.pk",
                full_name="Admin QSet Tester",
                role="admin",
                is_active=True,
                is_email_verified=True,
                password_hash="fake_hash"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        token = create_access_token(admin_user.id)
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

def test_admin_upload_question_set_json(admin_auth_client):
    """Verify upload custom question set creates QuestionSet row and links questions."""
    q_data = {
        "questions": [
            {
                "question": "What is connection pooling and how does PgBouncer improve throughput?",
                "role": "Full Stack Developer",
                "category": "Technical",
                "difficulty": "Intermediate",
                "expected_keywords": ["pooling", "PgBouncer", "concurrency", "PostgreSQL"],
                "sample_answer": "Connection pooling maintains warm DB sockets to avoid per-request handshake overhead."
            },
            {
                "question": "Explain optimistic vs pessimistic locking in high concurrency systems.",
                "role": "Full Stack Developer",
                "category": "Technical",
                "difficulty": "Advanced",
                "expected_keywords": ["optimistic", "pessimistic", "FOR UPDATE", "versioning"],
                "sample_answer": "Optimistic locking checks version timestamps at commit; pessimistic uses row locks."
            }
        ]
    }
    json_bytes = json.dumps(q_data).encode("utf-8")

    response = admin_auth_client.post(
        "/api/v1/admin/questions/upload-set?set_name=High+Concurrency+Mastery",
        files={"file": ("high_concurrency_questions.json", json_bytes, "application/json")}
    )

    assert response.status_code == 200, f"Upload failed: {response.text}"
    body = response.json()
    assert body["count"] == 2
    assert "question_set_id" in body
    q_set_id = body["question_set_id"]
    assert body["set_name"] == "High Concurrency Mastery"

    # Verify in DB
    with SessionLocal() as db:
        q_set = db.query(QuestionSet).filter(QuestionSet.id == q_set_id).first()
        assert q_set is not None
        assert q_set.name == "High Concurrency Mastery"
        assert len(q_set.questions) == 2

        # Verify linked questions
        for q in q_set.questions:
            assert q.question_set_id == q_set.id
            assert q.is_active is True

    # Verify GET /admin/questions/sets
    list_resp = admin_auth_client.get("/api/v1/admin/questions/sets")
    assert list_resp.status_code == 200
    sets = list_resp.json()
    matched = [s for s in sets if s["id"] == q_set_id]
    assert len(matched) == 1
    assert matched[0]["question_count"] == 2
