import os
import uuid
from datetime import datetime, timedelta
from typing import Any, List
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.interview import InterviewSession
from app.db.models.report import Report, ReportShare, Recommendation
from app.schemas.report import ReportResponse, ReportShareResponse
from app.workers.pipeline import pipeline_worker
from app.services.storage import storage_service

router = APIRouter()

@router.get("/public/{token}", response_model=ReportResponse)
def get_public_report(
    token: str,
    db: Session = Depends(get_db)
) -> Any:
    """Public endpoint to view a candidate's shared interview verification report."""
    share = db.query(ReportShare).filter(
        ReportShare.token == token,
        ReportShare.is_revoked == False
    ).first()

    if not share:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shared report not found or link revoked")

    if share.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="This shared report link has expired")

    report = share.report
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report data unavailable")

    return report

@router.get("/public/{token}/pdf")
def download_public_report_pdf(
    token: str,
    db: Session = Depends(get_db)
) -> Any:
    """Public endpoint to download PDF report via shared token."""
    share = db.query(ReportShare).filter(
        ReportShare.token == token,
        ReportShare.is_revoked == False
    ).first()

    if not share or share.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid or expired share link")

    report = share.report
    if not report or not report.pdf_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF report not found")

    abs_path = storage_service.get_absolute_path(report.pdf_path)
    if not abs_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF file missing from storage")

    return FileResponse(
        path=str(abs_path),
        media_type="application/pdf",
        filename=f"GIMS_Interview_Report_{share.report_id[:8]}.pdf"
    )

@router.get("/{session_id}", response_model=ReportResponse)
def get_session_report(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve full evaluation report for an interview session."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    report = db.query(Report).filter(Report.session_id == session.id).first()
    if not report:
        # If session has answers, auto-process pipeline to generate report
        try:
            pipeline_worker.process_session(session.id, db)
            report = db.query(Report).filter(Report.session_id == session.id).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Report is not ready yet: {e}"
            )

    return report

@router.get("/{session_id}/pdf")
def download_session_report_pdf(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Download the official ReportLab PDF evaluation report."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    report = db.query(Report).filter(Report.session_id == session.id).first()
    if not report or not report.pdf_path:
        # Trigger pipeline if needed
        pipeline_worker.process_session(session.id, db)
        report = db.query(Report).filter(Report.session_id == session.id).first()

    if not report or not report.pdf_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF report could not be generated")

    abs_path = storage_service.get_absolute_path(report.pdf_path)
    if not abs_path.exists():
        # Re-generate PDF
        pipeline_worker.process_session(session.id, db)
        report = db.query(Report).filter(Report.session_id == session.id).first()
        abs_path = storage_service.get_absolute_path(report.pdf_path)

    return FileResponse(
        path=str(abs_path),
        media_type="application/pdf",
        filename=f"Mock_Interview_Report_{session.id[:8]}.pdf"
    )

@router.post("/{session_id}/share", response_model=ReportShareResponse)
def create_report_share_link(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Generate secure public share link for candidate's interview report."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    report = db.query(Report).filter(Report.session_id == session.id).first()
    if not report:
        pipeline_worker.process_session(session.id, db)
        report = db.query(Report).filter(Report.session_id == session.id).first()

    # Check existing active share
    share = db.query(ReportShare).filter(
        ReportShare.report_id == report.id,
        ReportShare.is_revoked == False,
        ReportShare.expires_at > datetime.utcnow()
    ).first()

    if not share:
        token = str(uuid.uuid4())
        expires = datetime.utcnow() + timedelta(days=30)
        share = ReportShare(
            report_id=report.id,
            token=token,
            expires_at=expires,
            is_revoked=False,
            created_by=current_user.id
        )
        db.add(share)
        db.commit()
        db.refresh(share)

    return {
        "token": share.token,
        "share_url": f"/shared/{share.token}",
        "expires_at": share.expires_at
    }

from app.services.email import send_report_email

@router.post("/{session_id}/email")
def email_session_report(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Send evaluation report summary to candidate's email."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    report = db.query(Report).filter(Report.session_id == session.id).first()
    if not report:
        pipeline_worker.process_session(session.id, db)
        report = db.query(Report).filter(Report.session_id == session.id).first()

    send_report_email(
        to_email=current_user.email,
        candidate_name=current_user.full_name,
        session_id=session.id,
        overall_score=report.overall_score,
        verdict=report.final_verdict,
        pdf_path=report.pdf_path or ""
    )

    return {"message": "Performance report email dispatched successfully"}
