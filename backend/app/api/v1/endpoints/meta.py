from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.db.models.interview import JobRole, InterviewCategory, DifficultyLevel
from app.schemas.interview import JobRoleResponse, InterviewCategoryResponse, DifficultyLevelResponse

router = APIRouter()

@router.get("/job-roles", response_model=List[JobRoleResponse])
def get_job_roles(db: Session = Depends(get_db)):
    """Fetch all active interview job roles."""
    return db.query(JobRole).filter(JobRole.is_active == True).order_by(JobRole.name).all()

@router.get("/categories", response_model=List[InterviewCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Fetch all active interview categories (HR, Technical, Behavioral, Mixed)."""
    return db.query(InterviewCategory).filter(InterviewCategory.is_active == True).order_by(InterviewCategory.name).all()

@router.get("/difficulties", response_model=List[DifficultyLevelResponse])
def get_difficulties(db: Session = Depends(get_db)):
    """Fetch interview difficulty levels (Beginner, Intermediate, Advanced)."""
    return db.query(DifficultyLevel).all()

@router.get("/all")
def get_all_meta(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Single call helper to load all interview setup dropdowns at once."""
    roles = db.query(JobRole).filter(JobRole.is_active == True).order_by(JobRole.name).all()
    categories = db.query(InterviewCategory).filter(InterviewCategory.is_active == True).order_by(InterviewCategory.name).all()
    difficulties = db.query(DifficultyLevel).all()

    return {
        "job_roles": [JobRoleResponse.model_validate(r) for r in roles],
        "categories": [InterviewCategoryResponse.model_validate(c) for c in categories],
        "difficulties": [DifficultyLevelResponse.model_validate(d) for d in difficulties]
    }
