from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.resource import LearningResource
from app.db.models.report import Recommendation
from app.schemas.resource import LearningResourceResponse, RecommendationResponse

router = APIRouter()

@router.get("", response_model=List[LearningResourceResponse])
def get_learning_resources(
    weak_area: Optional[str] = Query(None, description="Filter by weak area tag"),
    job_role_id: Optional[str] = Query(None, description="Filter by job role ID"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve active curated learning resources with optional filtering."""
    query = db.query(LearningResource).filter(LearningResource.is_active == True)

    if weak_area and weak_area.lower() != "all":
        query = query.filter(LearningResource.weak_area_tag == weak_area.lower().strip())

    if job_role_id:
        query = query.filter(LearningResource.job_role_id == job_role_id)

    if difficulty and difficulty.lower() != "all":
        query = query.filter(LearningResource.difficulty.ilike(f"%{difficulty}%"))

    resources = query.order_by(LearningResource.created_at.desc()).all()
    return resources

@router.get("/{resource_id}", response_model=LearningResourceResponse)
def get_learning_resource(
    resource_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve details for a single learning resource."""
    resource = db.query(LearningResource).filter(
        LearningResource.id == resource_id,
        LearningResource.is_active == True
    ).first()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning resource not found"
        )
    return resource

@router.get("/user/recommendations", response_model=List[RecommendationResponse])
def get_user_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve personalized learning recommendations generated for current candidate."""
    recs = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).order_by(Recommendation.created_at.desc()).limit(10).all()
    return recs
