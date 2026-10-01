import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.session import SessionLocal, init_db
from app.scripts.seed_meta import seed_meta
from app.scripts.seed_admin import seed_admin
from app.scripts.seed_questions import seed_questions
from app.scripts.seed_resources import seed_resources
from app.scripts.seed_feedback_templates import seed_feedback_templates
from app.scripts.seed_demo import seed_demo

def run_all_seeds():
    print("=" * 60)
    print("AI-Based Mock Interview Preparation System - Master Database Seeder")
    print("Project ID: GIMS-BSSE-F202206 (PMAS-Arid Agriculture University)")
    print("=" * 60)

    # Ensure all tables exist
    init_db()

    db = SessionLocal()
    try:
        print("\n[1/6] Seeding Metadata (Roles, Categories, Difficulties, Settings)...")
        seed_meta(db)

        print("\n[2/6] Seeding Admin User...")
        seed_admin(db)

        print("\n[3/6] Seeding Interview Questions Bank (120+ questions)...")
        seed_questions(db)

        print("\n[4/6] Seeding Learning Resources (YouTube guides by weak area)...")
        seed_resources(db)

        print("\n[5/6] Seeding Feedback Templates...")
        seed_feedback_templates(db)

        print("\n[6/6] Seeding Demo Candidate Account with Sample Analyzed Sessions...")
        seed_demo(db)

        print("\n" + "=" * 60)
        print("ALL SEED DATA INITIALIZED SUCCESSFULLY!")
        print("=" * 60)
    except Exception as e:
        print(f"\nFATAL: Database seeding failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_all_seeds()
