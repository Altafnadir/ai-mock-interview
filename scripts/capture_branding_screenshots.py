import os
import sys
import time
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright
import pypdfium2 as pdfium

BASE_FRONTEND = "http://localhost:5173"
BASE_BACKEND = "http://localhost:8000"
OUTPUT_DIR = Path(r"d:\ai-mock-interview\docs\screenshots\branding")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_sample_report_and_share():
    cand_resp = requests.post(f"{BASE_BACKEND}/api/v1/auth/login", json={
        "email": "candidate@gims.edu.pk",
        "password": "CandidatePassword123!"
    })
    cand_token = cand_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {cand_token}"}
    
    meta = requests.get(f"{BASE_BACKEND}/api/v1/meta/all").json()
    create_resp = requests.post(f"{BASE_BACKEND}/api/v1/interviews", json={
        "job_role_id": meta["job_roles"][0]["id"],
        "category_id": meta["categories"][0]["id"],
        "difficulty_id": meta["difficulties"][0]["id"],
        "total_questions": 2,
        "mode": "video"
    }, headers=headers)
    session_id = create_resp.json()["id"]

    requests.post(f"{BASE_BACKEND}/api/v1/interviews/{session_id}/start", headers=headers)
    requests.post(f"{BASE_BACKEND}/api/v1/interviews/{session_id}/answer", json={
        "transcript": "I engineered scalable cloud microservices with FastAPI, Docker, and PostgreSQL.",
        "duration_seconds": 30.0
    }, headers=headers)
    requests.post(f"{BASE_BACKEND}/api/v1/interviews/{session_id}/end", headers=headers)

    report_resp = requests.get(f"{BASE_BACKEND}/api/v1/reports/{session_id}", headers=headers)
    share_resp = requests.post(f"{BASE_BACKEND}/api/v1/reports/{session_id}/share", headers=headers)
    share_token = share_resp.json().get("token")
    pdf_rel_path = report_resp.json().get("pdf_path")

    return share_token, pdf_rel_path

def main():
    print("Generating sample report and share token...")
    share_token, pdf_rel_path = create_sample_report_and_share()
    print(f"Share token: {share_token}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. Landing Page (Light Mode)
        print("1. Capturing landing.png...")
        ctx_landing = browser.new_context(viewport={"width": 1280, "height": 800})
        page = ctx_landing.new_page()
        page.goto(f"{BASE_FRONTEND}/", wait_until="networkidle")
        page.evaluate("document.documentElement.classList.remove('dark'); localStorage.setItem('theme', 'light');")
        time.sleep(1)
        page.screenshot(path=str(OUTPUT_DIR / "landing.png"))

        # 2. Dark Mode Landing
        print("2. Capturing dark_mode.png...")
        page.evaluate("document.documentElement.classList.add('dark'); localStorage.setItem('theme', 'dark');")
        time.sleep(1)
        page.screenshot(path=str(OUTPUT_DIR / "dark_mode.png"))
        ctx_landing.close()

        # 3. Mobile Width
        print("3. Capturing mobile_width.png...")
        ctx_mob = browser.new_context(viewport={"width": 375, "height": 812})
        page_mob = ctx_mob.new_page()
        page_mob.goto(f"{BASE_FRONTEND}/", wait_until="networkidle")
        time.sleep(1)
        page_mob.screenshot(path=str(OUTPUT_DIR / "mobile_width.png"))
        ctx_mob.close()

        # 4. Login Page
        print("4. Capturing login.png...")
        ctx_auth = browser.new_context(viewport={"width": 1280, "height": 800})
        page_auth = ctx_auth.new_page()
        page_auth.goto(f"{BASE_FRONTEND}/login", wait_until="networkidle")
        time.sleep(1)
        page_auth.screenshot(path=str(OUTPUT_DIR / "login.png"))

        # 5. Candidate Dashboard (via login submission)
        print("5. Capturing candidate_dashboard.png...")
        page_auth.fill("input[type='email']", "candidate@gims.edu.pk")
        page_auth.fill("input[type='password']", "CandidatePassword123!")
        page_auth.click("button[type='submit']")
        page_auth.wait_for_url("**/dashboard", timeout=10000)
        page_auth.wait_for_load_state("networkidle")
        time.sleep(2)
        page_auth.screenshot(path=str(OUTPUT_DIR / "candidate_dashboard.png"))
        ctx_auth.close()

        # 6. Admin Dashboard (via admin login submission)
        print("6. Capturing admin_dashboard.png...")
        ctx_admin = browser.new_context(viewport={"width": 1280, "height": 800})
        page_admin = ctx_admin.new_page()
        page_admin.goto(f"{BASE_FRONTEND}/admin/login", wait_until="networkidle")
        time.sleep(1)
        page_admin.fill("input[type='email']", "admin@gims.edu.pk")
        page_admin.fill("input[type='password']", "AdminPass123!")
        page_admin.click("button[type='submit']")
        page_admin.wait_for_url("**/admin", timeout=10000)
        page_admin.wait_for_load_state("networkidle")
        time.sleep(2)
        page_admin.screenshot(path=str(OUTPUT_DIR / "admin_dashboard.png"))
        ctx_admin.close()

        # 7. Shared Report Page
        print(f"7. Capturing report_page.png (/shared/{share_token})...")
        ctx_report = browser.new_context(viewport={"width": 1280, "height": 800})
        page_rep = ctx_report.new_page()
        page_rep.goto(f"{BASE_FRONTEND}/shared/{share_token}", wait_until="networkidle")
        time.sleep(2)
        page_rep.screenshot(path=str(OUTPUT_DIR / "report_page.png"))
        ctx_report.close()

        browser.close()

    # 8. Render One PDF Page
    print("8. Rendering one_pdf_page.png using pypdfium2...")
    pdf_full_path = Path(r"d:\ai-mock-interview") / pdf_rel_path
    if not pdf_full_path.exists():
        pdf_candidates = list(Path(r"d:\ai-mock-interview\storage\reports").glob("report_*.pdf"))
        if pdf_candidates:
            pdf_full_path = pdf_candidates[0]

    print(f"Using PDF: {pdf_full_path}")
    pdf = pdfium.PdfDocument(str(pdf_full_path))
    page0 = pdf[0]
    image = page0.render(scale=2.0).to_pil()
    image.save(str(OUTPUT_DIR / "one_pdf_page.png"))
    print("All branding screenshots captured successfully!")

if __name__ == "__main__":
    main()
