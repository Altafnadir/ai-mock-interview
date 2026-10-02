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
| DEC-009 | Brand Logo Selection: OPTION 2 chosen as official "Mock Interview AI" identity | Selected after comparative visual and small-size fidelity analysis. Option 2 depicts candidate head profile with an AI vision target/eye and vocal soundwaves, perfectly unifying Computer Vision (MediaPipe) and Audio Speech (Whisper/Librosa) pillars. |

---

### Logo Candidate Comparison Matrix (Task 0)

| Criteria | Option 1 (Speech Bubble + Neural Graph + Mic) | Option 2 (Candidate Profile + AI Vision Eye + Soundwaves) | Option 3 (Speech Bubble + Growth Chart) |
|---|---|---|---|
| **Visual Metaphor** | Conversational AI / Audio | Multimodal Vision + Speech + Candidate Intelligence | Business Analytics / Metrics Growth |
| **Readability at 16x16 / 32x32** | Fair (thin neural vertices lose definition) | **Excellent** (bold circular aperture & solid head silhouette remain sharp) | Good (simple bar chart shapes) |
| **Edge Definition & Cleanliness** | Complex multi-node vector | **Crisp, modern, high-contrast geometry** | Solid blocks |
| **Dark & Light Background Contrast** | Good on light, fair on dark | **Outstanding** (high-contrast royal blue, indigo, and bright electric cyan) | High contrast, but generic |
| **Fit for AI Mock Interview** | Moderate (looks like generic chatbot) | **Highest** (directly represents candidate face, camera gaze, and speech delivery) | Low (resembles financial or BI dashboard) |
| **Verdict** | Alternate | **SELECTED (Official Brand Identity)** | Rejected |

