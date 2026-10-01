from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.interview import Question, JobRole, InterviewCategory, DifficultyLevel
from app.schemas.resource import QuestionPracticeResponse

router = APIRouter()

PRACTICE_DRILLS = [
    {
        "id": "drill-filler-pause",
        "title": "Silent Pause Drill",
        "tag": "filler_words",
        "duration": "5 Mins",
        "desc": 'Answer a complex technical query without using "um", "uh", or "like". Replace every verbal hesitation with a calm 1-second silent breath.',
        "category": "Vocal Discipline",
    },
    {
        "id": "drill-star-story",
        "title": "STAR Method Storytelling Drill",
        "tag": "star_method",
        "duration": "8 Mins",
        "desc": "Structure a past bug resolution strictly dividing your answer into 15s Situation, 15s Task, 45s Action, and 15s quantifiable Result.",
        "category": "Behavioral",
    },
    {
        "id": "drill-eye-contact",
        "title": "Webcam Eye-Level Gaze Lock",
        "tag": "eye_contact",
        "duration": "4 Mins",
        "desc": "Focus continuously on the camera lens while answering technical questions to build unconscious gaze endurance.",
        "category": "Body Language",
    },
    {
        "id": "drill-pitch",
        "title": "60-Second System Design Elevator Pitch",
        "tag": "technical",
        "duration": "6 Mins",
        "desc": "Explain how you would design a high-throughput URL shortener or rate limiter in under 60 seconds with clear trade-offs.",
        "category": "Technical Architecture",
    },
]

@router.get("/drills")
def get_practice_drills(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Return catalog of interactive candidate micro-drills."""
    return PRACTICE_DRILLS

@router.get("/questions", response_model=List[QuestionPracticeResponse])
def get_practice_questions(
    category_id: Optional[str] = Query(None, description="Category ID filter"),
    job_role_id: Optional[str] = Query(None, description="Job role ID filter"),
    difficulty_id: Optional[str] = Query(None, description="Difficulty ID filter"),
    search: Optional[str] = Query(None, description="Search keyword in question text"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve practice questions from question bank with sample answers and expected keywords."""
    query = db.query(Question).filter(Question.is_active == True)

    if category_id:
        query = query.filter(Question.category_id == category_id)
    if job_role_id:
        query = query.filter(Question.job_role_id == job_role_id)
    if difficulty_id:
        query = query.filter(Question.difficulty_id == difficulty_id)
    if search:
        query = query.filter(Question.text.ilike(f"%{search.strip()}%"))

    questions = query.limit(limit).all()

    result = []
    for q in questions:
        result.append(QuestionPracticeResponse(
            id=q.id,
            text=q.text,
            category_name=q.category.name if q.category else "General",
            job_role_name=q.job_role.name if q.job_role else "All Roles",
            difficulty_name=q.difficulty.name if q.difficulty else "Intermediate",
            expected_keywords=q.expected_keywords or [],
            sample_answer=q.sample_answer
        ))
    return result

@router.get("/questions/{question_id}", response_model=QuestionPracticeResponse)
def get_practice_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get single question drill details with sample answer."""
    q = db.query(Question).filter(
        Question.id == question_id,
        Question.is_active == True
    ).first()

    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    return QuestionPracticeResponse(
        id=q.id,
        text=q.text,
        category_name=q.category.name if q.category else "General",
        job_role_name=q.job_role.name if q.job_role else "All Roles",
        difficulty_name=q.difficulty.name if q.difficulty else "Intermediate",
        expected_keywords=q.expected_keywords or [],
        sample_answer=q.sample_answer
    )
