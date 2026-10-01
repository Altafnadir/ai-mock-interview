import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.interview import JobRole, InterviewCategory, DifficultyLevel
from app.db.models.system import SystemSetting
from app.core.logging import logger

JOB_ROLES = [
    {"name": "Frontend Developer", "description": "Specializes in client-side web technologies, UI/UX implementation, React, JavaScript/TypeScript, CSS, and web performance."},
    {"name": "Backend Developer", "description": "Focuses on server-side architecture, APIs, microservices, databases, authentication, and distributed systems."},
    {"name": "Full Stack Developer", "description": "Proficient in end-to-end web engineering, from database design and backend services to responsive frontend user interfaces."},
    {"name": "Software Engineer", "description": "Generalist core computer science role emphasizing algorithms, data structures, OOP, clean code, design patterns, and system design."},
    {"name": "QA Engineer", "description": "Responsible for quality assurance, automated test suites (Selenium, Cypress, PyTest), CI/CD testing pipelines, and bug lifecycle."},
    {"name": "Data Analyst", "description": "Analyzes datasets, creates BI dashboards, writes advanced SQL queries, and derives statistical business insights using Python and visualization tools."},
    {"name": "Cybersecurity Analyst", "description": "Protects IT systems, identifies network vulnerabilities, enforces security policies, conducts penetration tests, and handles incident response."},
    {"name": "Mobile App Developer", "description": "Develops native and cross-platform mobile apps for iOS and Android using React Native, Flutter, Kotlin, or Swift."},
    {"name": "DevOps Engineer", "description": "Builds and manages CI/CD pipelines, container orchestration with Kubernetes/Docker, cloud infrastructure (AWS/GCP/Azure), and monitoring."},
    {"name": "AI/ML Engineer", "description": "Develops machine learning models, deep neural networks, LLM integrations, NLP pipelines, and computer vision systems."},
    {"name": "Business Analyst", "description": "Bridges business goals and technology, gathers technical requirements, models workflows, and facilitates stakeholder communication."}
]

CATEGORIES = [
    {"name": "HR", "description": "Human Resources & Cultural Fit: motivation, teamwork, conflict resolution, work ethic, and company alignment."},
    {"name": "Technical", "description": "Technical & Coding: domain-specific knowledge, architecture, problem-solving, and technology stack mastery."},
    {"name": "Behavioral", "description": "Behavioral & Situational: past experiences, leadership, adaptability, STAR method responses."},
    {"name": "Mixed", "description": "Comprehensive blend of HR, Technical, and Behavioral questions tailored to the target job role."}
]

DIFFICULTIES = [
    {"name": "Beginner", "description": "Entry-level candidates, fresh graduates, and junior positions (0-2 years experience)."},
    {"name": "Intermediate", "description": "Mid-level practitioners with proven project delivery (2-5 years experience)."},
    {"name": "Advanced", "description": "Senior engineers, leads, and architects (5+ years experience) tackling deep design and scale."}
]

SYSTEM_SETTINGS = [
    {
        "key": "scoring_weights",
        "value": {
            "content": 0.25,
            "communication": 0.15,
            "voice": 0.15,
            "grammar": 0.10,
            "eye_contact": 0.10,
            "body_language": 0.10,
            "confidence": 0.15
        },
        "description": "Default weighting matrix for aggregate interview performance scoring."
    },
    {
        "key": "interview_limits",
        "value": {
            "max_questions": 15,
            "default_questions": 5,
            "max_duration_seconds": 3600,
            "default_time_limit_per_question": 120
        },
        "description": "Operational constraints for interview sessions."
    },
    {
        "key": "maintenance_mode",
        "value": {
            "enabled": False,
            "message": "System is undergoing planned maintenance. Please check back shortly."
        },
        "description": "Platform global maintenance switch."
    }
]

def seed_meta(db: Session = None):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        # Seed Job Roles
        for role_data in JOB_ROLES:
            existing = db.query(JobRole).filter(JobRole.name == role_data["name"]).first()
            if not existing:
                role = JobRole(name=role_data["name"], description=role_data["description"], is_active=True)
                db.add(role)

        # Seed Categories
        for cat_data in CATEGORIES:
            existing = db.query(InterviewCategory).filter(InterviewCategory.name == cat_data["name"]).first()
            if not existing:
                cat = InterviewCategory(name=cat_data["name"], description=cat_data["description"], is_active=True)
                db.add(cat)

        # Seed Difficulties
        for diff_data in DIFFICULTIES:
            existing = db.query(DifficultyLevel).filter(DifficultyLevel.name == diff_data["name"]).first()
            if not existing:
                diff = DifficultyLevel(name=diff_data["name"])
                db.add(diff)

        # Seed System Settings
        for setting_data in SYSTEM_SETTINGS:
            existing = db.query(SystemSetting).filter(SystemSetting.key == setting_data["key"]).first()
            if not existing:
                setting = SystemSetting(
                    key=setting_data["key"],
                    value=setting_data["value"],
                    description=setting_data["description"]
                )
                db.add(setting)

        db.commit()
        print("Meta data (11 Job Roles, 4 Categories, 3 Difficulties, System Settings) seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding meta: {e}")
        raise
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_meta()
