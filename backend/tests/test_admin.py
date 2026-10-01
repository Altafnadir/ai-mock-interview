import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ADMIN_CREDENTIALS = {
    "email": "admin@gims.edu.pk",
    "password": "AdminSecurePassword123!"
}

CANDIDATE_CREDENTIALS = {
    "email": "candidate@gims.edu.pk",
    "password": "CandidatePassword123!"
}

@pytest.fixture(scope="module")
def admin_headers():
    res = client.post("/api/v1/auth/login", json=ADMIN_CREDENTIALS)
    assert res.status_code == 200, f"Admin login failed: {res.text}"
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def candidate_headers():
    res = client.post("/api/v1/auth/login", json=CANDIDATE_CREDENTIALS)
    assert res.status_code == 200, f"Candidate login failed: {res.text}"
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_admin_rbac_forbidden_for_candidate(candidate_headers):
    # Candidate should be blocked from admin dashboard with 403 Forbidden
    res = client.get("/api/v1/admin/dashboard", headers=candidate_headers)
    assert res.status_code == 403
    assert "Access denied" in res.json().get("detail", "")

def test_admin_rbac_unauthorized_without_token():
    res = client.get("/api/v1/admin/dashboard")
    assert res.status_code == 401

def test_admin_dashboard(admin_headers):
    res = client.get("/api/v1/admin/dashboard", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "metrics" in data
    assert "recent_sessions" in data
    assert data["metrics"]["total_questions"] >= 100
    assert data["metrics"]["system_status"] == "operational"

def test_admin_analytics(admin_headers):
    res = client.get("/api/v1/admin/analytics", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "activity_over_time" in data
    assert "role_averages" in data
    assert len(data["activity_over_time"]) == 7

def test_admin_user_management(admin_headers):
    # List users
    res = client.get("/api/v1/admin/users", headers=admin_headers)
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 2

    candidate_user = next((u for u in users if u["email"] == "candidate@gims.edu.pk"), None)
    assert candidate_user is not None
    user_id = candidate_user["id"]

    # Get single user
    res_single = client.get(f"/api/v1/admin/users/{user_id}", headers=admin_headers)
    assert res_single.status_code == 200
    assert res_single.json()["email"] == "candidate@gims.edu.pk"

    # Deactivate and activate user
    res_deact = client.put(f"/api/v1/admin/users/{user_id}/deactivate", headers=admin_headers)
    assert res_deact.status_code == 200
    assert res_deact.json()["is_active"] is False

    res_act = client.put(f"/api/v1/admin/users/{user_id}/activate", headers=admin_headers)
    assert res_act.status_code == 200
    assert res_act.json()["is_active"] is True

def test_admin_question_crud_and_bulk(admin_headers):
    # Fetch roles & categories first
    roles_res = client.get("/api/v1/admin/job-roles", headers=admin_headers)
    assert roles_res.status_code == 200
    roles_data = roles_res.json()
    assert len(roles_data) > 0
    role_id = roles_data[0]["id"]

    cats_res = client.get("/api/v1/admin/categories", headers=admin_headers)
    assert cats_res.status_code == 200
    cats_data = cats_res.json()
    assert len(cats_data) > 0
    category_id = cats_data[0]["id"]

    diffs_res = client.get("/api/v1/admin/difficulties", headers=admin_headers)
    assert diffs_res.status_code == 200
    diffs_data = diffs_res.json()
    assert len(diffs_data) > 0
    difficulty_id = diffs_data[0]["id"]

    # Create question
    create_payload = {
        "text": "What are the core design principles of RESTful microservices?",
        "job_role_id": role_id,
        "category_id": category_id,
        "difficulty_id": difficulty_id,
        "expected_keywords": ["stateless", "cacheable", "idempotent", "contract"],
        "sample_answer": "REST principles include statelessness, client-server decoupling, and standard HTTP methods."
    }
    create_res = client.post("/api/v1/admin/questions", json=create_payload, headers=admin_headers)
    assert create_res.status_code == 200
    q_data = create_res.json()
    q_id = q_data["id"]
    assert q_data["text"] == create_payload["text"]

    # Update question
    update_res = client.put(
        f"/api/v1/admin/questions/{q_id}",
        json={"text": "What are the core design principles of RESTful APIs?"},
        headers=admin_headers
    )
    assert update_res.status_code == 200
    assert update_res.json()["text"] == "What are the core design principles of RESTful APIs?"

    # Bulk upload JSON questions
    bulk_json = """[
        {"question": "Explain ACID properties in relational databases.", "role": "Backend Developer", "category": "Technical", "difficulty": "Intermediate", "keywords": ["atomicity", "consistency", "isolation", "durability"]}
    ]"""
    files = {"file": ("bulk.json", bulk_json.encode("utf-8"), "application/json")}
    bulk_res = client.post("/api/v1/admin/questions/bulk-upload", files=files, headers=admin_headers)
    assert bulk_res.status_code == 200
    assert bulk_res.json()["count"] >= 1

    # Delete question
    del_res = client.delete(f"/api/v1/admin/questions/{q_id}", headers=admin_headers)
    assert del_res.status_code == 200

def test_admin_taxonomies(admin_headers):
    # Job roles
    roles_res = client.get("/api/v1/admin/job-roles", headers=admin_headers)
    assert roles_res.status_code == 200
    assert len(roles_res.json()) >= 10

    # Categories
    cats_res = client.get("/api/v1/admin/categories", headers=admin_headers)
    assert cats_res.status_code == 200
    assert len(cats_res.json()) >= 4

    # Difficulties
    diffs_res = client.get("/api/v1/admin/difficulties", headers=admin_headers)
    assert diffs_res.status_code == 200
    assert len(diffs_res.json()) == 3

def test_admin_resources_and_templates(admin_headers):
    # Resource creation
    res_payload = {
        "title": "Mastering Behavioral Interviews Using STAR",
        "url": "https://www.youtube.com/watch?v=sample",
        "platform": "youtube",
        "weak_area_tag": "star_method",
        "difficulty": "All"
    }
    r_create = client.post("/api/v1/admin/resources", json=res_payload, headers=admin_headers)
    assert r_create.status_code == 200
    res_id = r_create.json()["id"]

    # Delete resource
    r_del = client.delete(f"/api/v1/admin/resources/{res_id}", headers=admin_headers)
    assert r_del.status_code == 200

    # Feedback templates
    tpl_res = client.get("/api/v1/admin/feedback-templates", headers=admin_headers)
    assert tpl_res.status_code == 200
    assert isinstance(tpl_res.json(), list)

def test_admin_sessions_and_reports(admin_headers):
    # Sessions
    sess_res = client.get("/api/v1/admin/sessions", headers=admin_headers)
    assert sess_res.status_code == 200
    assert len(sess_res.json()) >= 1

    # Reports
    rep_res = client.get("/api/v1/admin/reports", headers=admin_headers)
    assert rep_res.status_code == 200
    assert len(rep_res.json()) >= 1

def test_admin_notifications_broadcast(admin_headers):
    payload = {
        "title": "Platform Announcement Test",
        "message": "System will undergo maintenance at midnight.",
        "type": "maintenance"
    }
    res = client.post("/api/v1/admin/notifications", json=payload, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["message"] == "Notification dispatched"

def test_admin_monitoring_and_security(admin_headers):
    # Monitoring telemetry
    mon_res = client.get("/api/v1/admin/monitoring", headers=admin_headers)
    assert mon_res.status_code == 200
    assert mon_res.json()["server"] == "Online"
    assert "storage" in mon_res.json()

    # Audit logs
    logs_res = client.get("/api/v1/admin/logs", headers=admin_headers)
    assert logs_res.status_code == 200
    assert isinstance(logs_res.json(), list)

    # Login history
    lh_res = client.get("/api/v1/admin/security/login-history", headers=admin_headers)
    assert lh_res.status_code == 200
    assert isinstance(lh_res.json(), list)

    # Security settings
    sec_payload = {"max_duration": 45, "max_questions": 10, "maintenance_mode": False}
    sec_res = client.put("/api/v1/admin/security/settings", json=sec_payload, headers=admin_headers)
    assert sec_res.status_code == 200
    assert sec_res.json()["settings"]["max_duration"] == 45

    # Backup generation
    bk_res = client.post("/api/v1/admin/backup", headers=admin_headers)
    assert bk_res.status_code == 200
    assert "filename" in bk_res.json()

    # Backups list
    bks_res = client.get("/api/v1/admin/backups", headers=admin_headers)
    assert bks_res.status_code == 200
    assert len(bks_res.json()) >= 1
    new_bk_id = bk_res.json()["id"]

    # Test Restore Endpoint using freshly created backup
    restore_res = client.post(f"/api/v1/admin/restore/{new_bk_id}", headers=admin_headers)
    assert restore_res.status_code == 200
    assert "restored" in restore_res.json()["message"].lower()

def test_admin_upload_set_csv(admin_headers):
    csv_content = """text,role,category,difficulty,keywords,sample_answer
"Explain how database connection pooling operates.","Backend Developer","Technical","Intermediate","connections;pool;thread;latency","Connection pooling maintains active DB connections for reuse."
"""
    files = {"file": ("test_set.csv", csv_content.encode("utf-8"), "text/csv")}
    res = client.post("/api/v1/admin/questions/upload-set", files=files, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["count"] >= 1

def test_admin_maintenance_mode(admin_headers):
    # Enable maintenance
    put_res = client.put("/api/v1/admin/settings/maintenance", json={"maintenance_mode": True, "message": "Scheduled upgrades"}, headers=admin_headers)
    assert put_res.status_code == 200
    assert put_res.json()["maintenance_mode"] is True

    # Check maintenance
    get_res = client.get("/api/v1/admin/settings/maintenance", headers=admin_headers)
    assert get_res.status_code == 200
    assert get_res.json()["maintenance_mode"] is True

    # Disable maintenance
    reset_res = client.put("/api/v1/admin/settings/maintenance", json={"maintenance_mode": False}, headers=admin_headers)
    assert reset_res.status_code == 200
    assert reset_res.json()["maintenance_mode"] is False

