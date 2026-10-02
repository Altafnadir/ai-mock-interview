import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    voice_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    eye_contact_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    communication_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    content_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    body_language_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    grammar_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    strengths: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    weaknesses: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    confidence_analysis: Mapped[str] = mapped_column(Text, default="", nullable=False)
    communication_feedback: Mapped[str] = mapped_column(Text, default="", nullable=False)
    improvement_tips: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    candidate_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    final_verdict: Mapped[str] = mapped_column(String(100), default="Needs Improvement", nullable=False)
    pdf_path: Mapped[str] = mapped_column(String(500), nullable=True)
    summary_pdf_path: Mapped[str] = mapped_column(String(500), nullable=True)
    poster_path: Mapped[str] = mapped_column(String(500), nullable=True)
    used_fallback: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="report")
    shares: Mapped[list["ReportShare"]] = relationship("ReportShare", back_populates="report", cascade="all, delete-orphan")

    @property
    def recommendations(self):
        return self.session.recommendations if self.session else []


class ReportShare(Base):
    __tablename__ = "report_shares"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    report_id: Mapped[str] = mapped_column(String(36), ForeignKey("reports.id", ondelete="CASCADE"), index=True, nullable=False)
    token: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    report: Mapped["Report"] = relationship("Report", back_populates="shares")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    weak_area_tag: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_resources.id", ondelete="SET NULL"), nullable=True)
    practice_suggestion: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="recommendations")
    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="recommendations")
    resource: Mapped["LearningResource"] = relationship("LearningResource", back_populates="recommendations")
