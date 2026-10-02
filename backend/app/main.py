import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.scheduler import start_scheduler, shutdown_scheduler
from app.db.session import get_db, init_db
from app.db.models.user import User
from app.db.models.interview import Question, InterviewSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info("Initializing database tables...")
    init_db()
    start_scheduler()
    logger.info("Application startup complete.")
    yield
    # Shutdown
    shutdown_scheduler()
    logger.info("Application shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Based Mock Interview Preparation System API (GIMS-BSSE-F202206)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.core.maintenance import MaintenanceMiddleware
from app.core.rate_limit import RateLimitMiddleware

app.add_middleware(MaintenanceMiddleware)
app.add_middleware(RateLimitMiddleware)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """Comprehensive health check checking DB connectivity and storage status"""
    db_status = "connected"
    db_metrics = {}
    try:
        # Check raw query
        db.execute(text("SELECT 1"))
        db_metrics = {
            "total_users": db.query(User).count(),
            "total_questions": db.query(Question).count(),
            "total_sessions": db.query(InterviewSession).count()
        }
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Check storage directories
    storage_ok = True
    storage_subdirs = ["resumes", "recordings", "reports", "posters", "avatars"]
    storage_info = {}
    for sub in storage_subdirs:
        path = os.path.join(settings.STORAGE_DIR, sub)
        os.makedirs(path, exist_ok=True)
        storage_info[sub] = os.path.exists(path)

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "project": settings.PROJECT_NAME,
        "project_id": settings.PROJECT_ID,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "metrics": db_metrics,
        "storage": {
            "root": settings.STORAGE_DIR,
            "status": "ready" if all(storage_info.values()) else "degraded",
            "directories": storage_info
        }
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "project_id": settings.PROJECT_ID,
        "docs": "/docs",
        "health": "/health",
        "api_v1": settings.API_V1_STR
    }

# Mount API v1 Routers
from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/admin/ai-status", tags=["Admin - AI Telemetry"])
def direct_ai_status():
    from app.api.v1.endpoints.admin import get_ai_status
    return get_ai_status()

# Mount Static Storage directory
from fastapi.staticfiles import StaticFiles
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
app.mount("/storage", StaticFiles(directory=settings.STORAGE_DIR), name="storage")

