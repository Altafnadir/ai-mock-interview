# Known Issues & Workarounds

| ID | Component | Description | Workaround / Mitigation | Status |
|---|---|---|---|---|
| ISS-001 | MediaRecorder (Safari) | Safari on macOS/iOS sometimes fails to support `audio/webm;codecs=opus` or `video/webm`. | `mimeType` probe utility inspects `MediaRecorder.isTypeSupported` and falls back gracefully to `video/mp4` or empty string (browser default). Server-side ffmpeg normalizes all incoming streams to 16kHz mono WAV + H.264 MP4. | Mitigated |
| ISS-002 | DeepFace / MediaPipe Heavy Models on CPU | First inference loading deep neural networks can introduce high latency on constrained CPU instances. | Lazy-loaded singleton model instances; lightweight frame sampling (1 fps for emotion, 2-3 fps for vision); fallback computer vision heuristics when models are unavailable or initializing. | Mitigated |
| ISS-003 | External LLM Rate Limits & Missing Keys | Absence of `GEMINI_API_KEY` or `OPENAI_API_KEY` causes network exceptions. | Robust fallback engines for question generation, resume parsing, and content evaluation that produce structured data via deterministic heuristics and keyword analysis. | Mitigated |
| ISS-004 | Pytest module resolution from root | Running `pytest backend/tests` directly without PYTHONPATH can cause `ModuleNotFoundError: No module named 'app'`. | Added `backend/pytest.ini` with `pythonpath = .` and root configuration so `pytest` works seamlessly from any working directory. | Resolved |

---

## External Integrations Requiring User Environment Keys

The following third-party services operate in resilient mock/fallback mode by default. To test them against real live external services, configure the corresponding environment variables in `.env`:

### 1. SMTP Email Service (Live Password Reset & Report Delivery)
Set these variables in `.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
EMAILS_FROM_EMAIL=your_email@gmail.com
EMAILS_FROM_NAME="GIMS AI Mock Interview"
SMTP_TLS=True
SMTP_SSL=False
```
*Note: For Gmail, generate an App Password under Google Account -> Security -> 2-Step Verification -> App passwords.*

### 2. Google OAuth 2.0 (Live Single Sign-On)
Set in `.env`:
```env
GOOGLE_CLIENT_ID=your_project_id.apps.googleusercontent.com
```
*Configure Authorized JavaScript origins to `http://localhost:5173` and redirect URI to `http://localhost:5173/auth/google/callback` in the Google Cloud Console.*

### 3. S3 / MinIO Cloud Storage (Live Object Storage)
Set in `.env`:
```env
STORAGE_TYPE=s3
S3_ENDPOINT_URL=https://s3.amazonaws.com # Or http://localhost:9000 for local MinIO
S3_ACCESS_KEY=your_aws_access_key_id
S3_SECRET_KEY=your_aws_secret_access_key
S3_BUCKET_NAME=your_interview_recordings_bucket
```

