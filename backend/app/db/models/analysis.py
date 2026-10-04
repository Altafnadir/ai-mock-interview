import uuid
from datetime import datetime
from sqlalchemy import String, Float, Integer, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class AnalysisVoice(Base):
    __tablename__ = "analysis_voice"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    session_question_id: Mapped[str] = mapped_column(String(36), nullable=True)
    speaking_speed_wpm: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_pitch_hz: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    pitch_variance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    tone_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    clarity_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    fluency_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    pause_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_pause_duration: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_pause_duration: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    voice_stability_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    volume_score: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    pitch_score: Mapped[float] = mapped_column(Float, default=82.0, nullable=False)
    pace_score: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    pronunciation_score: Mapped[float] = mapped_column(Float, default=84.0, nullable=False)
    filler_score: Mapped[float] = mapped_column(Float, default=92.0, nullable=False)
    clarity_label: Mapped[str] = mapped_column(String(50), default="Optimal", nullable=False)
    used_fallback: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="voice_analysis")


class AnalysisVision(Base):
    __tablename__ = "analysis_vision"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    eye_contact_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    looking_away_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    posture_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    slouch_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    head_movement_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    body_stability_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sitting_position_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    shoulder_position_score: Mapped[float] = mapped_column(Float, default=82.0, nullable=False)
    head_position_score: Mapped[float] = mapped_column(Float, default=80.0, nullable=False)
    hand_gesture_score: Mapped[float] = mapped_column(Float, default=78.0, nullable=False)
    gaze_consistency_score: Mapped[float] = mapped_column(Float, default=80.0, nullable=False)
    blink_rate_per_min: Mapped[float] = mapped_column(Float, default=18.0, nullable=False)
    blink_label: Mapped[str] = mapped_column(String(20), default="Normal", nullable=False)
    distraction_score: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    frames_analyzed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    timeline: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    used_fallback: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="vision_analysis")


class AnalysisEmotion(Base):
    __tablename__ = "analysis_emotion"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    distribution: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)  # happy, confident, nervous, angry, sad, neutral, stress, smile %
    dominant_emotion: Mapped[str] = mapped_column(String(50), default="neutral", nullable=False)
    timeline: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    used_fallback: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="emotion_analysis")


class AnalysisGrammar(Base):
    __tablename__ = "analysis_grammar"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    session_question_id: Mapped[str] = mapped_column(String(36), nullable=True)
    grammar_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    vocabulary_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sentence_structure_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    pronunciation_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    language_quality_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    communication_effectiveness_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    errors: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    used_fallback: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="grammar_analysis")


class AnalysisContent(Base):
    __tablename__ = "analysis_content"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    session_question_id: Mapped[str] = mapped_column(String(36), ForeignKey("session_questions.id", ondelete="CASCADE"), unique=True, nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    completeness_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    technical_accuracy_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    star_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    star_breakdown: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)  # S, T, A, R presence & explanation
    keyword_match_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    matched_keywords: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    logical_flow_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    llm_comment: Mapped[str] = mapped_column(Text, nullable=True)
    used_fallback: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    session_question: Mapped["SessionQuestion"] = relationship("SessionQuestion", back_populates="content_analysis")
