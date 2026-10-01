from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class EducationItem(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    grade: Optional[str] = None

class ExperienceItem(BaseModel):
    role: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class CandidateProfileUpdate(BaseModel):
    phone: Optional[str] = None
    education: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = None
    work_experience: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[Any]] = None
    preferred_job_roles: Optional[List[str]] = None
    experience_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")

class CandidateProfileResponse(BaseModel):
    id: str
    user_id: str
    phone: Optional[str] = None
    education: List[Any] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    work_experience: List[Any] = Field(default_factory=list)
    certifications: List[Any] = Field(default_factory=list)
    preferred_job_roles: List[str] = Field(default_factory=list)
    experience_level: str = "beginner"
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserProfileResponse(BaseModel):
    id: str
    full_name: str
    email: str
    role: str
    is_active: bool
    is_email_verified: bool
    auth_provider: str
    profile_picture_path: Optional[str] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime
    profile: Optional[CandidateProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)
