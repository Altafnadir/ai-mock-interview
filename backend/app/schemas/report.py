from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class ResourceSimpleResponse(BaseModel):
    id: str
    title: str
    url: str
    platform: Optional[str] = "youtube"
    weak_area_tag: str
    difficulty: Optional[str] = "All"

    model_config = ConfigDict(from_attributes=True)

class RecommendationResponse(BaseModel):
    id: str
    weak_area_tag: str
    practice_suggestion: str
    resource_id: Optional[str] = None
    resource: Optional[ResourceSimpleResponse] = None

    model_config = ConfigDict(from_attributes=True)

class ReportResponse(BaseModel):
    id: str
    session_id: str
    overall_score: float
    confidence_score: float
    voice_score: float
    eye_contact_score: float
    communication_score: float
    content_score: float
    body_language_score: float
    grammar_score: float
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    confidence_analysis: str = ""
    communication_feedback: str = ""
    improvement_tips: List[str] = Field(default_factory=list)
    final_verdict: str = "Needs Improvement"
    pdf_path: Optional[str] = None
    summary_pdf_path: Optional[str] = None
    poster_path: Optional[str] = None
    generated_at: datetime
    recommendations: List[RecommendationResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

class ReportShareResponse(BaseModel):
    token: str
    share_url: str
    expires_at: datetime
