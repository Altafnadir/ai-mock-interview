import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, JSON, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class JobRole(Base):
    __tablename__ = "job_roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    questions: Mapped[list["Question"]] = relationship("Question", back_populates="job_role")
    interview_sessions: Mapped[list["InterviewSession"]] = relationship("InterviewSession", back_populates="job_role")


class InterviewCategory(Base):
    __tablename__ = "interview_categories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)  # 'HR' | 'Technical' | 'Behavioral' | 'Mixed'
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    questions: Mapped[list["Question"]] = relationship("Question", back_populates="category")
    interview_sessions: Mapped[list["InterviewSession"]] = relationship("InterviewSession", back_populates="category")


class DifficultyLevel(Base):
    __tablename__ = "difficulty_levels"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)  # 'Beginner' | 'Intermediate' | 'Advanced'

    questions: Mapped[list["Question"]] = relationship("Question", back_populates="difficulty")
    interview_sessions: Mapped[list["InterviewSession"]] = relationship("InterviewSession", back_populates="difficulty")


class QuestionSet(Base):
    __tablename__ = "question_sets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    uploaded_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    questions: Mapped[list["Question"]] = relationship("Question", back_populates="question_set")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_categories.id"), index=True, nullable=False)
    job_role_id: Mapped[str] = mapped_column(String(36), ForeignKey("job_roles.id"), index=True, nullable=False)
    difficulty_id: Mapped[str] = mapped_column(String(36), ForeignKey("difficulty_levels.id"), index=True, nullable=False)
    expected_keywords: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    sample_answer: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    question_set_id: Mapped[str] = mapped_column(String(36), ForeignKey("question_sets.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    category: Mapped["InterviewCategory"] = relationship("InterviewCategory", back_populates="questions")
    job_role: Mapped["JobRole"] = relationship("JobRole", back_populates="questions")
    difficulty: Mapped["DifficultyLevel"] = relationship("DifficultyLevel", back_populates="questions")
    question_set: Mapped["QuestionSet"] = relationship("QuestionSet", back_populates="questions")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    job_role_id: Mapped[str] = mapped_column(String(36), ForeignKey("job_roles.id"), index=True, nullable=False)
    category_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_categories.id"), index=True, nullable=False)
    difficulty_id: Mapped[str] = mapped_column(String(36), ForeignKey("difficulty_levels.id"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="created", index=True, nullable=False)
    # Statuses: 'created' | 'in_progress' | 'completed' | 'processing' | 'analyzed' | 'failed' | 'abandoned'
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    video_path: Mapped[str] = mapped_column(String(500), nullable=True)
    audio_path: Mapped[str] = mapped_column(String(500), nullable=True)
    processing_error: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="interview_sessions")
    resume: Mapped["Resume"] = relationship("Resume", back_populates="interview_sessions")
    job_role: Mapped["JobRole"] = relationship("JobRole", back_populates="interview_sessions")
    category: Mapped["InterviewCategory"] = relationship("InterviewCategory", back_populates="interview_sessions")
    difficulty: Mapped["DifficultyLevel"] = relationship("DifficultyLevel", back_populates="interview_sessions")

    questions: Mapped[list["SessionQuestion"]] = relationship("SessionQuestion", back_populates="session", cascade="all, delete-orphan", order_by="SessionQuestion.order_index")
    voice_analysis: Mapped["AnalysisVoice"] = relationship("AnalysisVoice", back_populates="session", uselist=False, cascade="all, delete-orphan")
    vision_analysis: Mapped["AnalysisVision"] = relationship("AnalysisVision", back_populates="session", uselist=False, cascade="all, delete-orphan")
    emotion_analysis: Mapped["AnalysisEmotion"] = relationship("AnalysisEmotion", back_populates="session", uselist=False, cascade="all, delete-orphan")
    grammar_analysis: Mapped["AnalysisGrammar"] = relationship("AnalysisGrammar", back_populates="session", uselist=False, cascade="all, delete-orphan")
    report: Mapped["Report"] = relationship("Report", back_populates="session", uselist=False, cascade="all, delete-orphan")
    recommendations: Mapped[list["Recommendation"]] = relationship("Recommendation", back_populates="session", cascade="all, delete-orphan")


class SessionQuestion(Base):
    __tablename__ = "session_questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(20), default="bank", nullable=False)  # 'ai' | 'bank' | 'followup'
    parent_question_id: Mapped[str] = mapped_column(String(36), ForeignKey("session_questions.id", ondelete="SET NULL"), nullable=True)
    time_limit_seconds: Mapped[int] = mapped_column(Integer, default=120, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # 'pending' | 'answered' | 'skipped'
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    video_segment_path: Mapped[str] = mapped_column(String(500), nullable=True)
    audio_segment_path: Mapped[str] = mapped_column(String(500), nullable=True)

    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="questions")
    answer: Mapped["Answer"] = relationship("Answer", back_populates="session_question", uselist=False, cascade="all, delete-orphan")
    content_analysis: Mapped["AnalysisContent"] = relationship("AnalysisContent", back_populates="session_question", uselist=False, cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_question_id: Mapped[str] = mapped_column(String(36), ForeignKey("session_questions.id", ondelete="CASCADE"), unique=True, nullable=False)
    transcript: Mapped[str] = mapped_column(Text, default="", nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    filler_word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    filler_words_breakdown: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    speaking_rate_wpm: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    session_question: Mapped["SessionQuestion"] = relationship("SessionQuestion", back_populates="answer")
