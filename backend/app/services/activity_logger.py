import logging
import traceback
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.db.models.system import ActivityLog, ErrorLog

logger = logging.getLogger(__name__)

def log_activity(
    db: Session,
    action: str,
    entity: str,
    user_id: Optional[str] = None,
    entity_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    metadata_info: Optional[Dict[str, Any]] = None
) -> Optional[ActivityLog]:
    """Records an audit event in activity_logs with exception safety."""
    try:
        log_entry = ActivityLog(
            user_id=user_id,
            action=action,
            entity=entity,
            entity_id=str(entity_id) if entity_id else None,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata_info=metadata_info or {}
        )
        db.add(log_entry)
        db.commit()
        return log_entry
    except Exception as e:
        logger.warning(f"Failed to record activity log ({action} on {entity}): {e}")
        try:
            db.rollback()
        except Exception:
            pass
        return None

def log_error(
    db: Session,
    error_type: str,
    message: str,
    endpoint: Optional[str] = None,
    method: Optional[str] = None,
    stack_trace: Optional[str] = None,
    user_id: Optional[str] = None
) -> Optional[ErrorLog]:
    """Records an unhandled exception or pipeline error in error_logs with exception safety."""
    try:
        err_entry = ErrorLog(
            endpoint=endpoint,
            method=method,
            error_type=error_type,
            message=message[:2000] if message else "Unknown error",
            stack_trace=stack_trace[:4000] if stack_trace else None,
            user_id=user_id
        )
        db.add(err_entry)
        db.commit()
        return err_entry
    except Exception as e:
        logger.warning(f"Failed to record error log ({error_type}): {e}")
        try:
            db.rollback()
        except Exception:
            pass
        return None
