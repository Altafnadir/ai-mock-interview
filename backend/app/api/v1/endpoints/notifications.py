from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.system import Notification
from app.schemas.resource import NotificationResponse

router = APIRouter()

@router.get("", response_model=List[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve notifications and system announcements for the current user."""
    notifs = db.query(Notification).filter(
        or_(
            Notification.user_id == current_user.id,
            Notification.user_id == None
        )
    ).order_by(Notification.created_at.desc()).limit(50).all()

    return notifs

@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get total count of unread notifications for badge indicator."""
    count = db.query(Notification).filter(
        or_(
            Notification.user_id == current_user.id,
            Notification.user_id == None
        ),
        Notification.is_read == False
    ).count()

    return {"unread_count": count}

def _mark_as_read(notification_id: str, db: Session, user_id: str):
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        or_(
            Notification.user_id == user_id,
            Notification.user_id == None
        )
    ).first()

    if not notif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif

@router.put("/{notification_id}/read", response_model=NotificationResponse)
@router.post("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Mark a specific notification as read (supports PUT and POST)."""
    return _mark_as_read(notification_id, db, current_user.id)

def _mark_all_read(db: Session, user_id: str):
    db.query(Notification).filter(
        or_(
            Notification.user_id == user_id,
            Notification.user_id == None
        ),
        Notification.is_read == False
    ).update({"is_read": True}, synchronize_session=False)
    db.commit()
    return {"message": "All notifications marked as read"}

@router.put("/read-all")
@router.post("/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Mark all notifications as read for current user."""
    return _mark_all_read(db, current_user.id)
