# Architectural & Engineering Decisions

| ID | Decision | Rationale |
|---|---|---|
| DEC-001 | SQLite used for local dev/testing with full PostgreSQL 15 support in Docker / production | Ensures zero-dependency instantaneous local test suites and offline execution while retaining full PG 15 compatibility in container deployments. |
| DEC-002 | PostgreSQL `processing_jobs` table with `FOR UPDATE SKIP LOCKED` for worker concurrency | Avoids Redis dependency overhead while providing fully transactional, crash-resilient multi-worker job scheduling as specified in Section 3. |
| DEC-003 | Hybrid AI processing with deterministic fallback heuristics when LLM/API keys absent | Guarantees 100% operational uptime, test pass rate, and zero runtime crashes if Gemini/OpenAI/LanguageTool/YouTube API keys are not supplied. |
| DEC-004 | Audio normalization via ffmpeg to 16kHz mono WAV and video to H.264 MP4 | Eliminates cross-browser codec incompatibilities (Safari MP4 vs Chrome WebM) before feeding into Whisper, Librosa, and MediaPipe. |
| DEC-005 | ReportLab for all 3 PDF deliverables (Full Report, AI Summary, Performance Poster) | Generates crisp, mathematically styled vector PDFs with custom color palettes, gauges, and tables without headless Chrome/WeasyPrint font engine overhead. |
| DEC-006 | Client-side IndexedDB buffer for audio/video chunks during mock interview | Prevents any data loss during transient network disconnects; chunks are stored locally and re-dispatched upon connection restoration. |
| DEC-007 | AI Plugin Registry in `app.ai.registry` | Permits dynamic registration and execution of specialized analysis modules without mutating core session pipeline logic. |
| DEC-008 | StorageService provider abstraction supporting Local Directory and S3/MinIO | Satisfies proposal cloud storage requirement while keeping zero-config local file storage as the default out-of-the-box mode. |
