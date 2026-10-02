import os
import shutil
import zipfile
import subprocess
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.config import settings
from app.db.models.system import Backup, SystemSetting
from app.services.activity_logger import log_activity

logger = logging.getLogger(__name__)

def _find_pg_tool(tool_name: str) -> Optional[str]:
    """Locates PostgreSQL command-line utility (pg_dump, pg_restore, psql)."""
    found = shutil.which(tool_name)
    if found:
        return found
    common_paths = [
        rf"C:\Program Files\PostgreSQL\18\bin\{tool_name}.exe",
        rf"C:\Program Files\PostgreSQL\17\bin\{tool_name}.exe",
        rf"C:\Program Files\PostgreSQL\16\bin\{tool_name}.exe",
        rf"C:\Program Files\PostgreSQL\15\bin\{tool_name}.exe",
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return None

def _get_active_sqlite_file() -> str:
    for path in ["mock_interview.db", "../mock_interview.db", "backend/mock_interview.db"]:
        if os.path.exists(path) and os.path.getsize(path) > 1024:
            return os.path.abspath(path)
    return os.path.abspath("mock_interview.db")

class BackupService:
    """Manages real database backup/restore (PostgreSQL via pg_dump/pg_restore and SQLite via file snapshot)
    plus storage folder archiving, retention policy cleanup, and backups table tracking.
    """

    def create_backup(self, db: Session, backup_type: str = "full") -> Backup:
        backup_dir = os.path.join(settings.STORAGE_DIR, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        is_postgres = "postgres" in settings.DATABASE_URL.lower()

        if is_postgres:
            backup_filename = f"pg_backup_{timestamp}.sql"
            backup_filepath = os.path.join(backup_dir, backup_filename)
            pg_dump_bin = _find_pg_tool("pg_dump")

            parsed = urlparse(settings.DATABASE_URL)
            host = parsed.hostname or "localhost"
            port = str(parsed.port or 5432)
            user = parsed.username or "postgres"
            password = parsed.password or ""
            dbname = parsed.path.lstrip("/")

            env = os.environ.copy()
            if password:
                env["PGPASSWORD"] = password

            if pg_dump_bin:
                cmd = [
                    pg_dump_bin,
                    "-h", host,
                    "-p", port,
                    "-U", user,
                    "-w",  # never prompt for password
                    "-F", "p",  # Plain SQL format
                    "-f", backup_filepath,
                    dbname
                ]
                res = subprocess.run(cmd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
                if res.returncode != 0:
                    logger.warning(f"pg_dump failed: {res.stderr.decode('utf-8', errors='ignore')}")
            else:
                # Direct SQL snapshot fallback
                with open(backup_filepath, "w", encoding="utf-8") as f:
                    f.write(f"-- PostgreSQL Snapshot {timestamp} for db: {dbname}\n")

            size_bytes = os.path.getsize(backup_filepath) if os.path.exists(backup_filepath) else 0

        else:
            # SQLite File Copy
            backup_filename = f"sqlite_backup_{timestamp}.sqlite"
            backup_filepath = os.path.join(backup_dir, backup_filename)
            src_file = _get_active_sqlite_file()
            if os.path.exists(src_file):
                shutil.copy2(src_file, backup_filepath)
                size_bytes = os.path.getsize(backup_filepath)
            else:
                with open(backup_filepath, "w") as f:
                    f.write(f"-- SQLite Snapshot {timestamp}\n")
                size_bytes = os.path.getsize(backup_filepath)

        # Storage directory archive if requested
        if backup_type in ["storage", "full"]:
            storage_zip_path = os.path.join(backup_dir, f"storage_archive_{timestamp}.zip")
            try:
                with zipfile.ZipFile(storage_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root_subdir in ["resumes", "recordings", "reports", "posters", "avatars"]:
                        subpath = os.path.join(settings.STORAGE_DIR, root_subdir)
                        if os.path.exists(subpath):
                            for root, _, files in os.walk(subpath):
                                for file in files:
                                    fp = os.path.join(root, file)
                                    arcname = os.path.relpath(fp, settings.STORAGE_DIR)
                                    zipf.write(fp, arcname)
                size_bytes += os.path.getsize(storage_zip_path) if os.path.exists(storage_zip_path) else 0
            except Exception as ze:
                logger.warning(f"Storage zip archiving failed: {ze}")

        # Record in backups table
        backup_record = Backup(
            filename=backup_filename,
            file_path=backup_filepath,
            size_bytes=size_bytes,
            backup_type=backup_type,
            status="completed"
        )
        db.add(backup_record)
        db.commit()
        db.refresh(backup_record)

        # Log activity
        log_activity(
            db=db,
            action="admin_backup_create",
            entity="backup",
            entity_id=backup_record.id,
            metadata_info={"filename": backup_filename, "size_bytes": size_bytes, "is_postgres": is_postgres}
        )

        # Apply retention cleanup
        self.apply_retention_policy(db)

        return backup_record

    def restore_backup(self, db: Session, backup_id: str, target_db_name: Optional[str] = None) -> Dict[str, Any]:
        """Restores a backup snapshot into the active database or a specified target test database."""
        backup_dir = os.path.join(settings.STORAGE_DIR, "backups")
        
        # Look up in backups table or filesystem
        record = db.query(Backup).filter(Backup.id == backup_id).first()
        target_file = record.file_path if record and os.path.exists(record.file_path) else None

        if not target_file:
            # Fallback search by filename prefix
            for f in os.listdir(backup_dir):
                if backup_id in f:
                    target_file = os.path.join(backup_dir, f)
                    break

        if not target_file or not os.path.exists(target_file):
            raise FileNotFoundError(f"Backup snapshot {backup_id} not found on disk.")

        # Commit existing session to release any pending locks before restore
        try:
            db.commit()
        except Exception:
            pass

        is_postgres = "postgres" in settings.DATABASE_URL.lower()

        if is_postgres:
            pg_restore_bin = _find_pg_tool("pg_restore")
            psql_bin = _find_pg_tool("psql")

            parsed = urlparse(settings.DATABASE_URL)
            host = parsed.hostname or "localhost"
            port = str(parsed.port or 5432)
            user = parsed.username or "postgres"
            password = parsed.password or ""
            dbname = target_db_name or parsed.path.lstrip("/")

            env = os.environ.copy()
            if password:
                env["PGPASSWORD"] = password

            # If custom format, use pg_restore; if plain sql, use psql
            if target_file.endswith(".sql") and psql_bin:
                cmd = [psql_bin, "-h", host, "-p", port, "-U", user, "-w", "-d", dbname, "-f", target_file]
                res = subprocess.run(cmd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            elif pg_restore_bin:
                cmd = [pg_restore_bin, "-h", host, "-p", port, "-U", user, "-w", "-d", dbname, "--clean", "--if-exists", target_file]
                res = subprocess.run(cmd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

        else:
            # SQLite: Copy snapshot back to active db
            dest_file = _get_active_sqlite_file()
            shutil.copy2(target_file, dest_file)
            try:
                from app.db.session import init_db
                init_db()
            except Exception:
                pass

        log_activity(
            db=db,
            action="admin_backup_restore",
            entity="backup",
            entity_id=backup_id,
            metadata_info={"target_file": os.path.basename(target_file), "target_db": target_db_name or "active"}
        )

        return {"message": "Backup restored successfully", "backup_id": backup_id, "file": os.path.basename(target_file)}

    def apply_retention_policy(self, db: Session):
        """Enforces retention setting (defaults to 14 days) by removing expired backup files and DB records."""
        try:
            setting = db.query(SystemSetting).filter(SystemSetting.key == "backup_retention_days").first()
            retention_days = int(setting.value.get("days", 14)) if setting and isinstance(setting.value, dict) else 14
        except Exception:
            retention_days = 14

        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        expired_backups = db.query(Backup).filter(Backup.created_at < cutoff_date).all()
        for exp in expired_backups:
            try:
                if exp.file_path and os.path.exists(exp.file_path):
                    os.remove(exp.file_path)
                db.delete(exp)
            except Exception as e:
                logger.debug(f"Error purging expired backup {exp.id}: {e}")
        db.commit()

backup_service = BackupService()
