from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class JobRoleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class InterviewCategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class DifficultyLevelResponse(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)

class InterviewCreateRequest(BaseModel):
    job_role_id: str
    category_id: str
    difficulty_id: str
    total_questions: int = Field(default=5, ge=1, le=15)
    num_questions: Optional[int] = None
    resume_id: Optional[str] = None
    mode: Optional[str] = "video"  # 'video' | 'audio' | 'text'

class AnswerResponse(BaseModel):
    id: str
    session_question_id: str
    transcript: str
    word_count: int
    duration_seconds: float
    filler_word_count: int
    speaking_rate_wpm: float

    model_config = ConfigDict(from_attributes=True)

class SessionQuestionResponse(BaseModel):
    id: str
    session_id: str
    order_index: int
    question_text: str
    source: str
    parent_question_id: Optional[str] = None
    time_limit_seconds: int
    status: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    answer: Optional[AnswerResponse] = None

    model_config = ConfigDict(from_attributes=True)

class InterviewSessionResponse(BaseModel):
    id: str
    user_id: str
    resume_id: Optional[str] = None
    job_role_id: str
    category_id: str
    difficulty_id: str
    status: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    total_questions: int
    duration_seconds: int
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    created_at: datetime
    job_role: Optional[JobRoleResponse] = None
    category: Optional[InterviewCategoryResponse] = None
    difficulty: Optional[DifficultyLevelResponse] = None

    model_config = ConfigDict(from_attributes=True)

class InterviewSessionDetailResponse(InterviewSessionResponse):
    questions: List[SessionQuestionResponse] = Field(default_factory=list)

class AnswerSubmitRequest(BaseModel):
    transcript: Optional[str] = ""
    duration_seconds: Optional[float] = 0.0

class InterviewProgressResponse(BaseModel):
    session_id: str
    status: str
    total_questions: int
    answered_questions: int
    current_index: int
    elapsed_seconds: int
    is_completed: bool

class InterviewStatusResponse(BaseModel):
    session_id: str
    status: str
    processing_step: Optional[str] = None
    progress_percentage: int = 0
    error: Optional[str] = None
