<div align="center">
  <img src="frontend/public/brand/logo-icon.png" alt="Mock Interview AI" width="160" />
  <h1>Mock Interview AI</h1>
  <p><strong>Practice. Analyze. Get Hired.</strong></p>
  <p>An enterprise-grade, multi-modal artificial intelligence platform for technical, behavioral, and HR mock interviews with real-time audio/visual tracking, instant rubric scoring, and comprehensive PDF analytics.</p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.11" />
    <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black" alt="React 18" />
    <img src="https://img.shields.io/badge/Vite-5-646CFF?style=flat&logo=vite&logoColor=white" alt="Vite" />
    <img src="https://img.shields.io/badge/PostgreSQL-18-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/TailwindCSS-3.4-06B6D4?style=flat&logo=tailwindcss&logoColor=white" alt="TailwindCSS" />
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat" alt="MIT License" />
  </p>
</div>

---

## 🎯 System Highlights

- **Multi-Modal AI Pipeline**: Real-time evaluation across **7 distinct dimensions** — Technical depth, Speech clarity, Eye contact engagement, Posture & body language, Voice pace/WPM, Emotional sentiment, and Grammar syntax.
- **Adaptive Question Engine**: Dynamic question generation tailored to the candidate's resume, selected seniority, and domain (Full Stack, Backend, Frontend, DevOps, ML/AI, QA, Mobile, Cloud, Cybersecurity).
- **Comprehensive PDF Reports**: Generates multi-page official ReportLab evaluation dossiers, 1-page executive summaries, and dark-mode performance posters.
- **Enterprise Security & Auth**: JWT authentication, argon2/bcrypt hashing, OTP email verification, per-IP rate limiting, and role-based access control (Admin / Candidate).
- **Modern Responsive UI**: Built with React 18, Tailwind CSS, Lucide icons, glassmorphism aesthetics, and system-wide 4-theme switching (System, White, Black, Blue).

---

## 🌗 Appearance & Theme Options

The platform includes a 4-choice theme engine accessible via the accessible `ThemeSwitcher` dropdown on all pages (Navbar, Auth screens, Candidate layout, and Admin console):

- **System (Default)**: Automatically tracks your device's `prefers-color-scheme` via `matchMedia`. Resolves dynamically to White in light mode and Black in dark mode.
- **White**: A crisp, distraction-free light theme with `#FFFFFF` / `#F8FAFC` backgrounds, `#E2E8F0` borders, and `#0F172A` high-contrast typography.
- **Black**: An ultra-deep OLED dark theme with `#000000` / `#0A0A0A` / `#121212` backgrounds, `#27272A` borders, and `#F8FAFC` text.
- **Blue**: A dark navy executive theme featuring `#0B1B3F` / `#12285C` / `#172554` backgrounds, `#1E3A8A` navy borders, `#E8F0FF` crisp text, and `#3B82F6` vibrant blue accents.

Stored choices persist in `localStorage` under `mock_interview_theme` and an inline pre-render script in `index.html` prevents Flash of Unstyled Content (FOUC). All charts (Recharts), brand logos, and active interview teleprompter overlays adapt dynamically.

## 🎨 Visual Identity & Brand System

- **Brand Name**: Mock Interview AI
- **Tagline**: Practice. Analyze. Get Hired.
- **Primary Color**: `#1858E8` (Royal Blue)
- **Primary Dark**: `#3B32C8` (Cognitive Indigo)
- **Accent Color**: `#0BB0E8` (Electric Cyan)
- Detailed brand assets and usage guidelines can be found in [docs/BRANDING.md](docs/BRANDING.md).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- PostgreSQL 14+ (or bundled local cluster)

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/Altafnadir/ai-mock-interview.git
cd ai-mock-interview

# Setup Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment variables
cp .env.example .env

# Run database migrations and seed default data
python -m app.scripts.seed
python -m app.scripts.seed_users

# Start the FastAPI backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Team Candidate Accounts Seeding
Candidate accounts are loaded via an uncommitted local JSON file for security:
1. Copy `backend/app/scripts/seed_users.example.json` to `backend/app/scripts/seed_users.local.json`.
2. Configure account credentials in `seed_users.local.json`.
3. Run `python -m app.scripts.seed_users` manually or start the dev server (runs automatically on startup). Password handling is strictly isolated and never logged or committed.


### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to access the application.

---

## 🧪 Testing Suite

### Backend Test Suite
```bash
pytest backend/tests -v
```

### Frontend Vitest Suite
```bash
cd frontend
npm run test:run
```

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
