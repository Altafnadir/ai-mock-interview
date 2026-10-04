import os
import json
import time
import requests
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.abspath("docs/screenshots/ui")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_URL = "http://localhost:5173"
API_URL = "http://127.0.0.1:8000/api/v1"

candidate_email = "altafnadir33@gims.edu.pk"
candidate_pwd = os.environ.get("DEMO_PASSWORD", "")

cand_res = requests.post(f"{API_URL}/auth/login", json={
    "email": candidate_email,
    "password": candidate_pwd
})
cand_data = cand_res.json()
candidate_token = cand_data.get("access_token", "")
candidate_user = cand_data.get("user", {})

def capture_phase1():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. Screen 1: Landing Page (Public)
        pub_ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = pub_ctx.new_page()
        page.goto(f"{BASE_URL}/?nosplash=1", wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "01_landing.png"))
        print("Captured 01_landing.png")
        pub_ctx.close()

        # 2. Screen 2: Login Page (Public)
        login_ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = login_ctx.new_page()
        page.goto(f"{BASE_URL}/login?nosplash=1", wait_until="networkidle")
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "02_login.png"))
        print("Captured 02_login.png")
        login_ctx.close()

        # 3. Screen 3: Dashboard (Authenticated Candidate)
        cand_ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = cand_ctx.new_page()
        page.goto(f"{BASE_URL}/login?nosplash=1", wait_until="networkidle")
        page.evaluate(f"""() => {{
            localStorage.setItem('auth-storage', JSON.stringify({{
                state: {{
                    token: '{candidate_token}',
                    user: {json.dumps(candidate_user)},
                    isAuthenticated: true
                }},
                version: 0
            }}));
            sessionStorage.setItem('mock_interview_splash_shown', 'true');
            document.documentElement.setAttribute('data-theme', 'white');
        }}""")
        page.goto(f"{BASE_URL}/dashboard?nosplash=1", wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "03_dashboard.png"))
        print("Captured 03_dashboard.png")

        # 4. Screen 4: Resume Analysis (Authenticated Candidate)
        page.goto(f"{BASE_URL}/resume?nosplash=1", wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "04_resume_analysis.png"))
        print("Captured 04_resume_analysis.png")

        cand_ctx.close()
        browser.close()

if __name__ == "__main__":
    capture_phase1()
