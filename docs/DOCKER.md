# Docker Deployment & Orchestration Guide

**Status:** **IMPLEMENTED-UNVERIFIED**  
*(Dockerfiles, `docker-compose.yml`, `.dockerignore`, and Nginx reverse proxy configurations are fully written and statically validated. Docker Engine was not running on the local Windows audit host, so containerized runtime deployment is marked IMPLEMENTED-UNVERIFIED).*

---

## 1. Container Topology

The multi-tier system runs across 4 core containers and 1 optional microservice:

```
[ Candidate Browser ] 
        │
        ▼ (Port 80 / 5173)
┌─────────────────────────────────┐
│ mock_interview_frontend (Nginx) │
└─────────────────────────────────┘
        │ Proxy /api/ requests
        ▼ (Port 8000)
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│ mock_interview_backend (FastAPI)│──────▶│ mock_interview_db (PostgreSQL)  │
└─────────────────────────────────┘       └─────────────────────────────────┘
                                                           ▲
                                                           │ Claims queued jobs
                                          ┌─────────────────────────────────┐
                                          │ mock_interview_ai_worker        │
                                          └─────────────────────────────────┘
                                                           │ (Optional)
                                                           ▼
                                          ┌─────────────────────────────────┐
                                          │ mock_interview_languagetool     │
                                          └─────────────────────────────────┘
```

### Services Overview
1. **`db`** (`postgres:15-alpine`): Relational store on port 5432 with persistent volume `postgres_data` and native healthcheck (`pg_isready`).
2. **`backend`** (`python:3.11-slim`): FastAPI REST API on port 8000 with `ffmpeg`, `libsndfile1`, and `libgl1` installed; healthcheck at `http://localhost:8000/health`.
3. **`ai-worker`** (`python:3.11-slim`): Asynchronous background queue worker running `python -m app.workers.run`. Uses `SELECT ... FOR UPDATE SKIP LOCKED`.
4. **`frontend`** (`node:20-alpine` build + `nginx:alpine` runtime): Serves production React bundle on ports 80 and 5173 with API reverse proxy.
5. **`languagetool`** (optional profile `with-languagetool`): Self-hosted LanguageTool grammar correction engine on port 8010.

---

## 2. Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine + Docker Compose v2 (Linux)
- Minimum 4 GB RAM allocated to Docker

---

## 3. Step-by-Step Launch Commands

### A. Clone and Prepare Environment
```bash
git clone https://github.com/Altafnadir/ai-mock-interview.git
cd ai-mock-interview

# Copy environment template
cp .env.example .env
```

### B. Build and Start Core Containers
```bash
docker compose up -d --build
```

### C. Build and Start with Local LanguageTool Grammar Engine
```bash
docker compose --profile with-languagetool up -d --build
```

### D. Verify Container Health
```bash
docker compose ps
```
Expected output:
```
NAME                         IMAGE               COMMAND                  SERVICE             STATUS
mock_interview_db            postgres:15-alpine  "docker-entrypoint.s…"   db                  Up (healthy)
mock_interview_backend       backend-backend     "uvicorn app.main:ap…"   backend             Up (healthy)
mock_interview_ai_worker     backend-ai-worker   "python -m app.worke…"   ai-worker           Up
mock_interview_frontend      frontend-frontend   "/docker-entrypoint.…"   frontend            Up
```

### E. Run Initial Migrations and Database Seeds Inside Container
```bash
# Execute Alembic migrations
docker compose exec backend alembic upgrade head

# Seed roles, categories, 120+ questions, resources, and demo account
docker compose exec backend python -m app.scripts.seed
```

### F. View Logs
```bash
# Stream all logs
docker compose logs -f

# Stream only AI worker logs
docker compose logs -f ai-worker
```

### G. Stopping Containers
```bash
# Stop containers (preserves database and storage)
docker compose down

# Stop containers and purge volumes (complete reset)
docker compose down -v
```
