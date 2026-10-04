from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class ResumeAnalysisResponse(BaseModel):
    id: str
    resume_id: str
    extracted_education: List[Any] = Field(default_factory=list)
    extracted_skills: List[str] = Field(default_factory=list)
    extracted_projects: List[Any] = Field(default_factory=list)
    extracted_certifications: List[Any] = Field(default_factory=list)
    extracted_experience: List[Any] = Field(default_factory=list)
    missing_skills: List[Any] = Field(default_factory=list)
    weak_sections: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)
    resume_score: float = 85.0
    score_label: str = "Very Good"
    top_skills: List[Any] = Field(default_factory=list)
    years_experience: float = 2.0
    projects_count: int = 3
    strengths: List[str] = Field(default_factory=list)
    areas_to_improve: List[str] = Field(default_factory=list)
    status: str
    raw_text: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResumeAnalysisSummaryResponse(BaseModel):
    resume_id: str
    resume_score: float
    score_label: str
    top_skills: List[Any] = Field(default_factory=list)
    years_experience: float
    projects_count: int
    strengths: List[str] = Field(default_factory=list)
    areas_to_improve: List[str] = Field(default_factory=list)
    uploaded_at: datetime
    original_filename: str

class ResumeAnalysisFullResponse(ResumeAnalysisResponse):
    score_label: str

class ResumeResponse(BaseModel):
    id: str
    user_id: str
    file_path: str
    original_filename: str
    file_type: str
    is_active: bool
    uploaded_at: datetime
    analysis: Optional[ResumeAnalysisResponse] = None

    model_config = ConfigDict(from_attributes=True)

class ResumeAnalyzeRequest(BaseModel):
    job_role_id: Optional[str] = None
    job_role_name: Optional[str] = None
