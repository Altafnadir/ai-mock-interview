import os
import sys

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.models.system import ActivityLog, ErrorLog
from app.services.activity_logger import log_activity, log_error

def test_logs():
    print("=" * 80)
    print("TASK 7: ACTIVITY_LOGS AND ERROR_LOGS VERIFICATION")
    print("=" * 80)

    with SessionLocal() as db:
        initial_activity_count = db.query(ActivityLog).count()
        initial_error_count = db.query(ErrorLog).count()
        print(f"Initial activity_logs row count: {initial_activity_count}")
        print(f"Initial error_logs row count:    {initial_error_count}")

        # 1. Test direct activity log
        log_activity(
            db=db,
            action="login_success",
            entity="user",
            user_id="test-user-1",
            ip_address="127.0.0.1",
            metadata_info={"email": "candidate@example.com"}
        )
        log_activity(
            db=db,
            action="interview_start",
            entity="interview_session",
            entity_id="session-test-1",
            user_id="test-user-1",
            metadata_info={"role": "Full Stack"}
        )
        log_activity(
            db=db,
            action="resume_upload",
            entity="resume",
            entity_id="res-1",
            user_id="test-user-1",
            metadata_info={"filename": "resume.pdf"}
        )
        log_activity(
            db=db,
            action="report_generation",
            entity="report",
            entity_id="rep-1",
            user_id="test-user-1",
            metadata_info={"score": 88.5}
        )
        log_activity(
            db=db,
            action="admin_maintenance_update",
            entity="system_setting",
            user_id="admin-1",
            metadata_info={"enabled": False}
        )

        # 2. Test error log
        log_error(
            db=db,
            error_type="PipelineFailure",
            message="Test simulated pipeline timeout error",
            endpoint="/workers/pipeline/simulated-1",
            method="WORKER",
            stack_trace="Traceback (simulated):\n  File pipeline.py, line 42, in process_session\nTimeoutError: audio normalization timeout"
        )

        # 3. Test through FastAPI TestClient endpoint
        client = TestClient(app)
        # Hit invalid endpoint to verify 404 or trigger error
        resp = client.get("/api/v1/auth/me") # 401 unauth
        print(f"Auth test response: {resp.status_code}")

        # Check counts again
        final_activity_count = db.query(ActivityLog).count()
        final_error_count = db.query(ErrorLog).count()

        print("-" * 80)
        print(f"Final activity_logs row count: {final_activity_count} (+{final_activity_count - initial_activity_count})")
        print(f"Final error_logs row count:    {final_error_count} (+{final_error_count - initial_error_count})")
        print("-" * 80)

        # Print top 5 activity logs
        print("Recent Activity Logs:")
        for log in db.query(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(5).all():
            print(f"  [{log.created_at}] Action: {log.action:<25} Entity: {log.entity:<18} IP: {log.ip_address}")

        # Print top error logs
        print("\nRecent Error Logs:")
        for err in db.query(ErrorLog).order_by(ErrorLog.created_at.desc()).limit(3).all():
            print(f"  [{err.created_at}] Type: {err.error_type:<20} Method: {err.method} Path: {err.endpoint} Msg: {err.message[:50]}")

    print("=" * 80)
    assert final_activity_count > 0, "activity_logs must have rows"
    assert final_error_count > 0, "error_logs must have rows"
    print("VERIFICATION SUCCESSFUL: Both activity_logs and error_logs are populated and queryable!")

if __name__ == "__main__":
    test_logs()
