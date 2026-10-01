import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.resource import FeedbackTemplate

TEMPLATES_DATA = [
    # Overall Score Bands
    {"area": "overall", "min_score": 85.0, "max_score": 100.0, "template_text": "Exceptional performance! You demonstrated outstanding technical depth, strong composure, clear articulation, and compelling STAR method storytelling."},
    {"area": "overall", "min_score": 70.0, "max_score": 84.9, "template_text": "Good interview presence. Your technical knowledge is solid and communication is clear, with minor opportunities to tighten structure and eliminate residual filler words."},
    {"area": "overall", "min_score": 50.0, "max_score": 69.9, "template_text": "Satisfactory foundation, but needs improvement. Focus on maintaining steady eye contact, providing more concrete examples in behavioral questions, and practicing calm vocal pacing."},
    {"area": "overall", "min_score": 0.0, "max_score": 49.9, "template_text": "Needs significant practice. Work on core fundamentals: review target role keywords, adopt the STAR framework for structured responses, and practice webcam posture and vocal fluency drills."},

    # Voice / Speech
    {"area": "voice", "min_score": 80.0, "max_score": 100.0, "template_text": "Excellent vocal pacing (130-160 WPM), strong pitch variation, and natural pauses that emphasize key architectural concepts."},
    {"area": "voice", "min_score": 60.0, "max_score": 79.9, "template_text": "Good vocal clarity, but occasional rushed segments or monotone deliveries when tackling complex questions. Inhale deeply and pause before starting complex answers."},
    {"area": "voice", "min_score": 0.0, "max_score": 59.9, "template_text": "Vocal pace was either too fast or heavily broken by hesitation pauses and filler words. Practice speaking aloud with a metronome and replace verbal crutches with silent pauses."},

    # Vision / Eye Contact / Posture
    {"area": "vision", "min_score": 80.0, "max_score": 100.0, "template_text": "Superb non-verbal presence. Steady webcam eye contact (>80%), upright sitting posture, and controlled head movements radiate confidence."},
    {"area": "vision", "min_score": 60.0, "max_score": 79.9, "template_text": "Moderate eye contact. Tendency to look down or away during cognitive retrieval. Place the camera closer to eye level and remember to look at the lens."},
    {"area": "vision", "min_score": 0.0, "max_score": 59.9, "template_text": "Significant slouching or frequent downward glances observed. Adjust desk ergonomics, position camera at eye height, and practice keeping your shoulders squared."},

    # Grammar & Communication
    {"area": "grammar", "min_score": 80.0, "max_score": 100.0, "template_text": "Rich vocabulary, precise technical terminology, and clean sentence structures throughout your responses."},
    {"area": "grammar", "min_score": 60.0, "max_score": 79.9, "template_text": "Clear language with minor grammatical slips or repetitive verb usage. Expand active technical verbs to strengthen response impact."},
    {"area": "grammar", "min_score": 0.0, "max_score": 59.9, "template_text": "Multiple grammatical inconsistencies and run-on sentences noted. Focus on speaking in concise, complete sentences with clear topic statements."},

    # Content / Technical Accuracy
    {"area": "content", "min_score": 80.0, "max_score": 100.0, "template_text": "Comprehensive technical accuracy. Expected keywords were naturally integrated and STAR structure was followed with measurable results."},
    {"area": "content", "min_score": 60.0, "max_score": 79.9, "template_text": "Good conceptual understanding, but answers occasionally lacked specific technical metrics or skipped the 'Result' phase of the STAR framework."},
    {"area": "content", "min_score": 0.0, "max_score": 59.9, "template_text": "Answers were vague or missed critical domain keywords. Ensure you review the fundamental architecture and lifecycle concepts for this job role."}
]

def seed_feedback_templates(db: Session = None):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        count = 0
        for t_data in TEMPLATES_DATA:
            existing = db.query(FeedbackTemplate).filter(
                FeedbackTemplate.area == t_data["area"],
                FeedbackTemplate.min_score == t_data["min_score"],
                FeedbackTemplate.max_score == t_data["max_score"]
            ).first()
            if not existing:
                t = FeedbackTemplate(
                    area=t_data["area"],
                    min_score=t_data["min_score"],
                    max_score=t_data["max_score"],
                    template_text=t_data["template_text"]
                )
                db.add(t)
                count += 1

        db.commit()
        total = db.query(FeedbackTemplate).count()
        print(f"Feedback templates seeded: {count} new templates added. Total in database: {total}.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding feedback templates: {e}")
        raise
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_feedback_templates()
