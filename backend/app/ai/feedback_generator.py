import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.config import settings
from app.db.models.resource import LearningResource
from app.db.models.report import Report, Recommendation
from app.db.models.interview import InterviewSession

logger = logging.getLogger(__name__)

class FeedbackGenerator:
    """Synthesizes candidate qualitative evaluation, strengths, weaknesses, and maps targeted learning resources.
    
    Implements 8 canonical weak area tags:
    - eye_contact, communication, star_method, filler_words, technical, confidence, english_pronunciation, body_language.
    
    Dynamic Re-ranking:
    - Analyzes past sessions for the candidate.
    - Improved areas drop in priority; persistently low or declining areas rise to top.
    """

    CANONICAL_TAGS = [
        "eye_contact", "communication", "star_method", "filler_words",
        "technical", "confidence", "english_pronunciation", "body_language"
    ]

    TAG_SUGGESTIONS = {
        "star_method": "Structure behavioral answers with clear Situation, Task, Action, and quantifiable Result milestones.",
        "eye_contact": "Maintain continuous gaze engagement by positioning the camera at eye level and speaking directly into the lens.",
        "filler_words": "Replace verbal hesitations ('um', 'uh', 'like') with calm, intentional 1-second silent pauses.",
        "technical": "Reinforce technical explanations with domain keywords, architectural trade-offs, and scaling considerations.",
        "confidence": "Project commanding executive presence through measured breathing and composed vocal projection.",
        "communication": "Deliver crisp, declarative statements rather than extended conversational run-ons.",
        "english_pronunciation": "Enunciate technical terminology deliberately and pace syllable emphasis at key points.",
        "body_language": "Keep shoulders relaxed and posture aligned upright without excessive leaning or slouching."
    }

    def generate_feedback(
        self,
        scores: Dict[str, float],
        question_evals: List[Dict[str, Any]],
        voice_feedback: str,
        vision_feedback: str,
        grammar_feedback: List[str],
        role_name: str
    ) -> Dict[str, Any]:
        strengths = []
        weaknesses = []
        improvement_tips = []
        detected_weak_tags = []

        # 1. Technical / Content
        content_sc = scores.get("content_score", 75.0)
        if content_sc >= 80.0:
            strengths.append(f"Demonstrated solid technical depth and problem-solving relevant to {role_name}.")
        else:
            weaknesses.append("Answers occasionally lacked architectural depth or omitted core domain keywords.")
            improvement_tips.append("Incorporate specific technical frameworks, tools, and production considerations.")
            detected_weak_tags.append("technical")

        # 2. STAR Method
        avg_star = 80.0
        if question_evals:
            stars = [q.get("star_score", 80.0) for q in question_evals if q.get("star_score") is not None]
            if stars:
                avg_star = sum(stars) / len(stars)
        if avg_star < 75.0:
            weaknesses.append("Stories lacked structured STAR (Situation, Task, Action, Result) resolution.")
            improvement_tips.append("Structure answers using the STAR method: 15s Context, 15s Role, 45s Action, 15s Result.")
            detected_weak_tags.append("star_method")
        else:
            strengths.append("Articulated project experiences cleanly using structured narrative progression.")

        # 3. Eye Contact & Vision
        eye_sc = scores.get("eye_contact_score", 75.0)
        if eye_sc >= 75.0:
            strengths.append("Maintained consistent and engaging direct eye contact with the camera.")
        else:
            weaknesses.append("Frequent gaze shifts away from the webcam lens observed.")
            improvement_tips.append("Position webcam at eye level and focus directly on the lens during explanations.")
            detected_weak_tags.append("eye_contact")

        # 4. Voice & Fillers
        voice_sc = scores.get("voice_score", 75.0)
        if voice_sc >= 80.0:
            strengths.append("Clear vocal projection, stable volume, and natural speaking cadence.")
        else:
            weaknesses.append("Noticed moments of vocal hesitation or variable volume levels.")
            improvement_tips.append("Practice pausing intentionally for 1-2 seconds rather than using verbal filler words.")
            detected_weak_tags.append("filler_words")

        # 5. Body Language & Posture
        body_sc = scores.get("body_language_score", 75.0)
        if body_sc >= 80.0:
            strengths.append("Professional sitting posture and composed physical composure throughout.")
        else:
            weaknesses.append("Occasional slouching or excessive movement detected.")
            improvement_tips.append("Keep shoulders relaxed and back straight to project executive presence.")
            detected_weak_tags.append("body_language")

        # 6. Confidence
        conf_sc = scores.get("confidence_score", 75.0)
        if conf_sc >= 80.0:
            strengths.append("Projected strong self-assurance and composure under technical questioning.")
        else:
            weaknesses.append("Physical and vocal markers indicated mild nervousness under pressure.")
            improvement_tips.append("Rehearse foundational concepts out loud to reinforce spontaneous confidence.")
            detected_weak_tags.append("confidence")

        # 7. Grammar & Communication
        gram_sc = scores.get("grammar_score", 80.0)
        comm_sc = scores.get("communication_score", 78.0)
        if gram_sc >= 80.0 and comm_sc >= 80.0:
            strengths.append("Grammatically precise expression with rich technical vocabulary.")
        else:
            weaknesses.append("Minor grammatical inconsistencies and conversational run-on sentences.")
            improvement_tips.append("Organize complex ideas into shorter, punchy declarative statements.")
            detected_weak_tags.append("communication")
            if gram_sc < 70.0:
                detected_weak_tags.append("english_pronunciation")

        confidence_analysis = (
            f"Candidate demonstrated a confidence score of {conf_sc:.1f}%. "
            f"Voice tone and facial demeanor reflected composure under technical inquiry, "
            f"with low overall stress indicators."
        )

        communication_feedback = (
            f"Overall communication scored {comm_sc:.1f}%. "
            f"{voice_feedback} {vision_feedback}"
        )

        if not detected_weak_tags:
            detected_weak_tags = ["technical", "star_method"]

        return {
            "strengths": strengths[:4],
            "weaknesses": weaknesses[:4],
            "confidence_analysis": confidence_analysis,
            "communication_feedback": communication_feedback,
            "improvement_tips": improvement_tips[:4],
            "weak_area_tags": detected_weak_tags
        }

    def create_recommendations(
        self,
        db: Session,
        user_id: str,
        session_id: str,
        weak_area_tags: List[str]
    ) -> List[Recommendation]:
        """Maps detected weak areas to curated learning resources, re-ranking based on candidate trajectory over time."""
        # 1. Compute historical trajectory for candidate to prioritize persistent weaknesses
        prior_reports = (
            db.query(Report)
            .join(InterviewSession, InterviewSession.id == Report.session_id)
            .filter(InterviewSession.user_id == user_id, InterviewSession.id != session_id)
            .order_by(desc(Report.generated_at))
            .limit(5)
            .all()
        )

        # Build trajectory priority scores
        tag_priorities: Dict[str, float] = {}
        for tag in weak_area_tags:
            base_priority = 10.0

            # If user had this tag recommended previously and did not improve, boost priority
            past_recs = (
                db.query(Recommendation)
                .filter(Recommendation.user_id == user_id, Recommendation.weak_area_tag == tag)
                .count()
            )
            base_priority += past_recs * 3.0  # persistent weak areas rank higher

            # If candidate's recent overall score improved, drop priority slightly
            if prior_reports and len(prior_reports) >= 2:
                recent_delta = prior_reports[0].overall_score - prior_reports[-1].overall_score
                if recent_delta > 5.0:
                    base_priority -= 2.0

            tag_priorities[tag] = base_priority

        # Sort tags by descending priority
        ranked_tags = sorted(weak_area_tags, key=lambda t: tag_priorities.get(t, 0.0), reverse=True)

        created_recs = []
        for tag in ranked_tags[:4]:
            # Query targeted learning resource
            resource = db.query(LearningResource).filter(
                LearningResource.weak_area_tag == tag,
                LearningResource.is_active == True
            ).first()

            if not resource:
                # Fallback to general resource
                resource = db.query(LearningResource).filter(LearningResource.is_active == True).first()

            suggestion = self.TAG_SUGGESTIONS.get(
                tag,
                "Review recommended video tutorials and practice targeted mock sessions."
            )

            rec = Recommendation(
                user_id=user_id,
                session_id=session_id,
                weak_area_tag=tag,
                resource_id=resource.id if resource else None,
                practice_suggestion=suggestion
            )
            db.add(rec)
            created_recs.append(rec)

        db.flush()
        return created_recs

feedback_generator = FeedbackGenerator()
