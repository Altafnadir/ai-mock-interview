import sqlite3
import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("backend"))

from app.core.config import settings

def run_migration():
    paths = [
        os.path.abspath("mock_interview.db"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../mock_interview.db")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../mock_interview.db")),
    ]
    seen = set()
    for db_path in paths:
        if db_path in seen or not os.path.exists(db_path):
            continue
        seen.add(db_path)
        print(f"Migrating database at: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Helper to add column if it doesn't exist
        def add_column_if_missing(table, col_name, col_type):
            cursor.execute(f"PRAGMA table_info({table})")
            cols = [row[1] for row in cursor.fetchall()]
            if col_name not in cols:
                print(f"Adding column {col_name} ({col_type}) to {table} in {db_path}...")
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}")

            # 1. resume_analyses
            add_column_if_missing("resume_analyses", "resume_score", "REAL DEFAULT 85.0")
            add_column_if_missing("resume_analyses", "top_skills", "JSON DEFAULT '[]'")
            add_column_if_missing("resume_analyses", "years_experience", "REAL DEFAULT 2.0")
            add_column_if_missing("resume_analyses", "projects_count", "INTEGER DEFAULT 3")
            add_column_if_missing("resume_analyses", "strengths", "JSON DEFAULT '[]'")
            add_column_if_missing("resume_analyses", "areas_to_improve", "JSON DEFAULT '[]'")

            # 2. analysis_voice
            add_column_if_missing("analysis_voice", "volume_score", "REAL DEFAULT 85.0")
            add_column_if_missing("analysis_voice", "pitch_score", "REAL DEFAULT 82.0")
            add_column_if_missing("analysis_voice", "pace_score", "REAL DEFAULT 85.0")
            add_column_if_missing("analysis_voice", "pronunciation_score", "REAL DEFAULT 84.0")
            add_column_if_missing("analysis_voice", "filler_score", "REAL DEFAULT 92.0")
            add_column_if_missing("analysis_voice", "clarity_label", "VARCHAR(50) DEFAULT 'Optimal'")

            # 3. analysis_vision
            add_column_if_missing("analysis_vision", "shoulder_position_score", "REAL DEFAULT 82.0")
            add_column_if_missing("analysis_vision", "head_position_score", "REAL DEFAULT 80.0")
            add_column_if_missing("analysis_vision", "hand_gesture_score", "REAL DEFAULT 78.0")
            add_column_if_missing("analysis_vision", "gaze_consistency_score", "REAL DEFAULT 80.0")
            add_column_if_missing("analysis_vision", "blink_rate_per_min", "REAL DEFAULT 18.0")
            add_column_if_missing("analysis_vision", "blink_label", "VARCHAR(20) DEFAULT 'Normal'")
            add_column_if_missing("analysis_vision", "distraction_score", "REAL DEFAULT 85.0")

            # 4. learning_resources
            add_column_if_missing("learning_resources", "level", "VARCHAR(20) DEFAULT 'Beginner'")
            add_column_if_missing("learning_resources", "thumbnail_url", "VARCHAR(500)")
            add_column_if_missing("learning_resources", "duration_seconds", "INTEGER DEFAULT 600")
            add_column_if_missing("learning_resources", "is_featured", "BOOLEAN DEFAULT 0")
            add_column_if_missing("learning_resources", "view_count", "INTEGER DEFAULT 0")

            # 5. candidate_profiles
            add_column_if_missing("candidate_profiles", "location", "VARCHAR(100)")

            conn.commit()
            conn.close()

    # Now run SQLAlchemy create_all to create any brand new tables (coach, badges, goals, preferences, etc.)
    from app.db.base import Base
    from app.db.session import engine
    import app.db.models  # load all models
    Base.metadata.create_all(bind=engine)
    print("Database tables & columns successfully upgraded!")

if __name__ == "__main__":
    run_migration()
