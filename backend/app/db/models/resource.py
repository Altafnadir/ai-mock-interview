import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class LearningResource(Base):
    __tablename__ = "learning_resources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    platform: Mapped[str] = mapped_column(String(50), default="youtube", nullable=False)  # 'youtube' | 'article' | 'other'
    weak_area_tag: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    # Tags: 'eye_contact' | 'communication' | 'star_method' | 'filler_words' | 'technical' | 'confidence' | 'english_pronunciation' | 'body_language' | 'grammar' | 'posture'
    job_role_id: Mapped[str] = mapped_column(String(36), ForeignKey("job_roles.id", ondelete="SET NULL"), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(20), default="All", nullable=False)
    level: Mapped[str] = mapped_column(String(20), default="Beginner", nullable=False)  # 'Beginner' | 'Intermediate' | 'Advanced'
    thumbnail_url: Mapped[str] = mapped_column(String(500), nullable=True)
    duration_seconds: Mapped[int] = mapped_column(Float, default=600, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    view_count: Mapped[int] = mapped_column(Float, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    added_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    recommendations: Mapped[list["Recommendation"]] = relationship("Recommendation", back_populates="resource")


class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    resource_id: Mapped[str] = mapped_column(String(36), ForeignKey("learning_resources.id", ondelete="CASCADE"), index=True, nullable=False)
    watched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class FeedbackTemplate(Base):
    __tablename__ = "feedback_templates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    area: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    # Area: 'overall' | 'voice' | 'vision' | 'grammar' | 'content' | 'confidence'
    min_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    max_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    template_text: Mapped[str] = mapped_column(Text, nullable=False)
