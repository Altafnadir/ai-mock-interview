from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class RecentSessionSummary(BaseModel):
    id: str
    job_role_name: str
    category_name: str
    difficulty_name: str
    status: str
    overall_score: Optional[float] = None
    final_verdict: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CandidateDashboardResponse(BaseModel):
    total_interviews: int
    average_score: float
    best_score: float
    interviews_this_month: int
    readiness_percentage: float
    dimension_averages: Dict[str, float]
    score_trend: List[Dict[str, Any]]
    recent_sessions: List[RecentSessionSummary]
    weak_areas: List[Dict[str, Any]]
    recommended_resources: List[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)

class DashboardMetrics(BaseModel):
    total_interviews: int
    average_score: float
    highest_score: float
    practice_streak_days: int
    confidence_score: float = 75.0
    communication_score: float = 75.0
    grammar_score: float = 75.0
    resume_score: float = 85.0
    interviews_delta_week: int = 0
    score_delta_week: float = 0.0
    confidence_label: str = "Good"
    communication_label: str = "Good"
    grammar_label: str = "Good"
    resume_label: str = "Very Good"
    average_score_label: str = "Good"
    practice_streak: str = "1 Days"
    next_goal: Dict[str, Any] = Field(default_factory=dict)

class CompetencyRadarItem(BaseModel):
    subject: str
    value: float
    fullMark: float = 100.0

class RecentSessionItem(BaseModel):
    id: str
    role_name: str
    category_name: str
    difficulty_name: str
    score: Optional[float] = None
    verdict: Optional[str] = None
    date: str

class WeakAreaAlert(BaseModel):
    tag: str
    title: str
    suggestion: str

class DashboardOverviewResponse(BaseModel):
    metrics: DashboardMetrics
    score_trend: List[Dict[str, Any]]
    competency_radar: List[CompetencyRadarItem]
    recent_sessions: List[RecentSessionItem]
    weak_area_alert: Optional[WeakAreaAlert] = None
    ai_recommendation: Optional[Dict[str, Any]] = None
    performance_overview: List[Dict[str, Any]] = Field(default_factory=list)

class InterviewSummaryResponse(BaseModel):
    total_interviews: int
    average_score: float
    best_score: float
    total_practice_time_seconds: int
    total_practice_time_formatted: str
