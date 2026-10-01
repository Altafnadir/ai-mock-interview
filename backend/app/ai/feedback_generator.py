import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.resource import LearningResource
from app.db.models.report import Recommendation

logger = logging.getLogger(__name__)

class FeedbackGenerator:
    """Synthesizes candidate qualitative evaluation, strengths, weaknesses, and maps targeted learning resources."""

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
        weak_tags = []

        # 1. Content & Technical
        if scores["content_score"] >= 80.0:
            strengths.append(f"Demonstrated solid technical depth and problem-solving relevant to {role_name}.")
        else:
            weaknesses.append("Answers were occasionally brief or omitted key architectural/domain terminology.")
            improvement_tips.append("Structure answers using the STAR method: Situation, Task, Action, and quantifiable Result.")
            weak_tags.append("star_method")

        # 2. Eye Contact & Vision
        if scores["eye_contact_score"] >= 75.0:
            strengths.append("Maintained consistent and engaging direct eye contact with the camera.")
        else:
            weaknesses.append("Frequent gaze shifts away from the webcam lens observed.")
            improvement_tips.append("Position webcam at eye level and focus directly on the lens during explanations.")
            weak_tags.append("eye_contact")

        # 3. Voice & Delivery
        if scores["voice_score"] >= 80.0:
            strengths.append("Clear vocal projection, stable volume, and natural speaking cadence.")
        else:
            weaknesses.append("Noticed moments of vocal hesitation and variable microphone distance.")
            improvement_tips.append("Practice pausing intentionally for 1-2 seconds rather than using verbal filler words.")
            weak_tags.append("filler_words")

        # 4. Body Language & Posture
        if scores["body_language_score"] >= 80.0:
            strengths.append("Professional sitting posture and composed physical composure throughout.")
        else:
            weaknesses.append("Occasional slouching or excessive movement detected.")
            improvement_tips.append("Keep shoulders relaxed and back straight to project executive presence.")
            weak_tags.append("body_language")

        # 5. Grammar & Communication
        if scores["grammar_score"] >= 80.0:
            strengths.append("Grammatically precise expression with rich technical vocabulary.")
        else:
            weaknesses.append("Minor grammatical inconsistencies and conversational run-on sentences.")
            improvement_tips.append("Organize complex ideas into shorter, punchy declarative statements.")
            weak_tags.append("communication")

        confidence_analysis = (
            f"Candidate demonstrated a confidence score of {scores['confidence_score']}%. "
            f"Voice tone and facial demeanor reflected composure under technical inquiry, "
            f"with low overall stress indicators."
        )

        communication_feedback = (
            f"Overall communication scored {scores['communication_score']}%. "
            f"{voice_feedback} {vision_feedback}"
        )

        if not weak_tags:
            weak_tags = ["system_design", "mock_interview"]

        return {
            "strengths": strengths[:4],
            "weaknesses": weaknesses[:4],
            "confidence_analysis": confidence_analysis,
            "communication_feedback": communication_feedback,
            "improvement_tips": improvement_tips[:4],
            "weak_area_tags": weak_tags
        }

    def create_recommendations(
        self,
        db: Session,
        user_id: str,
        session_id: str,
        weak_area_tags: List[str]
    ) -> List[Recommendation]:
        """Maps detected weak areas to curated learning resources in the database."""
        created_recs = []

        for tag in weak_area_tags:
            # Find relevant learning resource
            resource = db.query(LearningResource).filter(
                LearningResource.weak_area_tag == tag,
                LearningResource.is_active == True
            ).first()

            if not resource:
                # Fallback to general resource
                resource = db.query(LearningResource).filter(LearningResource.is_active == True).first()

            suggestion_map = {
                "star_method": "Practice structuring answers with Situation, Task, Action, Result framework.",
                "eye_contact": "Practice looking directly into the camera lens when presenting technical solutions.",
                "filler_words": "Practice using 1-second silent pauses instead of 'um' and 'like'.",
                "body_language": "Maintain an open, upright posture to project confidence in remote interviews.",
                "communication": "Review technical communication conciseness and declarative sentence delivery.",
                "system_design": "Review system design fundamentals, database indexing, and scaling strategies."
            }

            suggestion = suggestion_map.get(tag, "Review recommended video tutorials and practice targeted mock sessions.")

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
