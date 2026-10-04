import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, JSON, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'pdf' | 'docx'
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="resumes")
    analysis: Mapped["ResumeAnalysis"] = relationship("ResumeAnalysis", back_populates="resume", uselist=False, cascade="all, delete-orphan")
    interview_sessions: Mapped[list["InterviewSession"]] = relationship("InterviewSession", back_populates="resume")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), unique=True, nullable=False)
    extracted_education: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    extracted_skills: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    extracted_projects: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    extracted_certifications: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    extracted_experience: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    missing_skills: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    weak_sections: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    improvement_suggestions: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    resume_score: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    top_skills: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    years_experience: Mapped[float] = mapped_column(Float, default=2.0, nullable=False)
    projects_count: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    strengths: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    areas_to_improve: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # 'pending' | 'analyzed' | 'failed'
    raw_text: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="analysis")
