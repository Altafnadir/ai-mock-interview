# 09. Remaining Work, Bug Catalog & Technical Debt

**Audit Date:** October 2026  
**Auditor Mode:** Risk & Debt Evaluation based on Direct Execution  
**Project:** AI-Based Mock Interview Preparation System (GIMS-BSSE-F202206)  

---

## 1. Prioritized Action Backlog

The following backlog categorizes all identified bugs, technical gaps, and polish items into standardized priority tiers:
- **P0 (Critical / Blocker):** System cannot run, or main user journey crashes.
- **P1 (High / Required):** Proposal feature partial or missing integration.
- **P2 (Medium / Quality & Security):** Performance, linting, or container hardening.
- **P3 (Low / Nice-to-Have):** Non-blocking enhancements and optimizations.

| Priority | Item / Finding | Affected Files / Routes | Effort | Suggested Resolution |
|:---:|:---|:---|:---:|:---|
| **P0** | **Windows Console Encoding Crash:** `send_otp_email` outputs unicode emoji (`\U0001f4e9` / 📩) causing `UnicodeEncodeError` under Windows default `cp1252` encoding. | `backend/app/services/email.py` (lines 14, 25) | **S** (10 mins) | Replace raw unicode emoji in `print()` statements with standard ASCII log messages `[EMAIL OTP NOTIFICATION]`, or configure standard Python logging handler. |
| **P1** | **Dynamic Drill Integration:** `PracticePage.jsx` currently displays static drill cards linking to setup rather than consuming dynamic backend `/api/v1/practice/drills`. | `frontend/src/pages/candidate/PracticePage.jsx`, `/api/v1/practice/drills` | **S** (30 mins) | Connect `PracticePage.jsx` to `practiceApi.getDrills()` to render practice items dynamically from database. |
| **P1** | **Environment Variables Parity:** Eight variables used in backend code/compose (`PROJECT_ID`, `MAINTENANCE_MODE`, `STORAGE_TYPE`, `WORKER_CONCURRENCY`, `S3_*`) are missing from `.env.example`. | `.env.example`, `backend/app/core/config.py` | **S** (15 mins) | Update `.env.example` with documented defaults for all 8 parameters. |
| **P2** | **Frontend Linter Warnings:** `oxlint` identified 167 warnings (unused catch `err` parameters, missing dependencies in `useEffect`). | `frontend/src/pages/candidate/InterviewRoomPage.jsx`, other pages | **M** (2 hours) | Clean up unused exception variables (`catch (_err)`) and memoize callback hooks (`useCallback`) in `InterviewRoomPage.jsx`. |
| **P2** | **Vite Bundle Code-Splitting:** Production build emits a single large JavaScript vendor bundle (~940 kB minified, 268 kB gzipped). | `frontend/vite.config.js` | **S** (30 mins) | Configure `manualChunks` in `vite.config.js` to split `vendor-react` (`react`, `react-dom`, `react-router-dom`) and `vendor-charts` (`recharts`). |
| **P2** | **LanguageTool Self-Hosted Fallback:** The default LanguageTool configuration points to public cloud endpoint `https://api.languagetoolplus.com/v2`, which enforces a 20 req/min rate limit. | `docker-compose.yml`, `backend/app/core/config.py` | **M** (1 hour) | Add an optional `languagetool` Docker service container to `docker-compose.yml` for offline self-hosted processing. |
| **P3** | **Automated Backup Lifecycle Rotation:** Daily SQLite database backups accumulate in `storage/backups/` without an automated 30-day retention cleanup. | `backend/app/core/scheduler.py` | **S** (30 mins) | Add a scheduled maintenance task in `scheduler.py` to delete backup snapshots older than 30 days. |
| **P3** | **WebSocket Room Audio Streaming:** The interview room records via chunked MediaRecorder slices; real-time low-latency audio feedback could be enhanced via WebSockets. | `frontend/src/pages/candidate/InterviewRoomPage.jsx`, `backend/app/main.py` | **L** (1-2 days) | Add optional bidirectional WebSocket endpoint for streaming speech transcription. |

---

## 2. Technical Risk & Bottleneck Analysis

### 1. Memory Overhead of Neural Models
- **Observation:** `deepface` and `faster-whisper` download and instantiate neural network weights (~500 MB).
- **Risk:** Running on memory-constrained virtual machines (< 2 GB RAM) can trigger Linux Out-Of-Memory (OOM) killer terminations.
- **Mitigation in Place:** Lazy singleton initialization; modules only load weights when an active video/audio stream is processed. Rule-based heuristic fallback triggers automatically if model loading fails.

### 2. Host Docker CLI Absence
- **Observation:** On the local Windows auditor machine, the `docker` command is not recognized on PATH.
- **Risk:** Developers without Docker Desktop installed cannot spin up PostgreSQL or the full 4-container stack via `docker compose up`.
- **Mitigation in Place:** Zero-config SQLite mode (`mock_interview.db`) is pre-seeded and fully supported out-of-the-box, allowing non-Docker local runs via `python -m uvicorn app.main:app` and `npm run dev`.

### 3. Starlette TestClient Deprecation Notice
- **Observation:** Pytest emitted 1 deprecation warning: `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead.`
- **Risk:** Future minor versions of Starlette may alter the internal `TestClient` constructor.
- **Mitigation:** Pin `starlette` or update test client import conventions during standard maintenance cycles.

---

## 3. Review of `KNOWN_ISSUES.md`

| Issue ID | Component | Description from Known Issues | Current Status | Audit Verification Notes |
|:---:|:---|:---|:---:|:---|
| **ISS-001** | `MediaRecorder` Safari | Safari on macOS/iOS sometimes fails to support `audio/webm;codecs=opus` or `video/webm`. | **Mitigated** | Verified `getSupportedMimeType()` probe in `InterviewRoomPage.jsx`. Transcoding to H.264 MP4 handled by `media_normalizer.py`. |
| **ISS-002** | DeepFace / MediaPipe Heavy Models | First inference neural loading introduces latency on CPU-only machines. | **Mitigated** | Lazy singletons verified; lightweight frame sampling active. Fallback demeanor rules execute in < 0.001s. |
| **ISS-003** | External LLM Rate Limits & Missing Keys | Absence of `GEMINI_API_KEY` causes network exceptions. | **Resolved** | Deterministic keyword and STAR heuristics active across `resume_parser.py`, `question_generator.py`, and `content_evaluator.py`. |
| **ISS-004** | Pytest Module Resolution | Running pytest from root directory caused `ModuleNotFoundError: No module named 'app'`. | **Resolved** | Verified `pytest.ini` with `pythonpath = .` and `testpaths = backend/tests`. All 56 tests execute cleanly from any directory. |
"""

out_file = Path(r"d:\ai-mock-interview\docs\status\09_REMAINING_WORK.md")
with open(out_file, "w", encoding="utf-8") as f:
    f.write(md)

print(f"Written {out_file} ({len(md)} chars)")
