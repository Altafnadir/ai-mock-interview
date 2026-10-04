import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.db.session import SessionLocal
from app.db.models.analysis import (
    AnalysisVoice, AnalysisVision, AnalysisEmotion,
    AnalysisGrammar, AnalysisContent
)
from app.ai.registry import ai_registry
from app.ai.media_normalizer import media_normalizer
from app.ai.scoring_engine import scoring_engine
from app.ai.filler_detector import filler_detector
from app.ai.grammar_analyzer import grammar_analyzer
from app.ai.voice_analyzer import voice_analyzer
from app.ai.vision_analyzer import vision_analyzer
from app.ai.emotion_analyzer import emotion_analyzer
from app.ai.content_evaluator import content_evaluator

client = TestClient(app)

from app.db.models.user import User, CandidateProfile
from app.core.security import get_password_hash, create_access_token

def get_candidate_token():
    test_email = "test_ai_candidate@gims.edu.pk"
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == test_email).first()
        if not user:
            user = User(
                email=test_email,
                full_name="AI Test Candidate",
                password_hash=get_password_hash("TestPassword123!"),
                role="candidate",
                is_active=True,
                is_email_verified=True,
                auth_provider="local"
            )
            db.add(user)
            db.flush()
            profile = CandidateProfile(user_id=user.id, experience_level="beginner")
            db.add(profile)
            db.commit()
            db.refresh(user)
        return create_access_token(user.id)
    finally:
        db.close()

def test_filler_detector():
    transcript = "Um, in our last deployment, we basically, like, used Docker and Kubernetes, you know, to handle traffic."
    res = filler_detector.analyze(transcript, duration_seconds=30.0)
    assert res["total_fillers"] >= 4
    assert "um" in res["breakdown"]
    assert "basically" in res["breakdown"]
    assert "like" in res["breakdown"]
    assert res["filler_percentage"] > 0
    assert len(res["coaching_tip"]) > 10

def test_grammar_analyzer():
    transcript = "In my project, we is building a distributed caching system that are more better."
    res = grammar_analyzer.analyze(transcript)
    assert res["grammar_error_count"] >= 1
    assert 30.0 <= res["readability_score"] <= 100.0
    assert 0.0 <= res["vocabulary_richness_score"] <= 100.0
    assert len(res["suggestions"]) > 0

def test_voice_vision_emotion_analyzers():
    # 1. Voice
    v_res = voice_analyzer.analyze(audio_path=None, duration_seconds=45.0, word_count=85)
    assert v_res["speaking_rate_wpm"] > 50
    assert v_res["pitch_mean"] > 80
    assert v_res["volume_consistency_score"] > 50
    assert len(v_res["feedback"]) > 10

    # 2. Vision
    vis_res = vision_analyzer.analyze(video_path=None, duration_seconds=45.0)
    assert 50.0 <= vis_res["eye_contact_percentage"] <= 100.0
    assert vis_res["posture_stability_score"] > 50.0
    assert len(vis_res["feedback"]) > 10

    # 3. Emotion
    em_res = emotion_analyzer.analyze(duration_seconds=45.0, disfluency_rate=2.5, speaking_rate_wpm=130.0)
    assert em_res["confidence_score"] > 50
    assert em_res["stress_score"] < 50
    assert len(em_res["emotion_timeline"]) >= 1

def test_content_evaluator():
    question = "How do you handle database indexing and query optimization in PostgreSQL?"
    answer = "In my previous project, we faced slow query response times. I analyzed query execution plans using EXPLAIN ANALYZE, added B-Tree composite indexes on foreign keys, and reduced database response latency by 45% for 10k daily users."
    expected_kws = ["indexing", "explain", "latency", "postgresql"]

    eval_res = content_evaluator.evaluate_answer(
        question_text=question,
        answer_text=answer,
        expected_keywords=expected_kws,
        job_role_name="Backend Developer",
        category_name="Technical"
    )

    assert eval_res["technical_accuracy_score"] >= 70.0
    assert eval_res["star_action_score"] >= 70.0
    assert eval_res["star_result_score"] >= 70.0
    assert len(eval_res["keywords_matched"]) > 0
    assert len(eval_res["strengths"]) > 0

def test_full_ai_analysis_pipeline_integration():
    token = get_candidate_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create a 2-question session
    meta = client.get("/api/v1/meta/all").json()
    create_resp = client.post("/api/v1/interviews", json={
        "job_role_id": meta["job_roles"][0]["id"],
        "category_id": meta["categories"][0]["id"],
        "difficulty_id": meta["difficulties"][0]["id"],
        "total_questions": 2,
        "mode": "video"
    }, headers=headers)
    assert create_resp.status_code == 201
    session_id = create_resp.json()["id"]

    # 2. Start session
    client.post(f"/api/v1/interviews/{session_id}/start", headers=headers)

    # 3. Answer Question 1
    ans1 = {
        "transcript": "In our team project, um, we implemented asynchronous worker queues using Redis and Celery, basically reducing background task latency by 50%.",
        "duration_seconds": 35.0
    }
    client.post(f"/api/v1/interviews/{session_id}/answer", json=ans1, headers=headers)

    # 4. Answer Question 2
    ans2 = {
        "transcript": "For state management, we migrated our React application to Zustand, which eliminated unnecessary re-renders and improved UI responsiveness.",
        "duration_seconds": 40.0
    }
    client.post(f"/api/v1/interviews/{session_id}/answer", json=ans2, headers=headers)

    # 5. Trigger Pipeline Processing
    proc_resp = client.post(f"/api/v1/interviews/{session_id}/process", headers=headers)
    assert proc_resp.status_code == 200
    analyzed_session = proc_resp.json()
    assert analyzed_session["status"] == "analyzed"

    # 6. Verify all DB analysis records were created
    db = SessionLocal()
    try:
        voice = db.query(AnalysisVoice).filter(AnalysisVoice.session_id == session_id).first()
        vision = db.query(AnalysisVision).filter(AnalysisVision.session_id == session_id).first()
        emotion = db.query(AnalysisEmotion).filter(AnalysisEmotion.session_id == session_id).first()
        grammar = db.query(AnalysisGrammar).filter(AnalysisGrammar.session_id == session_id).first()
        content = db.query(AnalysisContent).all()

        assert voice is not None, "AnalysisVoice record missing"
        assert voice.speaking_speed_wpm > 0
        assert voice.clarity_score > 0

        assert vision is not None, "AnalysisVision record missing"
        assert vision.eye_contact_percentage > 0
        assert vision.posture_score > 0

        assert emotion is not None, "AnalysisEmotion record missing"
        assert emotion.distribution.get("confident") > 0
        assert emotion.dominant_emotion in ["confident", "neutral"]

        assert grammar is not None, "AnalysisGrammar record missing"
        assert grammar.grammar_score > 0

        assert len(content) >= 2, "AnalysisContent records missing for questions"
    finally:
        db.close()

def test_ai_plugin_registry():
    plugins = ai_registry.list_plugins()
    assert len(plugins) == 7
    plugin_names = {p["name"] for p in plugins}
    assert "stt" in plugin_names
    assert "filler_detector" in plugin_names
    assert "voice_analyzer" in plugin_names
    assert "vision_analyzer" in plugin_names
    assert "emotion_analyzer" in plugin_names
    assert "grammar_analyzer" in plugin_names
    assert "content_evaluator" in plugin_names

    # Test dynamic execution through registry
    res = ai_registry.execute("filler_detector", transcript="Um, like, basically", duration_seconds=10.0)
    assert res["total_fillers"] == 3

def test_media_normalizer_graceful():
    # Normalizer handles missing/null paths safely without crashing
    norm_audio = media_normalizer.normalize_audio(None)
    assert norm_audio is None

    norm_video = media_normalizer.normalize_video(None)
    assert norm_video is None

def test_scoring_engine_and_confidence():
    # Test composite confidence computation
    conf = scoring_engine.compute_composite_confidence(
        voice_stability=85.0,
        emotion_confidence=82.0,
        eye_contact_pct=80.0,
        posture_score=85.0,
        filler_frequency_wpm=1.5
    )
    assert 70.0 <= conf <= 95.0

    # Test calculation with default 7-factor weights
    scores = scoring_engine.calculate_scores(
        content_scores=[88.0, 90.0],
        communication_score=85.0,
        voice_score=82.0,
        eye_contact_score=80.0,
        body_language_score=85.0,
        confidence_score=conf,
        grammar_score=90.0
    )
    assert scores["overall_score"] >= 80.0
    assert scores["final_verdict"] in ["Excellent", "Good"]
    assert scores["weights_used"]["content"] == 25.0
    assert scores["weights_used"]["voice"] == 15.0
    assert scores["weights_used"]["grammar"] == 10.0

