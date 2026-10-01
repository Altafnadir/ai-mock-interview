import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.system import Notification
from app.db.models.resource import LearningResource

client = TestClient(app)

@pytest.fixture
def auth_header():
    db = SessionLocal()
    user = db.query(User).filter(User.email == "candidate@gims.edu.pk").first()
    db.close()
    assert user is not None
    res = client.post("/api/v1/auth/login", json={"email": "candidate@gims.edu.pk", "password": "CandidatePassword123!"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_candidate_dashboard(auth_header):
    res = client.get("/api/v1/dashboard/candidate", headers=auth_header)
    assert res.status_code == 200
    data = res.json()
    assert "total_interviews" in data
    assert "readiness_percentage" in data
    assert "dimension_averages" in data
    assert "recent_sessions" in data
    assert "weak_areas" in data
    assert "recommended_resources" in data

def test_dashboard_overview(auth_header):
    res = client.get("/api/v1/dashboard/overview", headers=auth_header)
    assert res.status_code == 200
    data = res.json()
    assert "metrics" in data
    assert "total_interviews" in data["metrics"]
    assert "practice_streak_days" in data["metrics"]
    assert "competency_radar" in data
    assert isinstance(data["competency_radar"], list)
    assert len(data["competency_radar"]) == 6
    assert "recent_sessions" in data
    assert "score_trend" in data

def test_dashboard_trends(auth_header):
    res = client.get("/api/v1/dashboard/trends", headers=auth_header)
    assert res.status_code == 200
    data = res.json()
    assert "trends" in data
    assert isinstance(data["trends"], list)

def test_get_learning_resources(auth_header):
    res = client.get("/api/v1/resources", headers=auth_header)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first_res = data[0]
    assert "title" in first_res
    assert "platform" in first_res
    assert "weak_area_tag" in first_res

    # Test filtering by weak area
    tag = first_res["weak_area_tag"]
    filtered = client.get(f"/api/v1/resources?weak_area={tag}", headers=auth_header)
    assert filtered.status_code == 200
    filtered_data = filtered.json()
    for r in filtered_data:
        assert r["weak_area_tag"] == tag

def test_get_single_resource(auth_header):
    all_res = client.get("/api/v1/resources", headers=auth_header).json()
    res_id = all_res[0]["id"]
    res = client.get(f"/api/v1/resources/{res_id}", headers=auth_header)
    assert res.status_code == 200
    assert res.json()["id"] == res_id

    # 404 test
    not_found = client.get("/api/v1/resources/non-existent-id", headers=auth_header)
    assert not_found.status_code == 404

def test_get_recommendations_shortcut(auth_header):
    res = client.get("/api/v1/recommendations", headers=auth_header)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_practice_questions(auth_header):
    res = client.get("/api/v1/practice/questions?limit=5", headers=auth_header)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    if len(data) > 0:
        q = data[0]
        assert "text" in q
        assert "category_name" in q
        assert "expected_keywords" in q

def test_get_practice_drills(auth_header):
    res = client.get("/api/v1/practice/drills", headers=auth_header)
    assert res.status_code == 200
    drills = res.json()
    assert len(drills) >= 4
    assert any(d["tag"] == "filler_words" for d in drills)

def test_notifications_workflow(auth_header):
    # Ensure there is at least one notification
    db = SessionLocal()
    notif = db.query(Notification).first()
    if not notif:
        notif = Notification(
            title="System Alert",
            message="Test announcement for candidates",
            type="announcement",
            is_read=False
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)
    notif_id = notif.id
    db.close()

    # Get notifications
    res = client.get("/api/v1/notifications", headers=auth_header)
    assert res.status_code == 200
    notifs = res.json()
    assert len(notifs) > 0

    # Unread count
    count_res = client.get("/api/v1/notifications/unread-count", headers=auth_header)
    assert count_res.status_code == 200
    assert "unread_count" in count_res.json()

    # Mark as read
    read_res = client.put(f"/api/v1/notifications/{notif_id}/read", headers=auth_header)
    assert read_res.status_code == 200
    assert read_res.json()["is_read"] is True

    # Mark all read
    all_read = client.put("/api/v1/notifications/read-all", headers=auth_header)
    assert all_read.status_code == 200

def test_compare_sessions(auth_header):
    # Fetch recent sessions from dashboard
    dash_res = client.get("/api/v1/dashboard/overview", headers=auth_header)
    assert dash_res.status_code == 200
    recent = dash_res.json()["recent_sessions"]
    if len(recent) >= 2:
        id1, id2 = recent[0]["id"], recent[1]["id"]
        res = client.get(f"/api/v1/dashboard/compare?ids={id1},{id2}", headers=auth_header)
        assert res.status_code == 200
        comp = res.json()["comparison"]
        assert len(comp) == 2
        assert comp[0]["session_id"] in [id1, id2]
        assert "overall_score" in comp[0]

def test_recommender_re_ranking():
    from app.ai.feedback_generator import feedback_generator
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "candidate@gims.edu.pk").first()
        assert user is not None
        recs = feedback_generator.create_recommendations(
            db=db,
            user_id=user.id,
            session_id="dummy-session-123",
            weak_area_tags=["star_method", "filler_words", "eye_contact", "technical"]
        )
        assert len(recs) > 0
        tag_list = [r.weak_area_tag for r in recs]
        assert any(t in feedback_generator.CANONICAL_TAGS for t in tag_list)
        for r in recs:
            assert len(r.practice_suggestion) > 10
    finally:
        db.close()

