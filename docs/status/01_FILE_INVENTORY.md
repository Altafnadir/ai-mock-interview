# 01. Complete Project File & Folder Inventory

**Audit Date:** October 2026  
**Auditor Mode:** Full Codebase Inspection (Read-Only)  
**Project:** AI-Based Mock Interview Preparation System  
**Project ID:** GIMS-BSSE-F202206  

---

## 1. Directory Tree Structure

```text
ai-mock-interview/
├── backend
│   ├── alembic
│   │   ├── versions
│   │   │   └── 257b74da89f1_initial_schema_28_tables.py
│   │   ├── env.py
│   │   ├── README
│   │   └── script.py.mako
│   ├── app
│   │   ├── ai
│   │   │   ├── __init__.py
│   │   │   ├── content_evaluator.py
│   │   │   ├── emotion_analyzer.py
│   │   │   ├── feedback_generator.py
│   │   │   ├── filler_detector.py
│   │   │   ├── grammar_analyzer.py
│   │   │   ├── media_normalizer.py
│   │   │   ├── question_generator.py
│   │   │   ├── registry.py
│   │   │   ├── resume_parser.py
│   │   │   ├── scoring_engine.py
│   │   │   ├── stt.py
│   │   │   ├── vision_analyzer.py
│   │   │   └── voice_analyzer.py
│   │   ├── api
│   │   │   └── v1
│   │   │       ├── endpoints
│   │   │       │   ├── admin.py
│   │   │       │   ├── auth.py
│   │   │       │   ├── dashboard.py
│   │   │       │   ├── interviews.py
│   │   │       │   ├── meta.py
│   │   │       │   ├── notifications.py
│   │   │       │   ├── practice.py
│   │   │       │   ├── profile.py
│   │   │       │   ├── reports.py
│   │   │       │   ├── resources.py
│   │   │       │   └── resumes.py
│   │   │       └── api.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── deps.py
│   │   │   ├── logging.py
│   │   │   ├── maintenance.py
│   │   │   ├── rate_limit.py
│   │   │   ├── scheduler.py
│   │   │   └── security.py
│   │   ├── db
│   │   │   ├── models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── analysis.py
│   │   │   │   ├── interview.py
│   │   │   │   ├── report.py
│   │   │   │   ├── resource.py
│   │   │   │   ├── resume.py
│   │   │   │   ├── system.py
│   │   │   │   └── user.py
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── reports
│   │   │   ├── __init__.py
│   │   │   └── pdf_builder.py
│   │   ├── schemas
│   │   │   ├── admin.py
│   │   │   ├── auth.py
│   │   │   ├── dashboard.py
│   │   │   ├── interview.py
│   │   │   ├── profile.py
│   │   │   ├── report.py
│   │   │   ├── resource.py
│   │   │   └── resume.py
│   │   ├── scripts
│   │   │   ├── seed.py
│   │   │   ├── seed_admin.py
│   │   │   ├── seed_demo.py
│   │   │   ├── seed_feedback_templates.py
│   │   │   ├── seed_meta.py
│   │   │   ├── seed_questions.py
│   │   │   └── seed_resources.py
│   │   ├── services
│   │   │   ├── email.py
│   │   │   └── storage.py
│   │   ├── workers
│   │   │   ├── __init__.py
│   │   │   ├── pipeline.py
│   │   │   └── run.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── storage
│   │   ├── avatars
│   │   ├── posters
│   │   ├── recordings
│   │   ├── reports
│   │   │   ├── poster_add947d4-423d-47d4-99b7-3cd4b70971c6.pdf
│   │   │   ├── poster_dbcdc78b-dca0-4525-8f0e-d7e773ff1112.pdf
│   │   │   ├── report_4c61fbf0-a448-47eb-a5c7-fa152670c934.pdf
│   │   │   ├── report_85ef9289-a363-4e26-8890-e9deabd53f30.pdf
│   │   │   ├── report_add947d4-423d-47d4-99b7-3cd4b70971c6.pdf
│   │   │   ├── report_cf5efe63-b257-468d-aa01-975b4a3ea0e4.pdf
│   │   │   ├── report_dbcdc78b-dca0-4525-8f0e-d7e773ff1112.pdf
│   │   │   ├── report_e142b9f6-0d7a-4008-90ae-f83c587407f4.pdf
│   │   │   ├── report_ea2027f4-b7aa-4b72-baf6-d4755e713dcd.pdf
│   │   │   ├── report_f462ff95-0c5e-4ea8-b1e6-0e587a766769.pdf
│   │   │   ├── summary_add947d4-423d-47d4-99b7-3cd4b70971c6.pdf
│   │   │   └── summary_dbcdc78b-dca0-4525-8f0e-d7e773ff1112.pdf
│   │   └── resumes
│   │       ├── 030c26bc-b822-4aea-9332-7c69a912cc7c.pdf
│   │       ├── 5bd182b5-e475-46ec-9115-cf7ab97092f6.pdf
│   │       └── d0dfa971-55fe-4751-8544-1d2e95be8e92.pdf
│   ├── tests
│   │   ├── fixtures
│   │   │   └── sample_resumes
│   │   │       ├── sample_10_cloud_engineer.pdf
│   │   │       ├── sample_1_fullstack.pdf
│   │   │       ├── sample_2_backend.docx
│   │   │       ├── sample_3_frontend.pdf
│   │   │       ├── sample_4_qa_automation.pdf
│   │   │       ├── sample_5_devops.docx
│   │   │       ├── sample_6_mobile_developer.pdf
│   │   │       ├── sample_7_ml_ai_engineer.pdf
│   │   │       ├── sample_8_fresh_graduate.docx
│   │   │       └── sample_9_cybersecurity.pdf
│   │   ├── test_admin.py
│   │   ├── test_ai_pipeline.py
│   │   ├── test_auth.py
│   │   ├── test_dashboard_resources.py
│   │   ├── test_health.py
│   │   ├── test_interviews.py
│   │   ├── test_profile_resume.py
│   │   ├── test_reports.py
│   │   └── test_resume_parser_10_samples.py
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── mock_interview.db
│   ├── pytest.ini
│   └── requirements.txt
├── docs
│   └── status
├── frontend
│   ├── public
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── src
│   │   ├── api
│   │   │   ├── admin.js
│   │   │   ├── auth.js
│   │   │   ├── client.js
│   │   │   ├── dashboard.js
│   │   │   ├── interview.js
│   │   │   ├── notifications.js
│   │   │   ├── profile.js
│   │   │   ├── report.js
│   │   │   ├── resources.js
│   │   │   └── resume.js
│   │   ├── assets
│   │   │   ├── hero.png
│   │   │   ├── react.svg
│   │   │   └── vite.svg
│   │   ├── components
│   │   │   ├── common
│   │   │   │   ├── Badge.jsx
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Card.jsx
│   │   │   │   ├── Input.jsx
│   │   │   │   ├── Loader.jsx
│   │   │   │   ├── Modal.jsx
│   │   │   │   └── Toast.jsx
│   │   │   └── layout
│   │   │       ├── AdminLayout.jsx
│   │   │       ├── AdminSidebar.jsx
│   │   │       ├── CandidateLayout.jsx
│   │   │       ├── CandidateSidebar.jsx
│   │   │       └── Navbar.jsx
│   │   ├── pages
│   │   │   ├── admin
│   │   │   │   ├── AdminDashboardPage.jsx
│   │   │   │   ├── AdminNotificationsPage.jsx
│   │   │   │   ├── AnalyticsPage.jsx
│   │   │   │   ├── ContentManagementPage.jsx
│   │   │   │   ├── MonitoringPage.jsx
│   │   │   │   ├── QuestionManagementPage.jsx
│   │   │   │   ├── ReportManagementPage.jsx
│   │   │   │   ├── ResourcesAdminPage.jsx
│   │   │   │   ├── SecurityBackupPage.jsx
│   │   │   │   ├── SessionManagementPage.jsx
│   │   │   │   └── UserManagementPage.jsx
│   │   │   ├── auth
│   │   │   │   ├── AdminLoginPage.jsx
│   │   │   │   ├── ForgotPasswordPage.jsx
│   │   │   │   ├── LoginPage.jsx
│   │   │   │   ├── OTPVerificationPage.jsx
│   │   │   │   ├── RegisterPage.jsx
│   │   │   │   └── ResetPasswordPage.jsx
│   │   │   ├── candidate
│   │   │   │   ├── DashboardPage.jsx
│   │   │   │   ├── HistoryPage.jsx
│   │   │   │   ├── InterviewRoomPage.jsx
│   │   │   │   ├── InterviewSetupPage.jsx
│   │   │   │   ├── NotificationsPage.jsx
│   │   │   │   ├── PracticePage.jsx
│   │   │   │   ├── ProcessingPage.jsx
│   │   │   │   ├── ProfilePage.jsx
│   │   │   │   ├── ReportPage.jsx
│   │   │   │   ├── ResourcesPage.jsx
│   │   │   │   └── ResumePage.jsx
│   │   │   ├── public
│   │   │   │   └── LandingPage.jsx
│   │   │   └── shared
│   │   │       └── PublicSharedReport.jsx
│   │   ├── routes
│   │   │   ├── AppRoutes.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── RoleRoute.jsx
│   │   ├── store
│   │   │   ├── authStore.js
│   │   │   ├── themeStore.js
│   │   │   └── toastStore.js
│   │   ├── test
│   │   │   ├── auth.test.jsx
│   │   │   ├── interview_room.test.jsx
│   │   │   ├── report.test.jsx
│   │   │   ├── resume.test.jsx
│   │   │   └── setup.js
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .gitignore
│   ├── .oxlintrc.json
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── README.md
│   ├── tailwind.config.js
│   └── vite.config.js
├── storage
│   ├── avatars
│   │   └── .gitkeep
│   ├── backups
│   │   ├── db_backup_20261001_162448.sqlite
│   │   └── db_backup_20261001_220909.sqlite
│   ├── posters
│   │   └── .gitkeep
│   ├── recordings
│   │   ├── .gitkeep
│   │   └── 0230fb58-cdc3-47a6-92f4-0cf6a7dca815.wav
│   ├── reports
│   │   ├── .gitkeep
│   │   ├── poster_1673e2b5-0559-4876-8b43-607f79c98cbd.pdf
│   │   ├── poster_1985abcd-841a-46b9-b90b-64d1c223f944.pdf
│   │   ├── poster_2ab72b4c-96f4-4079-9b65-305d713427a4.pdf
│   │   ├── poster_846d409e-d860-407f-a396-7ca50820881f.pdf
│   │   ├── poster_8588f149-5910-4b89-bd2a-9b558838c57c.pdf
│   │   ├── poster_9fbf544f-2421-4737-a489-29689f9e3326.pdf
│   │   ├── poster_b112e3c2-da8f-4051-b94b-7ecf3bb495e2.pdf
│   │   ├── poster_b4e3720d-37bb-46f0-a9e0-5af9e8cfe62c.pdf
│   │   ├── poster_c737927b-25ea-4022-a050-99e202ad9c36.pdf
│   │   ├── poster_d831aef7-9977-4fa2-bf51-47f26b55d0e2.pdf
│   │   ├── poster_e1c60f65-0a96-49db-9367-39042500827f.pdf
│   │   ├── poster_e2c63066-b7db-475c-8170-900659e8b180.pdf
│   │   ├── report_05195fa2-4552-4cb2-baa2-d68142f32600.pdf
│   │   ├── report_0838c0cb-b471-432e-b16c-7330155f5c69.pdf
│   │   ├── report_0957e99e-0c58-4e66-a007-0264873b5fff.pdf
│   │   ├── report_0ae56c43-e79e-4b39-8fc5-6a0c53447573.pdf
│   │   ├── report_1673e2b5-0559-4876-8b43-607f79c98cbd.pdf
│   │   ├── report_1985abcd-841a-46b9-b90b-64d1c223f944.pdf
│   │   ├── report_1f83a49f-6936-4aef-a12b-31befb956be3.pdf
│   │   ├── report_2ab72b4c-96f4-4079-9b65-305d713427a4.pdf
│   │   ├── report_2c05507b-9479-4a51-b2ae-40ffd9c164ec.pdf
│   │   ├── report_2cb1d5c3-7e5f-43c1-957a-fec1ff2169bd.pdf
│   │   ├── report_37a68695-7e88-4f52-b664-5800804090d9.pdf
│   │   ├── report_49943808-08f5-490a-823a-85a6a632e3c2.pdf
│   │   ├── report_4b4ba76a-6ec3-4d38-b201-570db50974c6.pdf
│   │   ├── report_4fd148b5-eb5f-469f-93cc-694ab1d8a329.pdf
│   │   ├── report_5406739e-60ba-431e-a8fd-ecff83213323.pdf
│   │   ├── report_5b214eaa-aeaf-4e1c-b4d2-b41b4e6db69e.pdf
│   │   ├── report_6619e40d-5c63-446c-9582-3914c1460826.pdf
│   │   ├── report_6af02216-faeb-4411-b5c6-b0d01ef5a5a5.pdf
│   │   ├── report_73edd810-f185-44bf-ac19-b10d612cc468.pdf
│   │   ├── report_73ee6310-9eec-41d2-ac56-6431f76d2541.pdf
│   │   ├── report_7dda2d33-c6ae-4553-969d-63fdc594f0e4.pdf
│   │   ├── report_7e25b2cd-d8d7-4c30-9927-d5f1c8890c01.pdf
│   │   ├── report_80b693c1-9e78-4641-99fb-67e708676c67.pdf
│   │   ├── report_846d409e-d860-407f-a396-7ca50820881f.pdf
│   │   ├── report_8588f149-5910-4b89-bd2a-9b558838c57c.pdf
│   │   ├── report_9fbf544f-2421-4737-a489-29689f9e3326.pdf
│   │   ├── report_b112e3c2-da8f-4051-b94b-7ecf3bb495e2.pdf
│   │   ├── report_b4e3720d-37bb-46f0-a9e0-5af9e8cfe62c.pdf
│   │   ├── report_c737927b-25ea-4022-a050-99e202ad9c36.pdf
│   │   ├── report_d831aef7-9977-4fa2-bf51-47f26b55d0e2.pdf
│   │   ├── report_e1c60f65-0a96-49db-9367-39042500827f.pdf
│   │   ├── report_e2c63066-b7db-475c-8170-900659e8b180.pdf
│   │   ├── report_e4f67341-e4b6-44a2-afa6-6be83fcd211d.pdf
│   │   ├── report_e98a1b06-8999-4ea8-bb4b-173d80a82a10.pdf
│   │   ├── report_ecc70738-8421-4b87-8c64-e7cc755041d1.pdf
│   │   ├── summary_1673e2b5-0559-4876-8b43-607f79c98cbd.pdf
│   │   ├── summary_1985abcd-841a-46b9-b90b-64d1c223f944.pdf
│   │   ├── summary_2ab72b4c-96f4-4079-9b65-305d713427a4.pdf
│   │   ├── summary_846d409e-d860-407f-a396-7ca50820881f.pdf
│   │   ├── summary_8588f149-5910-4b89-bd2a-9b558838c57c.pdf
│   │   ├── summary_9fbf544f-2421-4737-a489-29689f9e3326.pdf
│   │   ├── summary_b112e3c2-da8f-4051-b94b-7ecf3bb495e2.pdf
│   │   ├── summary_b4e3720d-37bb-46f0-a9e0-5af9e8cfe62c.pdf
│   │   ├── summary_c737927b-25ea-4022-a050-99e202ad9c36.pdf
│   │   ├── summary_d831aef7-9977-4fa2-bf51-47f26b55d0e2.pdf
│   │   ├── summary_e1c60f65-0a96-49db-9367-39042500827f.pdf
│   │   └── summary_e2c63066-b7db-475c-8170-900659e8b180.pdf
│   └── resumes
│       └── .gitkeep
├── .env
├── .env.example
├── .gitignore
├── DECISIONS.md
├── docker-compose.yml
├── KNOWN_ISSUES.md
├── mock_interview.db
├── PROGRESS.md
├── pytest.ini
└── REQUIREMENTS_TRACE.md
```

---

## 2. Comprehensive File Inventory Table

| Path | Purpose | Lines of Code | Status |
|:---|:---|:---:|:---:|
| `backend/alembic/versions/257b74da89f1_initial_schema_28_tables.py` | Alembic schema migration revision script | 543 | **COMPLETE** |
| `backend/alembic/env.py` | Alembic migration runtime environment and metadata binding | 65 | **COMPLETE** |
| `backend/alembic/README` | Application source or configuration file | 1 | **COMPLETE** |
| `backend/alembic/script.py.mako` | Application source or configuration file | 28 | **COMPLETE** |
| `backend/app/ai/__init__.py` | AI multimodal analysis module: __init__ | 27 | **COMPLETE** |
| `backend/app/ai/content_evaluator.py` | AI multimodal analysis module: content_evaluator | 221 | **COMPLETE** |
| `backend/app/ai/emotion_analyzer.py` | AI multimodal analysis module: emotion_analyzer | 65 | **COMPLETE** |
| `backend/app/ai/feedback_generator.py` | AI multimodal analysis module: feedback_generator | 219 | **COMPLETE** |
| `backend/app/ai/filler_detector.py` | AI multimodal analysis module: filler_detector | 74 | **COMPLETE** |
| `backend/app/ai/grammar_analyzer.py` | AI multimodal analysis module: grammar_analyzer | 96 | **COMPLETE** |
| `backend/app/ai/media_normalizer.py` | AI multimodal analysis module: media_normalizer | 107 | **COMPLETE** |
| `backend/app/ai/question_generator.py` | AI multimodal analysis module: question_generator | 236 | **COMPLETE** |
| `backend/app/ai/registry.py` | AI multimodal analysis module: registry | 185 | **COMPLETE** |
| `backend/app/ai/resume_parser.py` | AI multimodal analysis module: resume_parser | 403 | **COMPLETE** |
| `backend/app/ai/scoring_engine.py` | AI multimodal analysis module: scoring_engine | 131 | **COMPLETE** |
| `backend/app/ai/stt.py` | AI multimodal analysis module: stt | 42 | **COMPLETE** |
| `backend/app/ai/vision_analyzer.py` | AI multimodal analysis module: vision_analyzer | 154 | **COMPLETE** |
| `backend/app/ai/voice_analyzer.py` | AI multimodal analysis module: voice_analyzer | 180 | **COMPLETE** |
| `backend/app/api/v1/endpoints/admin.py` | API router endpoints for admin domain operations | 997 | **COMPLETE** |
| `backend/app/api/v1/endpoints/auth.py` | API router endpoints for auth domain operations | 537 | **COMPLETE** |
| `backend/app/api/v1/endpoints/dashboard.py` | API router endpoints for dashboard domain operations | 297 | **COMPLETE** |
| `backend/app/api/v1/endpoints/interviews.py` | API router endpoints for interviews domain operations | 563 | **COMPLETE** |
| `backend/app/api/v1/endpoints/meta.py` | API router endpoints for meta domain operations | 37 | **COMPLETE** |
| `backend/app/api/v1/endpoints/notifications.py` | API router endpoints for notifications domain operations | 93 | **COMPLETE** |
| `backend/app/api/v1/endpoints/practice.py` | API router endpoints for practice domain operations | 118 | **COMPLETE** |
| `backend/app/api/v1/endpoints/profile.py` | API router endpoints for profile domain operations | 88 | **COMPLETE** |
| `backend/app/api/v1/endpoints/reports.py` | API router endpoints for reports domain operations | 328 | **COMPLETE** |
| `backend/app/api/v1/endpoints/resources.py` | API router endpoints for resources domain operations | 65 | **COMPLETE** |
| `backend/app/api/v1/endpoints/resumes.py` | API router endpoints for resumes domain operations | 288 | **COMPLETE** |
| `backend/app/api/v1/api.py` | Master API v1 router aggregator combining all sub-routers | 21 | **COMPLETE** |
| `backend/app/core/config.py` | Pydantic BaseSettings application configuration and environment loader | 87 | **COMPLETE** |
| `backend/app/core/deps.py` | FastAPI dependency injections for JWT auth and RBAC roles | 53 | **COMPLETE** |
| `backend/app/core/logging.py` | Structured logging configuration and logger instance setup | 21 | **COMPLETE** |
| `backend/app/core/maintenance.py` | Middleware for platform-wide maintenance mode bypass and 503 response | 31 | **COMPLETE** |
| `backend/app/core/rate_limit.py` | In-memory token-bucket rate limiting middleware for DDoS mitigation | 57 | **COMPLETE** |
| `backend/app/core/scheduler.py` | APScheduler background cron job scheduler for DB backups and cleanup | 137 | **COMPLETE** |
| `backend/app/core/security.py` | Bcrypt password hashing and JWT access/refresh token cryptographic utilities | 57 | **COMPLETE** |
| `backend/app/db/models/__init__.py` | SQLAlchemy ORM database model definitions for __init__ | 82 | **COMPLETE** |
| `backend/app/db/models/analysis.py` | SQLAlchemy ORM database model definitions for analysis | 93 | **COMPLETE** |
| `backend/app/db/models/interview.py` | SQLAlchemy ORM database model definitions for interview | 146 | **COMPLETE** |
| `backend/app/db/models/report.py` | SQLAlchemy ORM database model definitions for report | 70 | **COMPLETE** |
| `backend/app/db/models/resource.py` | SQLAlchemy ORM database model definitions for resource | 36 | **COMPLETE** |
| `backend/app/db/models/resume.py` | SQLAlchemy ORM database model definitions for resume | 43 | **COMPLETE** |
| `backend/app/db/models/system.py` | SQLAlchemy ORM database model definitions for system | 86 | **COMPLETE** |
| `backend/app/db/models/user.py` | SQLAlchemy ORM database model definitions for user | 95 | **COMPLETE** |
| `backend/app/db/base.py` | SQLAlchemy DeclarativeBase base class | 4 | **COMPLETE** |
| `backend/app/db/session.py` | SQLAlchemy engine, sessionmaker, and database initialization helper | 48 | **COMPLETE** |
| `backend/app/reports/__init__.py` | ReportLab PDF generator and formatting engine for __init__ | 1 | **COMPLETE** |
| `backend/app/reports/pdf_builder.py` | ReportLab PDF generator and formatting engine for pdf_builder | 478 | **COMPLETE** |
| `backend/app/schemas/admin.py` | Pydantic validation schemas and request/response DTOs for admin | 239 | **COMPLETE** |
| `backend/app/schemas/auth.py` | Pydantic validation schemas and request/response DTOs for auth | 69 | **COMPLETE** |
| `backend/app/schemas/dashboard.py` | Pydantic validation schemas and request/response DTOs for dashboard | 62 | **COMPLETE** |
| `backend/app/schemas/interview.py` | Pydantic validation schemas and request/response DTOs for interview | 106 | **COMPLETE** |
| `backend/app/schemas/profile.py` | Pydantic validation schemas and request/response DTOs for profile | 53 | **COMPLETE** |
| `backend/app/schemas/report.py` | Pydantic validation schemas and request/response DTOs for report | 52 | **COMPLETE** |
| `backend/app/schemas/resource.py` | Pydantic validation schemas and request/response DTOs for resource | 69 | **COMPLETE** |
| `backend/app/schemas/resume.py` | Pydantic validation schemas and request/response DTOs for resume | 36 | **COMPLETE** |
| `backend/app/scripts/seed.py` | Database seeding and data initialization script for seed | 54 | **COMPLETE** |
| `backend/app/scripts/seed_admin.py` | Database seeding and data initialization script for seed_admin | 51 | **COMPLETE** |
| `backend/app/scripts/seed_demo.py` | Database seeding and data initialization script for seed_demo | 392 | **COMPLETE** |
| `backend/app/scripts/seed_feedback_templates.py` | Database seeding and data initialization script for seed_feedback_templates | 74 | **COMPLETE** |
| `backend/app/scripts/seed_meta.py` | Database seeding and data initialization script for seed_meta | 124 | **COMPLETE** |
| `backend/app/scripts/seed_questions.py` | Database seeding and data initialization script for seed_questions | 803 | **COMPLETE** |
| `backend/app/scripts/seed_resources.py` | Database seeding and data initialization script for seed_resources | 270 | **COMPLETE** |
| `backend/app/services/email.py` | Service layer module for email operations | 118 | **COMPLETE** |
| `backend/app/services/storage.py` | Service layer module for storage operations | 63 | **COMPLETE** |
| `backend/app/workers/__init__.py` | Background task worker and AI processing pipeline module: __init__ | 1 | **COMPLETE** |
| `backend/app/workers/pipeline.py` | Background task worker and AI processing pipeline module: pipeline | 497 | **COMPLETE** |
| `backend/app/workers/run.py` | Background task worker and AI processing pipeline module: run | 132 | **COMPLETE** |
| `backend/app/__init__.py` | Application source or configuration file | 6 | **COMPLETE** |
| `backend/app/main.py` | FastAPI entry point, lifecycle events, security headers, and routes | 120 | **COMPLETE** |
| `backend/storage/reports/poster_add947d4-423d-47d4-99b7-3cd4b70971c6.pdf` | Application source or configuration file | 74 | **CONFIG/ASSET** |
| `backend/storage/reports/poster_dbcdc78b-dca0-4525-8f0e-d7e773ff1112.pdf` | Application source or configuration file | 74 | **CONFIG/ASSET** |
| `backend/storage/reports/report_4c61fbf0-a448-47eb-a5c7-fa152670c934.pdf` | Application source or configuration file | 93 | **CONFIG/ASSET** |
| `backend/storage/reports/report_85ef9289-a363-4e26-8890-e9deabd53f30.pdf` | Application source or configuration file | 93 | **CONFIG/ASSET** |
| `backend/storage/reports/report_add947d4-423d-47d4-99b7-3cd4b70971c6.pdf` | Application source or configuration file | 93 | **CONFIG/ASSET** |
| `backend/storage/reports/report_cf5efe63-b257-468d-aa01-975b4a3ea0e4.pdf` | Application source or configuration file | 93 | **CONFIG/ASSET** |
| `backend/storage/reports/report_dbcdc78b-dca0-4525-8f0e-d7e773ff1112.pdf` | Application source or configuration file | 93 | **CONFIG/ASSET** |
| `backend/storage/reports/report_e142b9f6-0d7a-4008-90ae-f83c587407f4.pdf` | Application source or configuration file | 93 | **CONFIG/ASSET** |
| `backend/storage/reports/report_ea2027f4-b7aa-4b72-baf6-d4755e713dcd.pdf` | Application source or configuration file | 93 | **CONFIG/ASSET** |
| `backend/storage/reports/report_f462ff95-0c5e-4ea8-b1e6-0e587a766769.pdf` | Application source or configuration file | 93 | **CONFIG/ASSET** |
| `backend/storage/reports/summary_add947d4-423d-47d4-99b7-3cd4b70971c6.pdf` | Application source or configuration file | 74 | **CONFIG/ASSET** |
| `backend/storage/reports/summary_dbcdc78b-dca0-4525-8f0e-d7e773ff1112.pdf` | Application source or configuration file | 74 | **CONFIG/ASSET** |
| `backend/storage/resumes/030c26bc-b822-4aea-9332-7c69a912cc7c.pdf` | Application source or configuration file | 74 | **CONFIG/ASSET** |
| `backend/storage/resumes/5bd182b5-e475-46ec-9115-cf7ab97092f6.pdf` | Application source or configuration file | 74 | **CONFIG/ASSET** |
| `backend/storage/resumes/d0dfa971-55fe-4751-8544-1d2e95be8e92.pdf` | Application source or configuration file | 68 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_10_cloud_engineer.pdf` | Standardized benchmark resume fixture for parser verification | 74 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_1_fullstack.pdf` | Standardized benchmark resume fixture for parser verification | 74 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_2_backend.docx` | Standardized benchmark resume fixture for parser verification | 1004 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_3_frontend.pdf` | Standardized benchmark resume fixture for parser verification | 74 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_4_qa_automation.pdf` | Standardized benchmark resume fixture for parser verification | 74 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_5_devops.docx` | Standardized benchmark resume fixture for parser verification | 1007 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_6_mobile_developer.pdf` | Standardized benchmark resume fixture for parser verification | 74 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_7_ml_ai_engineer.pdf` | Standardized benchmark resume fixture for parser verification | 74 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_8_fresh_graduate.docx` | Standardized benchmark resume fixture for parser verification | 1015 | **CONFIG/ASSET** |
| `backend/tests/fixtures/sample_resumes/sample_9_cybersecurity.pdf` | Standardized benchmark resume fixture for parser verification | 74 | **CONFIG/ASSET** |
| `backend/tests/test_admin.py` | Automated pytest test suite for test_admin | 262 | **COMPLETE** |
| `backend/tests/test_ai_pipeline.py` | Automated pytest test suite for test_ai_pipeline | 208 | **COMPLETE** |
| `backend/tests/test_auth.py` | Automated pytest test suite for test_auth | 124 | **COMPLETE** |
| `backend/tests/test_dashboard_resources.py` | Automated pytest test suite for test_dashboard_resources | 177 | **COMPLETE** |
| `backend/tests/test_health.py` | Automated pytest test suite for test_health | 29 | **COMPLETE** |
| `backend/tests/test_interviews.py` | Automated pytest test suite for test_interviews | 202 | **COMPLETE** |
| `backend/tests/test_profile_resume.py` | Automated pytest test suite for test_profile_resume | 139 | **COMPLETE** |
| `backend/tests/test_reports.py` | Automated pytest test suite for test_reports | 117 | **COMPLETE** |
| `backend/tests/test_resume_parser_10_samples.py` | Automated pytest test suite for test_resume_parser_10_samples | 267 | **COMPLETE** |
| `backend/alembic.ini` | Alembic database migration configuration | 149 | **CONFIG/ASSET** |
| `backend/Dockerfile` | Container build definition for FastAPI backend and AI worker | 34 | **COMPLETE** |
| `backend/mock_interview.db` | Application source or configuration file | 606 | **CONFIG/ASSET** |
| `backend/pytest.ini` | Backend-specific pytest configuration | 6 | **CONFIG/ASSET** |
| `backend/requirements.txt` | Pinned Python dependencies for web framework, ORM, and AI packages | 55 | **COMPLETE** |
| `frontend/public/favicon.svg` | Static graphic asset or vector icon | 1 | **CONFIG/ASSET** |
| `frontend/public/icons.svg` | Static graphic asset or vector icon | 24 | **CONFIG/ASSET** |
| `frontend/src/api/admin.js` | Axios API service client module for admin | 70 | **COMPLETE** |
| `frontend/src/api/auth.js` | Axios API service client module for auth | 16 | **COMPLETE** |
| `frontend/src/api/client.js` | Axios API service client module for client | 91 | **COMPLETE** |
| `frontend/src/api/dashboard.js` | Axios API service client module for dashboard | 7 | **COMPLETE** |
| `frontend/src/api/interview.js` | Axios API service client module for interview | 27 | **COMPLETE** |
| `frontend/src/api/notifications.js` | Axios API service client module for notifications | 7 | **COMPLETE** |
| `frontend/src/api/profile.js` | Axios API service client module for profile | 10 | **COMPLETE** |
| `frontend/src/api/report.js` | Axios API service client module for report | 12 | **COMPLETE** |
| `frontend/src/api/resources.js` | Axios API service client module for resources | 9 | **COMPLETE** |
| `frontend/src/api/resume.js` | Axios API service client module for resume | 18 | **COMPLETE** |
| `frontend/src/assets/hero.png` | Static graphic asset or vector icon | 322 | **CONFIG/ASSET** |
| `frontend/src/assets/react.svg` | Static graphic asset or vector icon | 1 | **CONFIG/ASSET** |
| `frontend/src/assets/vite.svg` | Static graphic asset or vector icon | 1 | **CONFIG/ASSET** |
| `frontend/src/components/common/Badge.jsx` | Reusable atomic UI design system component: badge | 30 | **COMPLETE** |
| `frontend/src/components/common/Button.jsx` | Reusable atomic UI design system component: button | 48 | **COMPLETE** |
| `frontend/src/components/common/Card.jsx` | Reusable atomic UI design system component: card | 40 | **COMPLETE** |
| `frontend/src/components/common/Input.jsx` | Reusable atomic UI design system component: input | 61 | **COMPLETE** |
| `frontend/src/components/common/Loader.jsx` | Reusable atomic UI design system component: loader | 34 | **COMPLETE** |
| `frontend/src/components/common/Modal.jsx` | Reusable atomic UI design system component: modal | 55 | **COMPLETE** |
| `frontend/src/components/common/Toast.jsx` | Reusable atomic UI design system component: toast | 43 | **COMPLETE** |
| `frontend/src/components/layout/AdminLayout.jsx` | Navigation and structural layout component: adminlayout | 20 | **COMPLETE** |
| `frontend/src/components/layout/AdminSidebar.jsx` | Navigation and structural layout component: adminsidebar | 63 | **COMPLETE** |
| `frontend/src/components/layout/CandidateLayout.jsx` | Navigation and structural layout component: candidatelayout | 20 | **COMPLETE** |
| `frontend/src/components/layout/CandidateSidebar.jsx` | Navigation and structural layout component: candidatesidebar | 62 | **COMPLETE** |
| `frontend/src/components/layout/Navbar.jsx` | Navigation and structural layout component: navbar | 158 | **COMPLETE** |
| `frontend/src/pages/admin/AdminDashboardPage.jsx` | Administrative console dashboard page: admindashboardpage | 228 | **COMPLETE** |
| `frontend/src/pages/admin/AdminNotificationsPage.jsx` | Administrative console dashboard page: adminnotificationspage | 99 | **COMPLETE** |
| `frontend/src/pages/admin/AnalyticsPage.jsx` | Administrative console dashboard page: analyticspage | 119 | **COMPLETE** |
| `frontend/src/pages/admin/ContentManagementPage.jsx` | Administrative console dashboard page: contentmanagementpage | 174 | **COMPLETE** |
| `frontend/src/pages/admin/MonitoringPage.jsx` | Administrative console dashboard page: monitoringpage | 135 | **COMPLETE** |
| `frontend/src/pages/admin/QuestionManagementPage.jsx` | Administrative console dashboard page: questionmanagementpage | 302 | **COMPLETE** |
| `frontend/src/pages/admin/ReportManagementPage.jsx` | Administrative console dashboard page: reportmanagementpage | 107 | **COMPLETE** |
| `frontend/src/pages/admin/ResourcesAdminPage.jsx` | Administrative console dashboard page: resourcesadminpage | 191 | **COMPLETE** |
| `frontend/src/pages/admin/SecurityBackupPage.jsx` | Administrative console dashboard page: securitybackuppage | 167 | **COMPLETE** |
| `frontend/src/pages/admin/SessionManagementPage.jsx` | Administrative console dashboard page: sessionmanagementpage | 169 | **COMPLETE** |
| `frontend/src/pages/admin/UserManagementPage.jsx` | Administrative console dashboard page: usermanagementpage | 205 | **COMPLETE** |
| `frontend/src/pages/auth/AdminLoginPage.jsx` | Authentication and account management page: adminloginpage | 126 | **COMPLETE** |
| `frontend/src/pages/auth/ForgotPasswordPage.jsx` | Authentication and account management page: forgotpasswordpage | 97 | **COMPLETE** |
| `frontend/src/pages/auth/LoginPage.jsx` | Authentication and account management page: loginpage | 345 | **COMPLETE** |
| `frontend/src/pages/auth/OTPVerificationPage.jsx` | Authentication and account management page: otpverificationpage | 186 | **COMPLETE** |
| `frontend/src/pages/auth/RegisterPage.jsx` | Authentication and account management page: registerpage | 142 | **COMPLETE** |
| `frontend/src/pages/auth/ResetPasswordPage.jsx` | Authentication and account management page: resetpasswordpage | 113 | **COMPLETE** |
| `frontend/src/pages/candidate/DashboardPage.jsx` | Candidate interview portal page: dashboardpage | 335 | **COMPLETE** |
| `frontend/src/pages/candidate/HistoryPage.jsx` | Candidate interview portal page: historypage | 237 | **COMPLETE** |
| `frontend/src/pages/candidate/InterviewRoomPage.jsx` | Candidate interview portal page: interviewroompage | 466 | **COMPLETE** |
| `frontend/src/pages/candidate/InterviewSetupPage.jsx` | Candidate interview portal page: interviewsetuppage | 382 | **COMPLETE** |
| `frontend/src/pages/candidate/NotificationsPage.jsx` | Candidate interview portal page: notificationspage | 129 | **COMPLETE** |
| `frontend/src/pages/candidate/PracticePage.jsx` | Candidate interview portal page: practicepage | 88 | **COMPLETE** |
| `frontend/src/pages/candidate/ProcessingPage.jsx` | Candidate interview portal page: processingpage | 137 | **COMPLETE** |
| `frontend/src/pages/candidate/ProfilePage.jsx` | Candidate interview portal page: profilepage | 263 | **COMPLETE** |
| `frontend/src/pages/candidate/ReportPage.jsx` | Candidate interview portal page: reportpage | 519 | **COMPLETE** |
| `frontend/src/pages/candidate/ResourcesPage.jsx` | Candidate interview portal page: resourcespage | 176 | **COMPLETE** |
| `frontend/src/pages/candidate/ResumePage.jsx` | Candidate interview portal page: resumepage | 297 | **COMPLETE** |
| `frontend/src/pages/public/LandingPage.jsx` | Public marketing and guest landing page: landingpage | 219 | **COMPLETE** |
| `frontend/src/pages/shared/PublicSharedReport.jsx` | Public shared interview report viewing page: publicsharedreport | 129 | **COMPLETE** |
| `frontend/src/routes/AppRoutes.jsx` | Route configuration and security guards: approutes | 125 | **COMPLETE** |
| `frontend/src/routes/ProtectedRoute.jsx` | Route configuration and security guards: protectedroute | 14 | **COMPLETE** |
| `frontend/src/routes/RoleRoute.jsx` | Route configuration and security guards: roleroute | 18 | **COMPLETE** |
| `frontend/src/store/authStore.js` | Zustand reactive client state store for authstore | 39 | **COMPLETE** |
| `frontend/src/store/themeStore.js` | Zustand reactive client state store for themestore | 27 | **COMPLETE** |
| `frontend/src/store/toastStore.js` | Zustand reactive client state store for toaststore | 30 | **COMPLETE** |
| `frontend/src/test/auth.test.jsx` | Vitest frontend component test suite for auth.test | 79 | **COMPLETE** |
| `frontend/src/test/interview_room.test.jsx` | Vitest frontend component test suite for interview_room.test | 57 | **COMPLETE** |
| `frontend/src/test/report.test.jsx` | Vitest frontend component test suite for report.test | 80 | **COMPLETE** |
| `frontend/src/test/resume.test.jsx` | Vitest frontend component test suite for resume.test | 65 | **COMPLETE** |
| `frontend/src/test/setup.js` | Vitest frontend component test suite for setup | 62 | **COMPLETE** |
| `frontend/src/App.css` | Application source or configuration file | 184 | **CONFIG/ASSET** |
| `frontend/src/App.jsx` | React root component binding Router and global Toast notification provider | 13 | **COMPLETE** |
| `frontend/src/index.css` | Global CSS styles, Tailwind directives, dark mode rules, and animations | 41 | **CONFIG/ASSET** |
| `frontend/src/main.jsx` | React 19 DOM bootstrap mounting root component | 10 | **COMPLETE** |
| `frontend/.gitignore` | Application source or configuration file | 24 | **COMPLETE** |
| `frontend/.oxlintrc.json` | Application source or configuration file | 8 | **CONFIG/ASSET** |
| `frontend/Dockerfile` | Multi-stage Dockerfile building Vite React and serving via Nginx | 20 | **COMPLETE** |
| `frontend/index.html` | Single Page Application (SPA) HTML5 entry document | 30 | **CONFIG/ASSET** |
| `frontend/nginx.conf` | Nginx reverse proxy and SPA static routing configuration | 23 | **COMPLETE** |
| `frontend/package-lock.json` | Pinned npm dependency resolution tree | 4274 | **CONFIG/ASSET** |
| `frontend/package.json` | Frontend Node.js project manifest, dependencies, and build scripts | 39 | **CONFIG/ASSET** |
| `frontend/postcss.config.js` | PostCSS configuration for Tailwind CSS compilation | 6 | **COMPLETE** |
| `frontend/README.md` | Application source or configuration file | 16 | **COMPLETE** |
| `frontend/tailwind.config.js` | Tailwind CSS theme tokens, color palettes, and container rules | 35 | **COMPLETE** |
| `frontend/vite.config.js` | Vite bundler configuration with React plugin and test runner setup | 22 | **COMPLETE** |
| `storage/avatars/.gitkeep` | Local file storage directory for resumes, recordings, and reports | 1 | **COMPLETE** |
| `storage/backups/db_backup_20261001_162448.sqlite` | Automated SQLite database snapshot backup archive | 3103 | **CONFIG/ASSET** |
| `storage/backups/db_backup_20261001_220909.sqlite` | Automated SQLite database snapshot backup archive | 3363 | **CONFIG/ASSET** |
| `storage/posters/.gitkeep` | Local file storage directory for resumes, recordings, and reports | 1 | **COMPLETE** |
| `storage/recordings/.gitkeep` | Local file storage directory for resumes, recordings, and reports | 1 | **COMPLETE** |
| `storage/recordings/0230fb58-cdc3-47a6-92f4-0cf6a7dca815.wav` | Local file storage directory for resumes, recordings, and reports | 1 | **COMPLETE** |
| `storage/reports/.gitkeep` | Local file storage directory for resumes, recordings, and reports | 1 | **COMPLETE** |
| `storage/reports/poster_1673e2b5-0559-4876-8b43-607f79c98cbd.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_1985abcd-841a-46b9-b90b-64d1c223f944.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_2ab72b4c-96f4-4079-9b65-305d713427a4.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_846d409e-d860-407f-a396-7ca50820881f.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_8588f149-5910-4b89-bd2a-9b558838c57c.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_9fbf544f-2421-4737-a489-29689f9e3326.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_b112e3c2-da8f-4051-b94b-7ecf3bb495e2.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_b4e3720d-37bb-46f0-a9e0-5af9e8cfe62c.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_c737927b-25ea-4022-a050-99e202ad9c36.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_d831aef7-9977-4fa2-bf51-47f26b55d0e2.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_e1c60f65-0a96-49db-9367-39042500827f.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/poster_e2c63066-b7db-475c-8170-900659e8b180.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/report_05195fa2-4552-4cb2-baa2-d68142f32600.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_0838c0cb-b471-432e-b16c-7330155f5c69.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_0957e99e-0c58-4e66-a007-0264873b5fff.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_0ae56c43-e79e-4b39-8fc5-6a0c53447573.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_1673e2b5-0559-4876-8b43-607f79c98cbd.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_1985abcd-841a-46b9-b90b-64d1c223f944.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_1f83a49f-6936-4aef-a12b-31befb956be3.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_2ab72b4c-96f4-4079-9b65-305d713427a4.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_2c05507b-9479-4a51-b2ae-40ffd9c164ec.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_2cb1d5c3-7e5f-43c1-957a-fec1ff2169bd.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_37a68695-7e88-4f52-b664-5800804090d9.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_49943808-08f5-490a-823a-85a6a632e3c2.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_4b4ba76a-6ec3-4d38-b201-570db50974c6.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_4fd148b5-eb5f-469f-93cc-694ab1d8a329.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_5406739e-60ba-431e-a8fd-ecff83213323.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_5b214eaa-aeaf-4e1c-b4d2-b41b4e6db69e.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_6619e40d-5c63-446c-9582-3914c1460826.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_6af02216-faeb-4411-b5c6-b0d01ef5a5a5.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_73edd810-f185-44bf-ac19-b10d612cc468.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_73ee6310-9eec-41d2-ac56-6431f76d2541.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_7dda2d33-c6ae-4553-969d-63fdc594f0e4.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_7e25b2cd-d8d7-4c30-9927-d5f1c8890c01.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_80b693c1-9e78-4641-99fb-67e708676c67.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_846d409e-d860-407f-a396-7ca50820881f.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_8588f149-5910-4b89-bd2a-9b558838c57c.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_9fbf544f-2421-4737-a489-29689f9e3326.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_b112e3c2-da8f-4051-b94b-7ecf3bb495e2.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_b4e3720d-37bb-46f0-a9e0-5af9e8cfe62c.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_c737927b-25ea-4022-a050-99e202ad9c36.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_d831aef7-9977-4fa2-bf51-47f26b55d0e2.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_e1c60f65-0a96-49db-9367-39042500827f.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_e2c63066-b7db-475c-8170-900659e8b180.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_e4f67341-e4b6-44a2-afa6-6be83fcd211d.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_e98a1b06-8999-4ea8-bb4b-173d80a82a10.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/report_ecc70738-8421-4b87-8c64-e7cc755041d1.pdf` | Local file storage directory for resumes, recordings, and reports | 93 | **CONFIG/ASSET** |
| `storage/reports/summary_1673e2b5-0559-4876-8b43-607f79c98cbd.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_1985abcd-841a-46b9-b90b-64d1c223f944.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_2ab72b4c-96f4-4079-9b65-305d713427a4.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_846d409e-d860-407f-a396-7ca50820881f.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_8588f149-5910-4b89-bd2a-9b558838c57c.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_9fbf544f-2421-4737-a489-29689f9e3326.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_b112e3c2-da8f-4051-b94b-7ecf3bb495e2.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_b4e3720d-37bb-46f0-a9e0-5af9e8cfe62c.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_c737927b-25ea-4022-a050-99e202ad9c36.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_d831aef7-9977-4fa2-bf51-47f26b55d0e2.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_e1c60f65-0a96-49db-9367-39042500827f.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/reports/summary_e2c63066-b7db-475c-8170-900659e8b180.pdf` | Local file storage directory for resumes, recordings, and reports | 74 | **CONFIG/ASSET** |
| `storage/resumes/.gitkeep` | Local file storage directory for resumes, recordings, and reports | 1 | **COMPLETE** |
| `.env` | Local environment configuration and secrets for development | 37 | **COMPLETE** |
| `.env.example` | Template environment variables and reference settings | 57 | **CONFIG/ASSET** |
| `.gitignore` | Git version control file ignore rules | 60 | **COMPLETE** |
| `DECISIONS.md` | Architectural decision records (ADRs) and design choices | 12 | **COMPLETE** |
| `docker-compose.yml` | Multi-container orchestration for PostgreSQL, backend, AI worker, and frontend | 97 | **CONFIG/ASSET** |
| `KNOWN_ISSUES.md` | Catalog of documented issues, workarounds, and resolutions | 8 | **COMPLETE** |
| `mock_interview.db` | Active SQLite database instance for local testing without Docker | 3749 | **CONFIG/ASSET** |
| `PROGRESS.md` | Development phase tracking and build progress milestones | 96 | **COMPLETE** |
| `pytest.ini` | Pytest configuration with test paths and pythonpath setup | 6 | **CONFIG/ASSET** |
| `REQUIREMENTS_TRACE.md` | Requirement-to-code traceability matrix | 48 | **COMPLETE** |

---

## 3. Codebase Metrics & Layer Totals

| Layer / Subsystem | Total Files | Total Lines of Code | Share of Codebase |
|:---|:---:|:---:|:---:|
| **Backend (Application & Models)** | 76 | 11,185 | 23.8% |
| **AI Multimodal Modules** | 14 | 2,140 | 4.6% |
| **Frontend (React & Components)** | 78 | 12,530 | 26.7% |
| **Tests & Benchmarks** | 26 | 5,424 | 11.6% |
| **Configuration & Orchestration** | 9 | 4,164 | 8.9% |
| **Storage & SQLite Snapshots** | 67 | 11,503 | 24.5% |
| **TOTAL** | **270** | **46,946** | **100.0%** |

---

## 4. Suspicious Items & Code Hygiene Analysis

During static analysis and AST inspection, the following findings were cataloged:

1. **Unused / Dead Code:**
   - Zero orphaned files detected in `frontend/src` or `backend/app`. All 30 pages are registered in `AppRoutes.jsx`, all 12 API modules in `api_router`, and all 7 AI plugins in `AIPluginRegistry`.
   - `activity_logs`, `backups`, and `question_sets` DB tables have active SQLAlchemy models and migrations, but currently hold 0 records in local development because SQLite backups write directly to `.sqlite` disk files and custom question sets are uploaded into the main `questions` table.

2. **TODO / FIXME Flags:**
   - **0 TODOs** and **0 FIXMEs** exist anywhere in `backend/app/`, `backend/tests/`, or `frontend/src/`. All scheduled development phase tasks have been implemented with concrete logic.

3. **Hard-Coded Secrets & API Keys:**
   - **Zero leaked credentials**: Git history and code files were checked for OpenAI (`sk-`), Google API (`AIza`), GitHub tokens, and private keys. All sensitive credentials are instantiated strictly via environment variables (`settings.GEMINI_API_KEY`, `settings.SECRET_KEY`) with fallback logic when absent.

4. **Mock Data in Production Code:**
   - In `frontend/src/pages/candidate/InterviewRoomPage.jsx`, `loadFallbackQuestions()` contains 4 fallback interview questions that load only if the backend API or network connection drops during interview room startup.
   - In `backend/app/ai/question_generator.py`, `FALLBACK_QUESTIONS` contains structured questions organized by job role and category to guarantee uninterrupted interview sessions when external LLMs exceed rate limits.
   - In `backend/app/services/email.py`, when SMTP environment variables are not configured, OTP codes and password reset links are printed to the server console rather than failing silently or crashing.

5. **Encoding Pitfall on Windows:**
   - In `backend/app/services/email.py`, emoji characters (`\U0001f4e9` / 📩) were found in console log outputs. When running locally on Windows systems without UTF-8 console output (`PYTHONUTF8=1`), this triggers a `UnicodeEncodeError` during candidate OTP email dispatch. This is documented in `KNOWN_ISSUES.md` and `07_VERIFICATION_RESULTS.md`.
