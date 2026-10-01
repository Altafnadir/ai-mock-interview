import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.db.base import Base

# Calculate project root (d:\ai-mock-interview)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

database_url = settings.DATABASE_URL
connect_args = {}

if database_url.startswith("sqlite"):
    # If it is a relative sqlite path like sqlite:///./mock_interview.db, anchor it to PROJECT_ROOT
    if database_url.startswith("sqlite:///./") or database_url.startswith("sqlite:////"):
        rel_path = database_url.replace("sqlite:///./", "").replace("sqlite:////", "")
        abs_db_path = os.path.join(PROJECT_ROOT, rel_path).replace("\\", "/")
        database_url = f"sqlite:///{abs_db_path}"
    
    connect_args["check_same_thread"] = False
    engine = create_engine(
        database_url,
        connect_args=connect_args,
        echo=False
    )
else:
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    import app.db.models  # ensure models imported
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
