import os
import shutil
import logging
from datetime import datetime, timedelta
from typing import Optional

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.system import Notification, SystemSetting
from app.db.models.interview import InterviewSession

logger = logging.getLogger(__name__)

scheduler = None

def run_auto_backup_job():
    """Daily automated snapshot of database and critical storage."""
    logger.info("Executing scheduled daily database & storage backup job...")
    db = SessionLocal()
    try:
        from app.services.backup_service import backup_service
        backup_record = backup_service.create_backup(db, backup_type="full")
        logger.info(f"Scheduled backup saved to {backup_record.file_path} (size: {backup_record.size_bytes} bytes)")
    except Exception as e:
        logger.warning(f"Error in scheduled auto backup job: {e}")
    finally:
        db.close()


def run_candidate_reminders_job():
    """Creates improvement reminders and practice opportunity notifications for candidates."""
    logger.info("Executing scheduled candidate practice opportunity reminder job...")
    db = SessionLocal()
    try:
        candidates = db.query(User).filter(User.role == "candidate", User.is_active == True).all()
        now = datetime.utcnow()
        three_days_ago = now - timedelta(days=3)

        for candidate in candidates:
            # Check last interview
            last_sess = (
                db.query(InterviewSession)
                .filter(InterviewSession.user_id == candidate.id)
                .order_by(InterviewSession.created_at.desc())
                .first()
            )

            needs_reminder = False
            if not last_sess:
                needs_reminder = True
            elif last_sess.created_at < three_days_ago:
                needs_reminder = True

            if needs_reminder:
                # Avoid duplicate reminder within 48 hours
                existing = (
                    db.query(Notification)
                    .filter(
                        Notification.user_id == candidate.id,
                        Notification.type == "improvement_reminder",
                        Notification.created_at >= now - timedelta(days=2)
                    )
                    .first()
                )
                if not existing:
                    notif = Notification(
                        user_id=candidate.id,
                        title="Ready for another practice round?",
                        message="Consistent mock interviews build unshakeable confidence. Schedule a 15-minute mock session today to level up your verbal delivery and technical depth.",
                        type="improvement_reminder",
                        is_read=False
                    )
                    db.add(notif)
                    logger.info(f"Dispatched improvement reminder to candidate {candidate.email}")

        db.commit()
    except Exception as e:
        logger.warning(f"Error executing reminder job: {e}")
        db.rollback()
    finally:
        db.close()


def start_scheduler():
    """Initializes and starts the APScheduler background thread."""
    global scheduler
    import sys
    if "pytest" in sys.modules:
        logger.info("Pytest active; skipping background APScheduler thread.")
        return

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger

        scheduler = BackgroundScheduler()
        # Daily backup at 02:00 UTC
        scheduler.add_job(run_auto_backup_job, CronTrigger(hour=2, minute=0), id="daily_backup", replace_existing=True)
        # Daily practice reminders at 10:00 UTC
        scheduler.add_job(run_candidate_reminders_job, CronTrigger(hour=10, minute=0), id="practice_reminders", replace_existing=True)

        scheduler.start()
        logger.info("APScheduler initialized: daily backups & candidate practice reminders active.")
    except Exception as e:
        logger.warning(f"Could not start APScheduler: {e}")


def shutdown_scheduler():
    global scheduler
    if scheduler and scheduler.running:
        try:
            scheduler.shutdown(wait=False)
            logger.info("APScheduler stopped.")
        except Exception:
            pass
