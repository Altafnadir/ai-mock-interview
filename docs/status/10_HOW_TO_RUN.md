# 10. How to Run, Test & Operate the Platform

**Audit Date:** October 2026  
**Auditor Mode:** Clean-Clone Operational Runbook  
**Project:** AI-Based Mock Interview Preparation System (GIMS-BSSE-F202206)  

---

## 1. Quick Reference & Credentials

| Role / Service | Default Email / URL | Default Password / Port | Notes |
|:---|:---|:---|:---|
| **System Admin** | `admin@gims.edu.pk` | `AdminSecurePassword123!` | Access to `/admin` dashboard |
| **Team Candidate** | Configured via `seed_users.local.json` | Configured locally (uncommitted) | Pre-populated profile & sessions |
| **Frontend UI** | `http://localhost:5173` (dev) / `:80` (prod) | — | Vite / Nginx SPA |
| **Backend REST API**| `http://localhost:8000/api/v1` | — | FastAPI |
| **Interactive Docs**| `http://localhost:8000/docs` | — | Swagger UI |
| **PostgreSQL DB** | `localhost:5432` | User: `postgres`, Pass: `postgres` | Database: `ai_mock_interview` |

---

## 2. Option A: Running with Docker Compose (Recommended)

Requires Docker Desktop or Docker Engine + Compose installed on your host system.

```bash
# 1. Clone repository
git clone <repository_url>
cd ai-mock-interview

# 2. Configure environment
cp .env.example .env

# (Optional) Add your GEMINI_API_KEY to .env for generative LLM features.
# If left blank, the system automatically uses robust built-in heuristic fallbacks.

# 3. Build and launch all 4 containers in background
docker compose up --build -d

# 4. Confirm container health
docker compose ps
curl http://localhost:8000/health
```

Access the frontend at `http://localhost:5173` or `http://localhost:80`.

---

## 3. Option B: Running Locally without Docker (Zero-Config SQLite)

The platform includes full native support for SQLite (`mock_interview.db`), enabling instant local testing without Docker or PostgreSQL.

### Step 1: Backend Setup
```bash
# In project root:
# 1. Activate virtual environment (or create python 3.11 venv)
python -m venv .venv

# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8=1    # Important: ensures UTF-8 console output for email OTP prints

# On Linux / macOS:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Copy environment configuration
cp .env.example .env

# 4. Run database migrations to head revision
cd backend
python -m alembic upgrade head

# 5. Seed initial metadata, admin, questions, resources, and demo candidate
python -m app.scripts.seed

# 6. Start FastAPI server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 2: AI Processing Worker (Terminal 2)
In a separate terminal, start the asynchronous background processing queue worker:
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8=1

cd backend
python -m app.workers.run
```

### Step 3: Frontend Setup (Terminal 3)
```bash
cd frontend

# Install node dependencies
npm install

# Start Vite development server
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 4. How to Run Automated Test Suites

### Run Backend Pytest Suite
```bash
# From project root:
pytest -v

# Run specific domain test suites:
pytest backend/tests/test_auth.py -v
pytest backend/tests/test_interviews.py -v
pytest backend/tests/test_ai_pipeline.py -v
pytest backend/tests/test_reports.py -v
pytest backend/tests/test_admin.py -v
pytest backend/tests/test_resume_parser_10_samples.py -v
```

### Run Frontend Vitest & Build Checks
```bash
cd frontend

# Run component test suite:
npm run test

# Run code linter:
npm run lint

# Test production build:
npm run build
```

---

## 5. Database Reset & Backup Operations

### How to Reset the Database to Fresh Clean State

**Docker Environment:**
```bash
docker compose down -v
docker compose up --build -d
# Migrations and seeder run automatically upon container startup.
```

**Non-Docker SQLite Environment:**
```bash
# 1. Stop backend and worker processes
# 2. Remove SQLite file
rm mock_interview.db

# 3. Re-run migrations and master seed
cd backend
python -m alembic upgrade head
python -m app.scripts.seed
```

### How to Take and Restore Database Backups

- **Via Admin UI:**
  1. Login as `admin@gims.edu.pk` at `http://localhost:5173/admin/login`.
  2. Navigate to **Security & Backups** (`/admin/security`).
  3. Click **"Create Database Backup"**. An instant timestamped snapshot is archived to `storage/backups/`.
  4. To restore, select any snapshot from the backups table and click **"Restore"**.

- **Via REST API:**
  ```bash
  # Take backup:
  curl -X POST http://localhost:8000/api/v1/admin/backup \
       -H "Authorization: Bearer <ADMIN_ACCESS_TOKEN>"

  # Restore backup:
  curl -X POST http://localhost:8000/api/v1/admin/restore/<BACKUP_ID> \
       -H "Authorization: Bearer <ADMIN_ACCESS_TOKEN>"
  ```

---

## 6. API Keys & Fallback Engine Matrix

| Service / API Key | Purpose | Required? | Fallback Behavior when Missing |
|:---|:---|:---:|:---|
| `GEMINI_API_KEY` | Generative interview question generation, dynamic follow-ups, resume parsing, STAR evaluation | Optional | **Built-in Heuristic Fallback:** Uses curated 128-question bank, regex skill extractor, and rule-based STAR density evaluator. |
| `OPENAI_API_KEY` | Alternative LLM provider | Optional | Falls back to Gemini or built-in heuristic engine. |
| `YOUTUBE_API_KEY` | Dynamic YouTube video search for weak-area resources | Optional | **Pre-Seeded Resource Library:** 30 high-definition video tutorials mapped to all 8 canonical weakness tags are bundled in the database. |
| `SMTP_*` | Automated email dispatch for registration OTPs and PDF reports | Optional | **Console OTP Fallback:** Generates real 6-digit OTPs and prints them directly to terminal stdout for effortless local development. |
| `GOOGLE_CLIENT_ID`| Google Single Sign-On (OAuth2) | Optional | Password and Passwordless OTP logins remain 100% active. |
"""

out_file = Path(r"d:\ai-mock-interview\docs\status\10_HOW_TO_RUN.md")
with open(out_file, "w", encoding="utf-8") as f:
    f.write(md)

print(f"Written {out_file} ({len(md)} chars)")
