# Database Engine Parity & Incompatibilities Guide: SQLite vs. PostgreSQL

**Project:** AI-Based Mock Interview Preparation System (GIMS-BSSE-F202206)  
**Engines Tested:** SQLite 3 (Development/Local) & PostgreSQL 18.6 (Production/Docker Official)  
**Status:** **VERIFIED** (100% test parity achieved: 57/57 Pytest tests passing on both engines)

---

## 1. Engine Architecture & Protocol

| Feature | SQLite (Local Dev Fallback) | PostgreSQL 18 (Official Proposal Target) |
|---|---|---|
| **Storage Architecture** | Single disk file (`mock_interview.db`) | Client-Server relational cluster (`ai_mock_interview`) |
| **Driver / Client** | Built-in Python `sqlite3` driver | `psycopg` (psycopg 3) and `psycopg2-binary` |
| **Connection URL** | `sqlite:///./mock_interview.db` | `postgresql://postgres:postgres@localhost:5432/ai_mock_interview` |
| **Connection Pooling** | `NullPool` (file-based locking) | `QueuePool` (pool_size=10, max_overflow=20, pool_pre_ping=True) |
| **Thread Model** | `check_same_thread=False` required | Multi-threaded client pool natively safe |

---

## 2. Incompatibilities Identified & Fixed

### A. Foreign Key Constraint Enforcement
- **SQLite Behavior:** SQLite disables foreign keys by default unless `PRAGMA foreign_keys = ON;` is explicitly invoked per connection. Dummy/non-existent IDs inserted into child tables would succeed silently.
- **PostgreSQL Behavior:** Strictly enforces relational integrity at transaction time. When testing recommendations with `session_id="dummy-session-123"`, PostgreSQL immediately aborted with `psycopg.errors.ForeignKeyViolation: recommendations_session_id_fkey`.
- **Fix Implemented:** Updated `backend/tests/test_dashboard_resources.py` and factory fixtures to ensure foreign keys always link to real, seeded parent entities (`InterviewSession`).

### B. Schema Migrations (Alembic DDL)
- **SQLite Behavior:** Does not support `ALTER TABLE ADD CONSTRAINT` or arbitrary column modifications; requires `render_as_batch=True` to create temporary replacement tables.
- **PostgreSQL Behavior:** Supports fully transactional DDL (`PostgresqlImpl`).
- **Fix Implemented:** Created Alembic migration `47602d1e9233_add_question_sets_and_missing_schema.py` adding `questions.question_set_id` with explicit constraint `fk_questions_question_set_id`, `reports.candidate_snapshot`, and `reports.summary_pdf_path` with safe defaults (`server_default='{}'`).

### C. JSON vs. Binary JSONB
- **SQLite Behavior:** Emulates JSON storage using string `TEXT` columns and SQLite JSON1 extensions.
- **PostgreSQL Behavior:** Implements binary `JSONB` with indexing, key extraction, and GIN index capability.
- **Verification:** Verified in `test_pg_concurrency.py` that nested structures (e.g. `report.weaknesses` lists of objects, `report.candidate_snapshot` dicts) serialize, deserialize, and query cleanly without type mismatches.

### D. Concurrency & Queue Locking (`SELECT ... FOR UPDATE SKIP LOCKED`)
- **SQLite Behavior:** Acquires file-level locks. Simultaneous worker writes trigger `sqlite3.OperationalError: database is locked`. `SELECT ... FOR UPDATE` syntax is unsupported and falls back to serial queries.
- **PostgreSQL Behavior:** Row-level locking with `SELECT ... FOR UPDATE SKIP LOCKED`.
- **Verification:** Ran two concurrent worker threads simultaneously claiming 10 queued jobs from `processing_jobs`.
  - Worker 1 claimed 5 jobs.
  - Worker 2 claimed 5 jobs.
  - **Duplicate claims: 0** (proven race-condition free).

---

## 3. How to Switch Engines Cleanly

Set `DATABASE_URL` in `.env`:

```env
# Mode 1: SQLite (Instant out-of-the-box local development, no Docker required)
DATABASE_URL=sqlite:///./mock_interview.db

# Mode 2: PostgreSQL (Official proposal target, production Docker Compose)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_mock_interview
```

The application's `app.db.session` dynamically handles dialect connection arguments, pooling parameters, and driver resolution automatically.
