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
    status: str
    raw_text: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

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
