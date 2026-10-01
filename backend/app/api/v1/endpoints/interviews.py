import os
from datetime import datetime
from typing import List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db, SessionLocal
from app.db.models.user import User
from app.db.models.resume import Resume
from app.db.models.interview import (
    InterviewSession, SessionQuestion, Answer,
    JobRole, InterviewCategory, DifficultyLevel
)
from app.schemas.interview import (
    InterviewCreateRequest, InterviewSessionResponse,
    InterviewSessionDetailResponse, SessionQuestionResponse,
    AnswerSubmitRequest, AnswerResponse,
    InterviewProgressResponse, InterviewStatusResponse
)
from app.ai.question_generator import question_generator
from app.services.storage import storage_service
from app.workers.pipeline import pipeline_worker

def run_pipeline_task(session_id: str):
    db = SessionLocal()
    try:
        pipeline_worker.process_session(session_id, db)
    finally:
        db.close()

router = APIRouter()

@router.post("", response_model=InterviewSessionDetailResponse, status_code=status.HTTP_201_CREATED)
def create_interview_session(
    payload: InterviewCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create a new mock interview session with pre-generated tailored questions."""
    job_role = db.query(JobRole).filter(JobRole.id == payload.job_role_id).first()
    if not job_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job role not found")

    category = db.query(InterviewCategory).filter(InterviewCategory.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview category not found")

    difficulty = db.query(DifficultyLevel).filter(DifficultyLevel.id == payload.difficulty_id).first()
    if not difficulty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Difficulty level not found")

    resume_context = None
    if payload.resume_id:
        resume = db.query(Resume).filter(Resume.id == payload.resume_id, Resume.user_id == current_user.id).first()
        if resume and resume.analysis:
            resume_context = {
                "extracted_skills": resume.analysis.extracted_skills,
                "extracted_projects": resume.analysis.extracted_projects,
                "extracted_experience": resume.analysis.extracted_experience,
            }

    # Determine question count
    q_count = payload.num_questions if (payload.num_questions and 1 <= payload.num_questions <= 15) else payload.total_questions

    # Create session
    session = InterviewSession(
        user_id=current_user.id,
        resume_id=payload.resume_id,
        job_role_id=payload.job_role_id,
        category_id=payload.category_id,
        difficulty_id=payload.difficulty_id,
        status="created",
        total_questions=q_count
    )
    db.add(session)
    db.flush()

    # Generate questions
    generated_questions = question_generator.generate_session_questions(
        db=db,
        job_role=job_role,
        category=category,
        difficulty=difficulty,
        total_questions=q_count,
        resume_context=resume_context
    )

    for q_data in generated_questions:
        sq = SessionQuestion(
            session_id=session.id,
            order_index=q_data["order_index"],
            question_text=q_data["question_text"],
            source=q_data.get("source", "bank"),
            time_limit_seconds=q_data.get("time_limit_seconds", 120),
            status="pending"
        )
        db.add(sq)

    db.commit()
    db.refresh(session)
    return session

@router.get("", response_model=List[InterviewSessionResponse])
def get_user_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve interview session history for the authenticated candidate."""
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(InterviewSession.created_at.desc()).all()
    return sessions

@router.get("/{session_id}", response_model=InterviewSessionDetailResponse)
def get_interview_detail(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve full details of an interview session, including questions and answers."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return session

@router.post("/{session_id}/start", response_model=InterviewSessionDetailResponse)
def start_interview(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Begin interview session and activate the first question."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    now = datetime.utcnow()
    if session.status == "created":
        session.status = "in_progress"
        session.started_at = now

    first_q = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session.id,
        SessionQuestion.status == "pending"
    ).order_by(SessionQuestion.order_index).first()

    if first_q and not first_q.started_at:
        first_q.started_at = now

    db.commit()
    db.refresh(session)
    return session

@router.get("/{session_id}/current", response_model=Optional[SessionQuestionResponse])
@router.get("/{session_id}/questions/current", response_model=Optional[SessionQuestionResponse])
def get_current_question(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve the currently active pending question for this session."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    current_q = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session.id,
        SessionQuestion.status == "pending"
    ).order_by(SessionQuestion.order_index).first()

    if current_q and not current_q.started_at:
        current_q.started_at = datetime.utcnow()
        db.commit()
        db.refresh(current_q)

    return current_q

@router.post("/{session_id}/answer", response_model=SessionQuestionResponse)
@router.post("/{session_id}/questions/{question_id}/answer", response_model=SessionQuestionResponse)
def submit_answer(
    session_id: str,
    payload: Optional[AnswerSubmitRequest] = None,
    question_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Submit candidate's answer for the current question."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if question_id:
        current_q = db.query(SessionQuestion).filter(
            SessionQuestion.id == question_id,
            SessionQuestion.session_id == session.id
        ).first()
    else:
        current_q = db.query(SessionQuestion).filter(
            SessionQuestion.session_id == session.id,
            SessionQuestion.status == "pending"
        ).order_by(SessionQuestion.order_index).first()

    if not current_q:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No pending question to answer")

    now = datetime.utcnow()
    current_q.status = "answered"
    current_q.ended_at = now

    transcript = (payload.transcript if payload else "") or ""
    words = transcript.strip().split()
    word_count = len(words)
    duration = payload.duration_seconds if (payload and payload.duration_seconds and payload.duration_seconds > 0) else 30.0
    wpm = round((word_count / max(duration / 60.0, 0.1)), 1)

    # Basic filler detection for immediate feedback
    common_fillers = ["um", "uh", "like", "you know", "actually", "basically", "so", "right", "i mean"]
    t_lower = transcript.lower()
    filler_breakdown = {}
    total_fillers = 0
    for filler in common_fillers:
        cnt = t_lower.count(filler)
        if cnt > 0:
            filler_breakdown[filler] = cnt
            total_fillers += cnt

    ans = Answer(
        session_question_id=current_q.id,
        transcript=transcript,
        word_count=word_count,
        duration_seconds=duration,
        filler_word_count=total_fillers,
        filler_words_breakdown=filler_breakdown,
        speaking_rate_wpm=wpm
    )
    db.add(ans)

    # Activate next question timestamp if present
    next_q = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session.id,
        SessionQuestion.status == "pending"
    ).order_by(SessionQuestion.order_index).first()

    if next_q:
        next_q.started_at = now

    db.commit()
    db.refresh(current_q)
    return current_q

@router.post("/{session_id}/skip", response_model=SessionQuestionResponse)
@router.post("/{session_id}/questions/{question_id}/skip", response_model=SessionQuestionResponse)
def skip_question(
    session_id: str,
    question_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Skip the current question and advance to the next."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if question_id:
        current_q = db.query(SessionQuestion).filter(
            SessionQuestion.id == question_id,
            SessionQuestion.session_id == session.id
        ).first()
    else:
        current_q = db.query(SessionQuestion).filter(
            SessionQuestion.session_id == session.id,
            SessionQuestion.status == "pending"
        ).order_by(SessionQuestion.order_index).first()

    if not current_q:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active question to skip")

    now = datetime.utcnow()
    current_q.status = "skipped"
    current_q.ended_at = now

    # Activate next question
    next_q = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session.id,
        SessionQuestion.status == "pending",
        SessionQuestion.id != current_q.id
    ).order_by(SessionQuestion.order_index).first()

    if next_q:
        next_q.started_at = now

    db.commit()
    db.refresh(current_q)
    return current_q

@router.post("/{session_id}/repeat")
@router.post("/{session_id}/questions/{question_id}/repeat")
def repeat_question(
    session_id: str,
    question_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Return the active question text for replay."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    if question_id:
        current_q = db.query(SessionQuestion).filter(
            SessionQuestion.id == question_id,
            SessionQuestion.session_id == session.id
        ).first()
    else:
        current_q = db.query(SessionQuestion).filter(
            SessionQuestion.session_id == session.id,
            SessionQuestion.status == "pending"
        ).order_by(SessionQuestion.order_index).first()

    if not current_q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active question found")

    return {
        "question_id": current_q.id,
        "question_text": current_q.question_text,
        "order_index": current_q.order_index,
        "time_limit_seconds": current_q.time_limit_seconds
    }

@router.get("/{session_id}/progress", response_model=InterviewProgressResponse)
def get_progress(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get candidate's progress and elapsed time for the interview session."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    questions = db.query(SessionQuestion).filter(SessionQuestion.session_id == session.id).order_by(SessionQuestion.order_index).all()
    total_q = len(questions)
    answered_q = sum(1 for q in questions if q.status in ["answered", "skipped"])

    pending_idx = 1
    for q in questions:
        if q.status == "pending":
            pending_idx = q.order_index
            break
        elif q.status in ["answered", "skipped"]:
            pending_idx = q.order_index + 1

    elapsed = 0
    if session.started_at:
        end_time = session.ended_at or datetime.utcnow()
        elapsed = int((end_time - session.started_at).total_seconds())

    return {
        "session_id": session.id,
        "status": session.status,
        "total_questions": total_q,
        "answered_questions": answered_q,
        "current_index": min(pending_idx, total_q),
        "elapsed_seconds": max(elapsed, 0),
        "is_completed": session.status in ["completed", "analyzed", "processing"]
    }

@router.post("/{session_id}/end", response_model=InterviewSessionResponse)
def end_interview(
    session_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """End interview session, calculate final duration, and queue AI analysis pipeline."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    now = datetime.utcnow()
    session.ended_at = now
    if session.started_at:
        session.duration_seconds = int((now - session.started_at).total_seconds())

    session.status = "completed"
    db.commit()
    db.refresh(session)

    # Queue background analysis pipeline
    background_tasks.add_task(run_pipeline_task, session.id)

    return session

@router.post("/{session_id}/process", response_model=InterviewSessionResponse)
def process_interview_manually(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Synchronously triggers or re-runs the AI analysis pipeline on an interview session."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    pipeline_worker.process_session(session.id, db)
    db.refresh(session)
    return session

@router.get("/{session_id}/status", response_model=InterviewStatusResponse)
def get_interview_status(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Check AI pipeline processing status for this session."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    progress_map = {
        "created": (10, "Interview configured"),
        "in_progress": (30, "Interview in progress"),
        "completed": (50, "Recording submitted"),
        "processing": (75, "AI analysis in progress"),
        "analyzed": (100, "Comprehensive report ready"),
        "failed": (0, "Analysis failed"),
    }

    pct, step = progress_map.get(session.status, (0, session.status))

    return {
        "session_id": session.id,
        "status": session.status,
        "processing_step": step,
        "progress_percentage": pct,
        "error": session.processing_error
    }
