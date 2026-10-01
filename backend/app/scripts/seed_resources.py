import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.resource import LearningResource

RESOURCES_DATA = [
    # Eye Contact
    {
        "title": "How to Maintain Good Eye Contact in Virtual and In-Person Interviews",
        "url": "https://www.youtube.com/watch?v=3mJ7k0d1aJk",
        "platform": "youtube",
        "weak_area_tag": "eye_contact",
        "difficulty": "All"
    },
    {
        "title": "Webcam Eye Contact Mastery: Where to Look During Video Interviews",
        "url": "https://www.youtube.com/watch?v=kYv9G_k2eRw",
        "platform": "youtube",
        "weak_area_tag": "eye_contact",
        "difficulty": "Beginner"
    },
    {
        "title": "The Psychology of Eye Contact: Radiate Confidence Without Staring",
        "url": "https://www.youtube.com/watch?v=KzKkM6Wl1kI",
        "platform": "youtube",
        "weak_area_tag": "eye_contact",
        "difficulty": "Intermediate"
    },

    # Body Language & Posture
    {
        "title": "Your Body Language May Shape Who You Are | Amy Cuddy | TED",
        "url": "https://www.youtube.com/watch?v=Ks-_Mh1QhMc",
        "platform": "youtube",
        "weak_area_tag": "body_language",
        "difficulty": "All"
    },
    {
        "title": "Nonverbal Communication in Job Interviews: Gestures and Presence",
        "url": "https://www.youtube.com/watch?v=1evw4YSq5m8",
        "platform": "youtube",
        "weak_area_tag": "body_language",
        "difficulty": "Intermediate"
    },
    {
        "title": "Interview Body Language Mistakes to Avoid (Slouching, Fidgeting)",
        "url": "https://www.youtube.com/watch?v=3g8KkWaV5mQ",
        "platform": "youtube",
        "weak_area_tag": "body_language",
        "difficulty": "Beginner"
    },
    {
        "title": "Ergonomics & Sitting Posture for Video Conferences",
        "url": "https://www.youtube.com/watch?v=4Y2wV2uL_K4",
        "platform": "youtube",
        "weak_area_tag": "posture",
        "difficulty": "All"
    },
    {
        "title": "How to Sit Up Straight and Avoid Slouching Under Pressure",
        "url": "https://www.youtube.com/watch?v=5rNkWyP4e9g",
        "platform": "youtube",
        "weak_area_tag": "posture",
        "difficulty": "Beginner"
    },
    {
        "title": "Correcting Forward Head Posture for Professional Webcam Presence",
        "url": "https://www.youtube.com/watch?v=7Yw9x3eM1jA",
        "platform": "youtube",
        "weak_area_tag": "posture",
        "difficulty": "Intermediate"
    },

    # Communication & STAR Method
    {
        "title": "Master the STAR Method for Behavioral Interview Questions",
        "url": "https://www.youtube.com/watch?v=uG36dZp5j7g",
        "platform": "youtube",
        "weak_area_tag": "star_method",
        "difficulty": "All"
    },
    {
        "title": "STAR Method Examples: Situation, Task, Action, Result Detailed Breakdown",
        "url": "https://www.youtube.com/watch?v=0kF1R3i8nQw",
        "platform": "youtube",
        "weak_area_tag": "star_method",
        "difficulty": "Intermediate"
    },
    {
        "title": "How to Structure Powerful Behavioral Stories (Amazon Leadership Principles)",
        "url": "https://www.youtube.com/watch?v=p4f4Yg6v4bQ",
        "platform": "youtube",
        "weak_area_tag": "star_method",
        "difficulty": "Advanced"
    },
    {
        "title": "How to Speak Clearly and Concisely in Professional Interviews",
        "url": "https://www.youtube.com/watch?v=kYv9G_k2eRw",
        "platform": "youtube",
        "weak_area_tag": "communication",
        "difficulty": "All"
    },
    {
        "title": "Executive Communication Skills: Framing Your Thoughts on the Spot",
        "url": "https://www.youtube.com/watch?v=3g8KkWaV5mQ",
        "platform": "youtube",
        "weak_area_tag": "communication",
        "difficulty": "Advanced"
    },
    {
        "title": "Active Listening Techniques for Interview Success",
        "url": "https://www.youtube.com/watch?v=t2z9MDZ1q7g",
        "platform": "youtube",
        "weak_area_tag": "communication",
        "difficulty": "Beginner"
    },

    # Filler Words & Voice
    {
        "title": "How to Stop Saying 'Um', 'Uh', and 'Like' When You Speak",
        "url": "https://www.youtube.com/watch?v=p1t3F4p1A8c",
        "platform": "youtube",
        "weak_area_tag": "filler_words",
        "difficulty": "All"
    },
    {
        "title": "Replace Filler Words with Confident Pauses",
        "url": "https://www.youtube.com/watch?v=9j7hK8m5y2k",
        "platform": "youtube",
        "weak_area_tag": "filler_words",
        "difficulty": "Intermediate"
    },
    {
        "title": "Drills to Eliminate Verbal Crutches in High-Stakes Presentations",
        "url": "https://www.youtube.com/watch?v=6v4Yg6v4bQ1",
        "platform": "youtube",
        "weak_area_tag": "filler_words",
        "difficulty": "Advanced"
    },

    # Confidence
    {
        "title": "How to Build Unshakeable Interview Confidence | Stanford GSB",
        "url": "https://www.youtube.com/watch?v=HAnw168huqA",
        "platform": "youtube",
        "weak_area_tag": "confidence",
        "difficulty": "All"
    },
    {
        "title": "Overcoming Impostor Syndrome and Pre-Interview Anxiety",
        "url": "https://www.youtube.com/watch?v=ZkwqZfvahFw",
        "platform": "youtube",
        "weak_area_tag": "confidence",
        "difficulty": "Intermediate"
    },
    {
        "title": "Vocal Warmups for Confidence, Projection, and Resonant Tone",
        "url": "https://www.youtube.com/watch?v=Yp9lW3A1jK0",
        "platform": "youtube",
        "weak_area_tag": "confidence",
        "difficulty": "Beginner"
    },

    # English Pronunciation & Grammar
    {
        "title": "English Pronunciation for Tech Interviews: Clear Enunciation & Cadence",
        "url": "https://www.youtube.com/watch?v=p3F4A8k1j9q",
        "platform": "youtube",
        "weak_area_tag": "english_pronunciation",
        "difficulty": "All"
    },
    {
        "title": "Mastering English Intonation and Sentence Stress for Interviews",
        "url": "https://www.youtube.com/watch?v=7Yw9x3eM1jB",
        "platform": "youtube",
        "weak_area_tag": "english_pronunciation",
        "difficulty": "Intermediate"
    },
    {
        "title": "Pacing and Articulation: Speaking with Rhythm and Clarity",
        "url": "https://www.youtube.com/watch?v=1evw4YSq5m9",
        "platform": "youtube",
        "weak_area_tag": "english_pronunciation",
        "difficulty": "Beginner"
    },
    {
        "title": "Common Professional English Grammar Mistakes in Interviews",
        "url": "https://www.youtube.com/watch?v=8m5y2k9j7hK",
        "platform": "youtube",
        "weak_area_tag": "grammar",
        "difficulty": "All"
    },
    {
        "title": "Elevating Your Vocabulary: Replacing Basic Verbs with Action Verbs",
        "url": "https://www.youtube.com/watch?v=4Y2wV2uL_K5",
        "platform": "youtube",
        "weak_area_tag": "grammar",
        "difficulty": "Intermediate"
    },
    {
        "title": "Sentence Structure Mastery: Cohesion and Transition Words",
        "url": "https://www.youtube.com/watch?v=5rNkWyP4e9h",
        "platform": "youtube",
        "weak_area_tag": "grammar",
        "difficulty": "Advanced"
    },

    # Technical
    {
        "title": "How to Structure Technical Coding and System Design Answers",
        "url": "https://www.youtube.com/watch?v=Gg35i_9hG6o",
        "platform": "youtube",
        "weak_area_tag": "technical",
        "difficulty": "All"
    },
    {
        "title": "System Design Interview: Step by Step Guide for Software Engineers",
        "url": "https://www.youtube.com/watch?v=i7twT3x5yv8",
        "platform": "youtube",
        "weak_area_tag": "technical",
        "difficulty": "Advanced"
    },
    {
        "title": "Explaining Complex Technical Architecture to Non-Technical Interviewers",
        "url": "https://www.youtube.com/watch?v=4bQ16v4Yg6v",
        "platform": "youtube",
        "weak_area_tag": "technical",
        "difficulty": "Intermediate"
    }
]

def seed_resources(db: Session = None):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        count = 0
        for res_data in RESOURCES_DATA:
            existing = db.query(LearningResource).filter(LearningResource.title == res_data["title"]).first()
            if not existing:
                res = LearningResource(
                    title=res_data["title"],
                    url=res_data["url"],
                    platform=res_data["platform"],
                    weak_area_tag=res_data["weak_area_tag"],
                    difficulty=res_data["difficulty"],
                    is_active=True
                )
                db.add(res)
                count += 1

        db.commit()
        total = db.query(LearningResource).count()
        print(f"Learning resources seeded: {count} new resources added. Total in database: {total}.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding resources: {e}")
        raise
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_resources()
