import time
import signal
import sys
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models.system import ProcessingJob
from app.db.models.interview import InterviewSession
from app.workers.pipeline import pipeline_worker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [AI-Worker] %(message)s"
)
logger = logging.getLogger("ai_worker")

running = True

def handle_exit(sig, frame):
    global running
    logger.info("Received termination signal, shutting down worker gracefully...")
    running = False

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


def process_single_job(job_id: str) -> None:
    db: Session = SessionLocal()
    start_time = time.time()
    try:
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        if not job or job.status != "running":
            return

        logger.info(f"Executing pipeline for Session {job.session_id} (Job {job.id})...")
        pipeline_worker.process_session(job.session_id, db)

        # Mark job as completed
        job.status = "done"
        job.finished_at = datetime.utcnow()
        job.duration_ms = int((time.time() - start_time) * 1000)
        job.error = None
        db.commit()
        logger.info(f"Successfully finished Job {job.id} for Session {job.session_id} in {job.duration_ms}ms")

    except Exception as e:
        logger.error(f"Error processing Job {job_id}: {e}", exc_info=True)
        try:
            db.rollback()
            job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
            if job:
                job.status = "failed"
                job.finished_at = datetime.utcnow()
                job.duration_ms = int((time.time() - start_time) * 1000)
                job.error = str(e)
                job.attempts += 1
                db.commit()
        except Exception as inner_e:
            logger.error(f"Failed to record job failure in DB: {inner_e}")
    finally:
        db.close()


def claim_next_job(db: Session) -> str | None:
    """Claims one queued job using SELECT ... FOR UPDATE SKIP LOCKED on PostgreSQL."""
    is_postgres = "postgresql" in settings.DATABASE_URL.lower()
    try:
        if is_postgres:
            stmt = (
                select(ProcessingJob)
                .where(ProcessingJob.status == "queued")
                .order_by(ProcessingJob.created_at.asc())
                .with_for_update(skip_locked=True)
                .limit(1)
            )
            job = db.execute(stmt).scalars().first()
        else:
            # SQLite fallback for local test/dev
            job = (
                db.query(ProcessingJob)
                .filter(ProcessingJob.status == "queued")
                .order_by(ProcessingJob.created_at.asc())
                .first()
            )

        if job:
            job.status = "running"
            job.started_at = datetime.utcnow()
            job.attempts += 1
            db.commit()
            return job.id
    except Exception as e:
        logger.error(f"Error claiming job: {e}")
        db.rollback()
    return None


def run_worker_loop():
    logger.info("=" * 60)
    logger.info("AI Mock Interview - Background AI Processing Worker Started")
    logger.info(f"Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'local'}")
    logger.info(f"Concurrency: {settings.WORKER_CONCURRENCY} worker threads")
    logger.info("=" * 60)

    executor = ThreadPoolExecutor(max_workers=settings.WORKER_CONCURRENCY)

    while running:
        db = SessionLocal()
        job_id = None
        try:
            job_id = claim_next_job(db)
        finally:
            db.close()

        if job_id:
            executor.submit(process_single_job, job_id)
        else:
            time.sleep(1.5)

    logger.info("Shutting down worker thread pool...")
    executor.shutdown(wait=True)
    logger.info("AI Worker stopped.")


if __name__ == "__main__":
    run_worker_loop()
