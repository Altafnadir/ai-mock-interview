from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any
from datetime import datetime

class LearningResourceBase(BaseModel):
    title: str
    url: str
    platform: str = "youtube"
    weak_area_tag: str
    job_role_id: Optional[str] = None
    difficulty: str = "All"
    is_active: bool = True

class LearningResourceCreate(LearningResourceBase):
    pass

class LearningResourceUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    platform: Optional[str] = None
    weak_area_tag: Optional[str] = None
    job_role_id: Optional[str] = None
    difficulty: Optional[str] = None
    is_active: Optional[bool] = None

class LearningResourceResponse(LearningResourceBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RecommendationResponse(BaseModel):
    id: str
    session_id: str
    weak_area_tag: str
    practice_suggestion: str
    resource: Optional[LearningResourceResponse] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class QuestionPracticeResponse(BaseModel):
    id: str
    text: str
    category_name: str
    job_role_name: str
    difficulty_name: str
    expected_keywords: List[str] = Field(default_factory=list)
    sample_answer: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class NotificationCreate(BaseModel):
    user_id: Optional[str] = None  # None = broadcast to all
    title: str
    message: str
    type: str = "announcement"

class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    type: str
    link: Optional[str] = None
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

