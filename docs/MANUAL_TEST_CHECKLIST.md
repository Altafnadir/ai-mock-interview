# Real Device & Browser Manual Testing Checklist

> **AI-Based Mock Interview Preparation System**  
> Group Final Year Project | PMAS-Arid Agriculture University Rawalpindi / GIMS  
> Authors: Iltaf Ali (21-ARID-4560), M. Hussnain (21-ARID-4573) | Supervisor: Ma'am Rabia Butt

---

## 1. Browser & Device Testing Matrix

| Device / Platform | Browser Engine | Audio / Video MediaRecorder | Web Speech TTS | Full Flow Status | Tester / Notes |
|---|---|---|---|---|---|
| **Windows 11 / 10** | Google Chrome 120+ | VP8 / VP9 / Opus (`video/webm`) | Supported | **VERIFIED** | Automated (Playwright) & Manual verified |
| **Windows 11 / 10** | Microsoft Edge 120+ | VP8 / VP9 / Opus (`video/webm`) | Supported | **VERIFIED** | Chromium base, hardware acceleration ok |
| **Windows / Linux** | Mozilla Firefox 120+ | VP8 / Opus (`video/webm`) | Supported | **IMPLEMENTED-UNVERIFIED** | Candidate to test with manual webcam |
| **macOS Desktop** | Apple Safari 17+ | H.264 / AAC (`video/mp4`) | Supported | **NOT TESTED** | Requires native macOS hardware |
| **Mobile (Android)**| Chrome Mobile | H.264 / VP8 | Supported | **IMPLEMENTED-UNVERIFIED** | Candidate to test with phone camera/mic |
| **Mobile (iOS)** | Safari Mobile / iOS WebKit | H.264 / AAC (`video/mp4`) | Partial | **NOT TESTED** | Apple WebKit restrictions require direct iPhone test |

---

## 2. Pre-Flight Hardware & Environment Check

Before initiating a mock interview test:
1. **Server Running**:
   - Backend API: `http://localhost:8000` (FastAPI)
   - Frontend SPA: `http://localhost:5173` (Vite / React)
   - PostgreSQL 18 or SQLite active
2. **Hardware Permissions**:
   - Camera and Microphone permissions granted in browser prompt (`navigator.mediaDevices.getUserMedia`).
   - Good ambient lighting with camera at eye level (for MediaPipe face landmark detection).
   - Quiet environment for clean audio input (for Whisper STT and Librosa acoustic feature extraction).

---

## 3. Step-by-Step Candidate Journey Test Steps

### Step 1: Candidate Account Registration & OTP Verification
- [ ] Navigate to `http://localhost:5173/register`.
- [ ] Fill in Full Name, Email, Password, Target Role, and Experience Level.
- [ ] Submit registration form. Confirm redirect to OTP verification screen.
- [ ] Check console / email log for 6-digit OTP code.
- [ ] Enter OTP code and verify. Confirm successful login and JWT session storage in `localStorage`.

### Step 2: Profile & Resume Upload
- [ ] Navigate to Profile (`/profile`) and Resume Upload (`/resume`).
- [ ] Drag-and-drop a sample PDF/DOCX resume (e.g. `backend/tests/fixtures/sample_resumes/sample_1_fullstack.pdf`).
- [ ] Click "Analyze Resume".
- [ ] Verify skills extraction, experience timeline, and tailored role recommendations.

### Step 3: Interview Setup & Question Configuration
- [ ] Navigate to Interview Setup (`/interview/setup`).
- [ ] Select Target Job Role (e.g. Full Stack Engineer, Data Scientist, DevOps).
- [ ] Choose Interview Type: Comprehensive (Technical + Behavioral).
- [ ] Choose Question Source: AI-Generated (Gemini) or Pre-vetted Question Bank.
- [ ] Click "Start Interview" to create session.

### Step 4: Live Interview Room Experience
- [ ] Confirm camera preview activates immediately without delay.
- [ ] Check facial tracking indicator banner ("MediaPipe Vision: Active Tracking").
- [ ] Check Question Teleprompter: verify question 1 is clearly rendered with source badge.
- [ ] Check AI Speech (TTS): question is read aloud automatically if voice enabled.
- [ ] Test HUD Controls:
  - [ ] "Repeat Audio": replays question audio utterance.
  - [ ] "Skip Question": advances to next question without error.
  - [ ] "Toggle Fullscreen": expands room to borderless fullscreen.
  - [ ] "End Now": confirms session exit and queues analysis.
- [ ] Answer question with speech for 30–60 seconds.
- [ ] Click "Next Question" — verify MediaRecorder chunk is captured and uploaded.

### Step 5: Network Drop & Offline Resiliency
- [ ] Disconnect Wi-Fi or set browser devtools to "Offline".
- [ ] Verify amber alert banner: "Network connection lost. All video chunks are safely buffered locally in IndexedDB...".
- [ ] Answer next question and click advance: verify chunk is saved to IndexedDB (`pending_answers` store).
- [ ] Re-enable network: verify green toast notification "Internet connection restored. Synchronized buffered answers".
- [ ] Simulate total failure: if session cannot be loaded, verify clear "Connection Lost" screen with "Retry Connection" button appears (no hardcoded question fallbacks).

### Step 6: Processing Screen & Multi-Worker Queue
- [ ] After ending session, observe redirect to `/interview/:id/processing`.
- [ ] Verify circular progress meter and real-time status indicators (Audio extraction -> Whisper transcription -> Emotion analysis -> Multimodal scoring).
- [ ] Verify automatic redirection to Report page once processing reaches 100%.

### Step 7: Comprehensive 5-Domain Evaluation Report
- [ ] Inspect Overall Score (0–100) and Readiness Level badge (Ready / Needs Practice).
- [ ] Inspect 5-Domain Breakdown:
  1. Technical Accuracy (STAR method & keyword alignment)
  2. Communication & Articulation (Speaking pace WPM, filler words, grammar)
  3. Emotional & Facial Composure (Smile ratio, calm confidence, nervous expressions)
  4. Behavioral & Soft Skills (Leadership, teamwork, conflict resolution)
  5. Eye Contact & Attentiveness (Gaze fixation percentage)
- [ ] Inspect Radar Chart / Visualizations (Recharts multi-axis competency graph).
- [ ] Inspect Transcript Review with timestamps and per-turn feedback.
- [ ] Inspect AI-curated Strengths, Weaknesses, and Actionable Recommendations.

### Step 8: PDF Report Generation & Export
- [ ] Click "Export Candidate Report (PDF)": verify download of comprehensive candidate PDF.
- [ ] Click "Export Technical Evaluation (PDF)": verify deep technical rubric breakdown.
- [ ] Click "Export Executive Summary (PDF)": verify concise 1-page leadership summary.
- [ ] Open downloaded PDFs: verify high-resolution formatting, clean typography, and zero layout overlap.

### Step 9: Report Sharing & Dashboard Integration
- [ ] Click "Share Report": verify shareable link copied to clipboard.
- [ ] Open share link in incognito browser tab: verify read-only candidate report renders cleanly.
- [ ] Return to Candidate Dashboard (`/dashboard`):
  - [ ] Verify latest interview appears in History table.
  - [ ] Verify performance progress trend line updates.
  - [ ] Verify Personalized Practice Drills (`/practice`) recommend exercises based on weak areas identified in this report.

---

## 4. Evaluator Sign-Off Template

- **Tester Name**: __________________________
- **Test Date**: __________________________
- **Operating System / Device**: __________________________
- **Browser & Version**: __________________________
- **Webcam / Audio Hardware**: __________________________
- **Overall Result**: [ ] PASS   [ ] MINOR ISSUES   [ ] FAIL
- **Comments / Observations**:
