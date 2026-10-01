import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Based Mock Interview Preparation System"
    PROJECT_ID: str = "GIMS-BSSE-F202206"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    
    # Security & Tokens
    SECRET_KEY: str = "gims-bsse-f202206-super-secret-key-change-in-production-min32bytes"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite:///./mock_interview.db"
    
    # First Admin Account
    FIRST_ADMIN_EMAIL: str = "admin@gims.edu.pk"
    FIRST_ADMIN_PASSWORD: str = "AdminSecurePassword123!"
    FIRST_ADMIN_NAME: str = "System Administrator"
    
    # AI Providers & Keys
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    WHISPER_MODEL_SIZE: str = "base"
    LANGUAGETOOL_URL: str = "https://api.languagetoolplus.com/v2"
    YOUTUBE_API_KEY: str = ""
    
    # Storage
    STORAGE_DIR: str = "./storage"
    STORAGE_TYPE: str = "local"  # 'local' | 's3'
    S3_ENDPOINT_URL: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET_NAME: str = "mock-interview"
    MAX_UPLOAD_SIZE_MB: int = 100
    
    # Worker & Maintenance
    WORKER_CONCURRENCY: int = 2
    MAINTENANCE_MODE: bool = False
    
    # Email / SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "no-reply@gims.edu.pk"
    EMAILS_FROM_NAME: str = "GIMS AI Mock Interview"
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

settings = Settings()
