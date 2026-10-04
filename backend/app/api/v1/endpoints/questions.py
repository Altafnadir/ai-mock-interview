from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.db.models.user import User
from app.db.models.resume import Resume
from app.db.models.interview import JobRole, InterviewCategory, DifficultyLevel
from app.schemas.interview import QuestionPreviewRequest, QuestionPreviewResponse, QuestionPreviewItem
from app.ai.question_generator import question_generator

router = APIRouter()

DIFFICULTY_MAP = {
    "easy": "Beginner",
    "beginner": "Beginner",
    "medium": "Intermediate",
    "intermediate": "Intermediate",
    "hard": "Advanced",
    "advanced": "Advanced",
}

CATEGORY_MAP = {
    "technical": "Technical",
    "hr": "HR",
    "behavioral": "Behavioral",
    "mixed": "Mixed",
}

@router.post("/generate-preview", response_model=QuestionPreviewResponse)
def generate_questions_preview(
    payload: QuestionPreviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Generate interview questions preview without creating a session in the database."""
    # Resolve Job Role
    job_role = None
    if payload.job_role_id:
        job_role = db.query(JobRole).filter(JobRole.id == payload.job_role_id).first()
    if not job_role and payload.role:
        job_role = db.query(JobRole).filter(JobRole.name.ilike(f"%{payload.role.strip()}%")).first()
    if not job_role:
        job_role = db.query(JobRole).filter(JobRole.is_active == True).first()
    if not job_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active job roles available")

    # Resolve Interview Category / Type
    category_name = CATEGORY_MAP.get((payload.type or "").strip().lower(), "Technical")
    category = None
    if payload.category_id:
        category = db.query(InterviewCategory).filter(InterviewCategory.id == payload.category_id).first()
    if not category:
        category = db.query(InterviewCategory).filter(InterviewCategory.name.ilike(category_name)).first()
    if not category:
        category = db.query(InterviewCategory).filter(InterviewCategory.is_active == True).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active interview categories available")

    # Resolve Difficulty
    difficulty_target = DIFFICULTY_MAP.get((payload.difficulty or "").strip().lower(), "Intermediate")
    difficulty = None
    if payload.difficulty_id:
        difficulty = db.query(DifficultyLevel).filter(DifficultyLevel.id == payload.difficulty_id).first()
    if not difficulty:
        difficulty = db.query(DifficultyLevel).filter(DifficultyLevel.name.ilike(difficulty_target)).first()
    if not difficulty:
        difficulty = db.query(DifficultyLevel).first()
    if not difficulty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No difficulty levels available")

    # Resume context if provided
    resume_context = None
    if payload.resume_id:
        resume = db.query(Resume).filter(Resume.id == payload.resume_id, Resume.user_id == current_user.id).first()
        if resume and resume.analysis:
            resume_context = {
                "extracted_skills": resume.analysis.extracted_skills,
                "extracted_projects": resume.analysis.extracted_projects,
                "extracted_experience": resume.analysis.extracted_experience,
            }

    count = max(1, min(15, payload.count))

    # Generate questions via QuestionGenerator (Gemini API or Question Bank)
    raw_questions = question_generator.generate_session_questions(
        db=db,
        job_role=job_role,
        category=category,
        difficulty=difficulty,
        total_questions=count,
        resume_context=resume_context
    )

    items: List[QuestionPreviewItem] = []
    for idx, q in enumerate(raw_questions):
        items.append(QuestionPreviewItem(
            order_index=idx + 1,
            question_text=q["question_text"],
            category=category.name,
            difficulty=difficulty.name,
            time_limit_seconds=q.get("time_limit_seconds", 120)
        ))

    return QuestionPreviewResponse(
        questions=items,
        count=len(items),
        role=job_role.name,
        level=payload.level or "2-5 Years",
        type=category.name,
        difficulty=difficulty.name
    )
