import os
import json
import requests
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.abspath("docs/screenshots/themes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_URL = "http://localhost:5173"
API_URL = "http://127.0.0.1:8000/api/v1"

# Fetch candidate credentials dynamically from local seed file
seed_file = "backend/app/scripts/seed_users.local.json"
seed_data = json.load(open(seed_file))
candidate_pwd = seed_data[0]["password"] if isinstance(seed_data, list) else seed_data["users"][0]["password"]
candidate_email = "altafnadir33@gims.edu.pk"

cand_res = requests.post(f"{API_URL}/auth/login", json={
    "email": candidate_email,
    "password": candidate_pwd
})
cand_data = cand_res.json()
candidate_token = cand_data["access_token"]
candidate_user = cand_data["user"]

# Fetch sessions for this candidate
headers = {"Authorization": f"Bearer {candidate_token}"}
sess_res = requests.get(f"{API_URL}/interviews", headers=headers)
sessions = sess_res.json()
sample_session_id = "6a55d143-cbfb-4b8b-99d2-82617edf9051"
if isinstance(sessions, list) and len(sessions) > 0:
    sample_session_id = sessions[0].get("id", sample_session_id)

print(f"Candidate authenticated. Sample session ID: {sample_session_id}")

# Admin authentication
admin_res = requests.post(f"{API_URL}/auth/login", json={
    "email": "admin@gims.edu.pk",
    "password": "AdminSecurePassword123!"
})
admin_data = admin_res.json()
admin_token = admin_data["access_token"]
admin_user = admin_data["user"]
print("Admin authenticated.")

THEMES = ["white", "black", "blue", "system"]

def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for theme in THEMES:
            print(f"--- Capturing Theme: {theme} ---")
            color_scheme = "dark" if theme in ["black", "blue", "system"] else "light"

            # 1. Public Context (Unauthenticated / Public pages)
            pub_context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                color_scheme=color_scheme
            )
            pub_context.add_init_script(f"""
                window.sessionStorage.setItem('mock_interview_splash_shown', 'true');
                window.localStorage.setItem('mock_interview_theme', '{theme}');
            """)
            pub_page = pub_context.new_page()

            # Landing Page
            pub_page.goto(f"{BASE_URL}/")
            pub_page.wait_for_timeout(1000)
            pub_page.screenshot(path=os.path.join(OUTPUT_DIR, f"landing_{theme}.png"), full_page=False)
            print(f"Saved landing_{theme}.png")

            # Login Page
            pub_page.goto(f"{BASE_URL}/login")
            pub_page.wait_for_timeout(1000)
            pub_page.screenshot(path=os.path.join(OUTPUT_DIR, f"login_{theme}.png"), full_page=False)
            print(f"Saved login_{theme}.png")

            pub_context.close()

            # 2. Candidate Context (Authenticated Candidate)
            cand_context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                color_scheme=color_scheme
            )
            cand_user_json = json.dumps(candidate_user)
            cand_context.add_init_script(f"""
                window.sessionStorage.setItem('mock_interview_splash_shown', 'true');
                window.localStorage.setItem('mock_interview_theme', '{theme}');
                window.localStorage.setItem('user', JSON.stringify({cand_user_json}));
                window.localStorage.setItem('access_token', '{candidate_token}');
                window.localStorage.setItem('refresh_token', '{candidate_token}');
            """)
            cand_page = cand_context.new_page()

            # Candidate Interview Setup Page
            cand_page.goto(f"{BASE_URL}/interview/setup")
            cand_page.wait_for_timeout(1500)
            cand_page.screenshot(path=os.path.join(OUTPUT_DIR, f"setup_{theme}.png"), full_page=False)
            print(f"Saved setup_{theme}.png")

            # Candidate Dashboard
            cand_page.goto(f"{BASE_URL}/dashboard")
            cand_page.wait_for_timeout(1500)
            cand_page.screenshot(path=os.path.join(OUTPUT_DIR, f"dashboard_{theme}.png"), full_page=False)
            print(f"Saved dashboard_{theme}.png")

            # Candidate Report Page
            cand_page.goto(f"{BASE_URL}/reports/{sample_session_id}")
            cand_page.wait_for_timeout(1500)
            cand_page.screenshot(path=os.path.join(OUTPUT_DIR, f"report_{theme}.png"), full_page=False)
            print(f"Saved report_{theme}.png")

            cand_context.close()

            # 3. Admin Context (Authenticated Admin)
            admin_context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                color_scheme=color_scheme
            )
            admin_user_json = json.dumps(admin_user)
            admin_context.add_init_script(f"""
                window.sessionStorage.setItem('mock_interview_splash_shown', 'true');
                window.localStorage.setItem('mock_interview_theme', '{theme}');
                window.localStorage.setItem('user', JSON.stringify({admin_user_json}));
                window.localStorage.setItem('access_token', '{admin_token}');
                window.localStorage.setItem('refresh_token', '{admin_token}');
            """)
            admin_page = admin_context.new_page()

            # Admin Dashboard Page
            admin_page.goto(f"{BASE_URL}/admin")
            admin_page.wait_for_timeout(1500)
            admin_page.screenshot(path=os.path.join(OUTPUT_DIR, f"admin_dashboard_{theme}.png"), full_page=False)
            print(f"Saved admin_dashboard_{theme}.png")

            admin_context.close()

        # Capture Mobile Width (390 x 844) in White and Blue
        print("--- Capturing Mobile Width Views ---")
        for m_theme in ["white", "blue"]:
            m_color = "dark" if m_theme == "blue" else "light"
            m_context = browser.new_context(
                viewport={"width": 390, "height": 844},
                is_mobile=True,
                has_touch=True,
                color_scheme=m_color
            )
            cand_user_json = json.dumps(candidate_user)
            m_context.add_init_script(f"""
                window.sessionStorage.setItem('mock_interview_splash_shown', 'true');
                window.localStorage.setItem('mock_interview_theme', '{m_theme}');
                window.localStorage.setItem('user', JSON.stringify({cand_user_json}));
                window.localStorage.setItem('access_token', '{candidate_token}');
                window.localStorage.setItem('refresh_token', '{candidate_token}');
            """)
            m_page = m_context.new_page()

            # Mobile Landing
            m_page.goto(f"{BASE_URL}/")
            m_page.wait_for_timeout(1000)
            m_page.screenshot(path=os.path.join(OUTPUT_DIR, f"landing_mobile_{m_theme}.png"), full_page=False)
            print(f"Saved landing_mobile_{m_theme}.png")

            # Mobile Dashboard
            m_page.goto(f"{BASE_URL}/dashboard")
            m_page.wait_for_timeout(1500)
            m_page.screenshot(path=os.path.join(OUTPUT_DIR, f"dashboard_mobile_{m_theme}.png"), full_page=False)
            print(f"Saved dashboard_mobile_{m_theme}.png")

            m_context.close()

        browser.close()
    print("All theme screenshots successfully captured!")

if __name__ == "__main__":
    capture_all()
