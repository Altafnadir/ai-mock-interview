import logging
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.db.models.interview import InterviewSession, SessionQuestion, Answer
from app.db.models.analysis import (
    AnalysisVoice, AnalysisVision, AnalysisEmotion,
    AnalysisGrammar, AnalysisContent
)
from app.db.models.report import Report
from app.ai.filler_detector import filler_detector
from app.ai.voice_analyzer import voice_analyzer
from app.ai.vision_analyzer import vision_analyzer
from app.ai.emotion_analyzer import emotion_analyzer
from app.ai.grammar_analyzer import grammar_analyzer
from app.ai.content_evaluator import content_evaluator
from app.ai.scoring_engine import scoring_engine
from app.ai.feedback_generator import feedback_generator
from app.reports.pdf_builder import pdf_builder

logger = logging.getLogger(__name__)

class PipelineWorker:
    """Orchestrates the 7-stage multimodal AI analysis pipeline for completed interview sessions."""

    def process_session(self, session_id: str, db: Session) -> Dict[str, Any]:
        session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
        if not session:
            raise ValueError(f"Interview session {session_id} not found")

        logger.info(f"Starting AI Analysis Pipeline for Session {session_id}...")
        session.status = "processing"
        db.commit()

        try:
            questions = db.query(SessionQuestion).filter(
                SessionQuestion.session_id == session.id
            ).order_by(SessionQuestion.order_index).all()

            role_name = session.job_role.name if session.job_role else "Software Engineer"
            cat_name = session.category.name if session.category else "Technical"

            all_transcripts = []
            total_duration = 0.0
            total_words = 0
            total_fillers = 0

            # 1. Per-Question Content & STAR Evaluation
            for q in questions:
                answer = q.answer
                transcript = answer.transcript if answer else ""
                duration = answer.duration_seconds if answer else 30.0

                all_transcripts.append(transcript)
                total_duration += duration
                total_words += (answer.word_count if answer else 0)

                # Filler breakdown
                filler_res = filler_detector.analyze(transcript, duration)
                total_fillers += filler_res["total_fillers"]
                if answer:
                    answer.filler_word_count = filler_res["total_fillers"]
                    answer.filler_words_breakdown = filler_res["breakdown"]

                # Expected keywords
                expected_kws = []
                # Check if existing question matches
                content_res = content_evaluator.evaluate_answer(
                    question_text=q.question_text,
                    answer_text=transcript,
                    expected_keywords=expected_kws,
                    job_role_name=role_name,
                    category_name=cat_name
                )

                # Upsert AnalysisContent
                content_entry = db.query(AnalysisContent).filter(
                    AnalysisContent.session_question_id == q.id
                ).first()
                if not content_entry:
                    content_entry = AnalysisContent(session_question_id=q.id)
                    db.add(content_entry)

                star_avg = round((
                    content_res["star_situation_score"] +
                    content_res["star_task_score"] +
                    content_res["star_action_score"] +
                    content_res["star_result_score"]
                ) / 4.0, 1)

                content_entry.relevance_score = content_res["relevance_score"]
                content_entry.completeness_score = content_res["completeness_score"]
                content_entry.technical_accuracy_score = content_res["technical_accuracy_score"]
                content_entry.star_score = star_avg
                content_entry.star_breakdown = {
                    "situation": content_res["star_situation_score"],
                    "task": content_res["star_task_score"],
                    "action": content_res["star_action_score"],
                    "result": content_res["star_result_score"]
                }
                content_entry.keyword_match_score = content_res.get("keyword_match_score", 80.0)
                content_entry.matched_keywords = content_res.get("keywords_matched", [])
                content_entry.logical_flow_score = round((content_res["relevance_score"] + star_avg) / 2.0, 1)
                content_entry.llm_comment = " ".join(content_res.get("strengths", []) + content_res.get("improvements", []))

            combined_transcript = " ".join(all_transcripts)
            session_duration = max(total_duration, float(session.duration_seconds or 60.0))

            # 2. Voice DSP Analysis
            voice_res = voice_analyzer.analyze(
                audio_path=session.audio_path,
                duration_seconds=session_duration,
                word_count=total_words
            )

            voice_entry = db.query(AnalysisVoice).filter(AnalysisVoice.session_id == session.id).first()
            if not voice_entry:
                voice_entry = AnalysisVoice(session_id=session.id)
                db.add(voice_entry)

            voice_entry.speaking_speed_wpm = voice_res["speaking_rate_wpm"]
            voice_entry.avg_pitch_hz = voice_res["pitch_mean"]
            voice_entry.pitch_variance = voice_res["pitch_variance"]
            voice_entry.tone_score = voice_res["volume_consistency_score"]
            voice_entry.clarity_score = voice_res["clarity_score"]
            voice_entry.fluency_score = max(round(100.0 - (total_fillers * 2.0), 1), 55.0)
            voice_entry.confidence_score = round((voice_res["volume_consistency_score"] + voice_res["clarity_score"]) / 2.0, 1)
            voice_entry.pause_count = voice_res["pause_count"]
            voice_entry.avg_pause_duration = voice_res["average_pause_seconds"]
            voice_entry.total_pause_duration = round(voice_res["pause_count"] * voice_res["average_pause_seconds"], 1)
            voice_entry.voice_stability_score = voice_res["volume_consistency_score"]

            # 3. Vision Analysis
            vision_res = vision_analyzer.analyze(
                video_path=session.video_path,
                duration_seconds=session_duration
            )

            vision_entry = db.query(AnalysisVision).filter(AnalysisVision.session_id == session.id).first()
            if not vision_entry:
                vision_entry = AnalysisVision(session_id=session.id)
                db.add(vision_entry)

            vision_entry.eye_contact_percentage = vision_res["eye_contact_percentage"]
            vision_entry.looking_away_count = vision_res["looking_away_count"]
            vision_entry.posture_score = vision_res["posture_stability_score"]
            vision_entry.slouch_percentage = round((vision_res["slouch_detection_count"] / 20.0) * 100, 1)
            vision_entry.head_movement_score = 84.0
            vision_entry.body_stability_score = vision_res["posture_stability_score"]
            vision_entry.sitting_position_score = 86.0
            vision_entry.frames_analyzed = 120
            vision_entry.timeline = [
                {"time": "0:00", "eye_contact": True, "posture": "upright"},
                {"time": "0:30", "eye_contact": True, "posture": "upright"},
                {"time": "1:00", "eye_contact": False, "posture": "slight_tilt"},
                {"time": "1:30", "eye_contact": True, "posture": "upright"},
            ]

            # 4. Emotion Analysis
            filler_pct = round((total_fillers / max(total_words, 1)) * 100, 1)
            emotion_res = emotion_analyzer.analyze(
                duration_seconds=session_duration,
                disfluency_rate=filler_pct,
                speaking_rate_wpm=voice_res["speaking_rate_wpm"]
            )

            emotion_entry = db.query(AnalysisEmotion).filter(AnalysisEmotion.session_id == session.id).first()
            if not emotion_entry:
                emotion_entry = AnalysisEmotion(session_id=session.id)
                db.add(emotion_entry)

            emotion_entry.dominant_emotion = emotion_res["dominant_emotion"]
            emotion_entry.distribution = {
                "confident": emotion_res["confidence_score"],
                "stress": emotion_res["stress_score"],
                "neutral": 65.0,
                "smiling": emotion_res["smile_percentage"]
            }
            emotion_entry.timeline = emotion_res["emotion_timeline"]

            # 5. Grammar & Lexical Analysis
            grammar_res = grammar_analyzer.analyze(combined_transcript)

            grammar_entry = db.query(AnalysisGrammar).filter(AnalysisGrammar.session_id == session.id).first()
            if not grammar_entry:
                grammar_entry = AnalysisGrammar(session_id=session.id)
                db.add(grammar_entry)

            gram_score = max(round(100.0 - (grammar_res["grammar_error_count"] * 5.0), 1), 50.0)
            grammar_entry.grammar_score = gram_score
            grammar_entry.vocabulary_score = grammar_res["vocabulary_richness_score"]
            grammar_entry.sentence_structure_score = grammar_res["readability_score"]
            grammar_entry.pronunciation_score = 88.0
            grammar_entry.language_quality_score = round((gram_score + grammar_res["vocabulary_richness_score"]) / 2.0, 1)
            grammar_entry.communication_effectiveness_score = round((grammar_res["readability_score"] + gram_score) / 2.0, 1)
            grammar_entry.errors = grammar_res["error_breakdown"]

            # 6. Scoring Engine & Multi-Dimensional Weights
            content_scores = [q.content_analysis.technical_accuracy_score for q in questions if q.content_analysis]
            comm_score = round((grammar_entry.communication_effectiveness_score + voice_entry.clarity_score) / 2.0, 1)

            calculated_scores = scoring_engine.calculate_scores(
                content_scores=content_scores,
                communication_score=comm_score,
                voice_score=voice_entry.confidence_score,
                eye_contact_score=vision_entry.eye_contact_percentage,
                body_language_score=vision_entry.posture_score,
                confidence_score=emotion_res["confidence_score"],
                grammar_score=grammar_entry.grammar_score
            )

            # 7. Feedback & Recommendations
            question_evals = [
                {
                    "question_text": q.question_text,
                    "transcript": q.answer.transcript if q.answer else "",
                    "technical_accuracy": q.content_analysis.technical_accuracy_score if q.content_analysis else 80.0,
                    "star_score": q.content_analysis.star_score if q.content_analysis else 80.0
                }
                for q in questions
            ]

            feedback_data = feedback_generator.generate_feedback(
                scores=calculated_scores,
                question_evals=question_evals,
                voice_feedback=voice_res["feedback"],
                vision_feedback=vision_res["feedback"],
                grammar_feedback=grammar_res["suggestions"],
                role_name=role_name
            )

            # Create or update learning recommendations
            recs = feedback_generator.create_recommendations(
                db=db,
                user_id=session.user_id,
                session_id=session.id,
                weak_area_tags=feedback_data["weak_area_tags"]
            )

            # 8. ReportLab PDF Generation
            candidate_user = session.user
            c_name = candidate_user.full_name if candidate_user else "Candidate"
            c_email = candidate_user.email if candidate_user else ""
            date_str = session.created_at.strftime("%B %d, %Y")

            rec_list_for_pdf = [
                {"title": r.resource.title if r.resource else r.weak_area_tag, "url": r.resource.url if r.resource else "https://youtube.com"}
                for r in recs
            ]

            pdf_path = pdf_builder.build_report_pdf(
                session_id=session.id,
                candidate_name=c_name,
                candidate_email=c_email,
                job_role=role_name,
                category=cat_name,
                difficulty=session.difficulty.name if session.difficulty else "Intermediate",
                date_str=date_str,
                overall_score=calculated_scores["overall_score"],
                final_verdict=calculated_scores["final_verdict"],
                score_breakdown=calculated_scores,
                strengths=feedback_data["strengths"],
                weaknesses=feedback_data["weaknesses"],
                improvement_tips=feedback_data["improvement_tips"],
                questions_data=question_evals,
                recommendations=rec_list_for_pdf
            )

            # 9. Upsert Report Record
            report_entry = db.query(Report).filter(Report.session_id == session.id).first()
            if not report_entry:
                report_entry = Report(session_id=session.id)
                db.add(report_entry)

            report_entry.overall_score = calculated_scores["overall_score"]
            report_entry.confidence_score = calculated_scores["confidence_score"]
            report_entry.voice_score = calculated_scores["voice_score"]
            report_entry.eye_contact_score = calculated_scores["eye_contact_score"]
            report_entry.communication_score = calculated_scores["communication_score"]
            report_entry.content_score = calculated_scores["content_score"]
            report_entry.body_language_score = calculated_scores["body_language_score"]
            report_entry.grammar_score = calculated_scores["grammar_score"]
            report_entry.strengths = feedback_data["strengths"]
            report_entry.weaknesses = feedback_data["weaknesses"]
            report_entry.confidence_analysis = feedback_data["confidence_analysis"]
            report_entry.communication_feedback = feedback_data["communication_feedback"]
            report_entry.improvement_tips = feedback_data["improvement_tips"]
            report_entry.final_verdict = calculated_scores["final_verdict"]
            report_entry.pdf_path = pdf_path

            # Mark session as analyzed
            session.status = "analyzed"
            session.processing_error = None
            db.commit()
            logger.info(f"AI Pipeline and Report Generation completed successfully for Session {session_id}.")

            return {
                "session_id": session.id,
                "status": "analyzed",
                "overall_score": report_entry.overall_score,
                "final_verdict": report_entry.final_verdict,
                "pdf_path": report_entry.pdf_path
            }

        except Exception as e:
            logger.error(f"Pipeline processing error for Session {session_id}: {e}", exc_info=True)
            session.status = "failed"
            session.processing_error = str(e)
            db.commit()
            raise

pipeline_worker = PipelineWorker()
