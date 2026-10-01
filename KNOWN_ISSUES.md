# Known Issues & Workarounds

| ID | Component | Description | Workaround / Mitigation | Status |
|---|---|---|---|---|
| ISS-001 | MediaRecorder (Safari) | Safari on macOS/iOS sometimes fails to support `audio/webm;codecs=opus` or `video/webm`. | `mimeType` probe utility inspects `MediaRecorder.isTypeSupported` and falls back gracefully to `video/mp4` or empty string (browser default). Server-side ffmpeg normalizes all incoming streams to 16kHz mono WAV + H.264 MP4. | Mitigated |
| ISS-002 | DeepFace / MediaPipe Heavy Models on CPU | First inference loading deep neural networks can introduce high latency on constrained CPU instances. | Lazy-loaded singleton model instances; lightweight frame sampling (1 fps for emotion, 2-3 fps for vision); fallback computer vision heuristics when models are unavailable or initializing. | Mitigated |
| ISS-003 | External LLM Rate Limits & Missing Keys | Absence of `GEMINI_API_KEY` or `OPENAI_API_KEY` causes network exceptions. | Robust fallback engines for question generation, resume parsing, and content evaluation that produce structured data via deterministic heuristics and keyword analysis. | Mitigated |
| ISS-004 | Pytest module resolution from root | Running `pytest backend/tests` directly without PYTHONPATH can cause `ModuleNotFoundError: No module named 'app'`. | Added `backend/pytest.ini` with `pythonpath = .` and root configuration so `pytest` works seamlessly from any working directory. | Resolved |
