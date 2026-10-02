import os
import pytest
from app.db.session import SessionLocal
from app.db.models.system import Backup, SystemSetting
from app.services.backup_service import backup_service
from app.core.config import settings

def test_backup_creation_and_tracking():
    db = SessionLocal()
    bk = None
    try:
        # Create a backup
        bk = backup_service.create_backup(db, backup_type="full")
        assert bk is not None
        assert bk.id is not None
        assert os.path.exists(bk.file_path)
        assert bk.size_bytes > 0
        assert bk.status == "completed"

        # Verify query in backups table
        db_record = db.query(Backup).filter(Backup.id == bk.id).first()
        assert db_record is not None
        assert db_record.filename == bk.filename
    finally:
        db.close()

    # Verify restore logic with a clean session
    db_restore = SessionLocal()
    try:
        restore_result = backup_service.restore_backup(db_restore, bk.id)
        assert "restored successfully" in restore_result["message"].lower()
    finally:
        db_restore.close()

def test_retention_policy_enforcement():
    db = SessionLocal()
    try:
        from datetime import datetime, timedelta
        # Insert a simulated old backup record
        old_time = datetime.utcnow() - timedelta(days=30)
        old_file = os.path.join(settings.STORAGE_DIR, "backups", "old_test_backup.sqlite")
        with open(old_file, "w") as f:
            f.write("-- Test old backup")

        old_bk = Backup(
            filename="old_test_backup.sqlite",
            file_path=old_file,
            size_bytes=18,
            backup_type="full",
            status="completed",
            created_at=old_time
        )
        db.add(old_bk)
        db.commit()
        db.refresh(old_bk)
        old_id = old_bk.id

        # Apply retention policy
        backup_service.apply_retention_policy(db)

        # Confirm old backup record and file are removed
        check = db.query(Backup).filter(Backup.id == old_id).first()
        assert check is None
        assert not os.path.exists(old_file)

    finally:
        db.close()
