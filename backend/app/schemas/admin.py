from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# --- Dashboard & Analytics ---
class AdminDashboardMetrics(BaseModel):
    total_candidates: int
    total_interviews: int
    total_questions: int
    average_platform_score: float
    system_status: str

class AdminRecentSession(BaseModel):
    id: str
    candidate_name: str
    email: str
    role_name: str
    overall_score: float
    verdict: str
    created_at: str

class AdminDashboardResponse(BaseModel):
    metrics: AdminDashboardMetrics
    recent_sessions: List[AdminRecentSession]

class AdminAnalyticsResponse(BaseModel):
    activity_over_time: List[Dict[str, Any]]
    role_averages: List[Dict[str, Any]]

# --- Users ---
class AdminUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: str
    role: str
    is_active: bool
    is_email_verified: bool
    created_at: datetime

class UserUpdateAdmin(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_email_verified: Optional[bool] = None

# --- Question Bank ---
class AdminQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    text: str
    job_role_id: str
    role_name: str
    category_id: str
    category_name: str
    difficulty_id: str
    difficulty_name: str
    expected_keywords: List[str] = []
    sample_answer: Optional[str] = None
    is_active: bool

class AdminQuestionCreate(BaseModel):
    text: str
    job_role_id: str
    category_id: str
    difficulty_id: str
    expected_keywords: List[str] = []
    sample_answer: Optional[str] = None

class AdminQuestionUpdate(BaseModel):
    text: Optional[str] = None
    job_role_id: Optional[str] = None
    category_id: Optional[str] = None
    difficulty_id: Optional[str] = None
    expected_keywords: Optional[List[str]] = None
    sample_answer: Optional[str] = None
    is_active: Optional[bool] = None

# --- Taxonomies & Metadata ---
class JobRoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class JobRoleCreate(JobRoleBase):
    pass

class JobRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class JobRoleResponse(JobRoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: str

class DifficultyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str

# --- Resources & Templates ---
class ResourceAdminCreate(BaseModel):
    title: str
    url: str
    platform: str = "youtube"
    weak_area_tag: str
    job_role_id: Optional[str] = None
    difficulty: str = "All"
    is_active: bool = True

class ResourceAdminUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    platform: Optional[str] = None
    weak_area_tag: Optional[str] = None
    job_role_id: Optional[str] = None
    difficulty: Optional[str] = None
    is_active: Optional[bool] = None

class ResourceAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    url: str
    platform: str
    weak_area_tag: str
    job_role_id: Optional[str] = None
    difficulty: str
    is_active: bool
    created_at: datetime

class FeedbackTemplateCreate(BaseModel):
    area: str
    min_score: float = 0.0
    max_score: float = 100.0
    template_text: str

class FeedbackTemplateUpdate(BaseModel):
    area: Optional[str] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    template_text: Optional[str] = None

class FeedbackTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    area: str
    min_score: float
    max_score: float
    template_text: str

# --- Sessions & Reports ---
class AdminSessionResponse(BaseModel):
    id: str
    candidate_name: str
    email: str
    role_name: str
    category_name: str
    status: str
    total_questions: int
    duration_seconds: int
    created_at: str
    video_path: Optional[str] = None

class AdminReportSummaryResponse(BaseModel):
    id: str
    session_id: str
    candidate_name: str
    role_name: str
    overall_score: float
    final_verdict: str
    generated_at: str
    scores: Dict[str, float]

# --- Notifications ---
class NotificationBroadcastCreate(BaseModel):
    title: str
    message: str
    type: str = "announcement"
    user_id: Optional[str] = None

# --- Telemetry, Logs & Security ---
class AdminMonitoringResponse(BaseModel):
    server: str
    environment: str
    database: str
    ai_pipeline_workers: str
    storage: Dict[str, Any]

class AdminLogResponse(BaseModel):
    id: str
    action: str
    entity: str
    ip_address: Optional[str] = None
    created_at: str

class AdminLoginHistoryResponse(BaseModel):
    id: str
    email: str
    ip_address: Optional[str] = None
    success: bool
    created_at: str

class SecuritySettingsUpdate(BaseModel):
    max_duration: Optional[int] = 60
    max_questions: Optional[int] = 15
    maintenance_mode: Optional[bool] = False

class BackupResponse(BaseModel):
    id: str
    filename: str
    size_bytes: int
    created_at: str
