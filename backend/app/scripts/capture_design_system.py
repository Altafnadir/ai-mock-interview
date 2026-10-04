import os
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.abspath("docs/screenshots/design_system")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_URL = "http://localhost:5173"

def capture_design_system():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for theme in ["white", "black", "blue", "system"]:
            color_scheme = "dark" if theme in ["black", "blue", "system"] else "light"
            context = browser.new_context(
                viewport={"width": 1440, "height": 1100},
                color_scheme=color_scheme
            )
            context.add_init_script(f"""
                window.sessionStorage.setItem('mock_interview_splash_shown', 'true');
                window.localStorage.setItem('mock_interview_theme', '{theme}');
            """)
            page = context.new_page()

            page.goto(f"{BASE_URL}/design-system")
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"design_system_{theme}.png"), full_page=True)
            print(f"Saved design_system_{theme}.png")
            context.close()

        browser.close()
    print("Design system screenshots captured!")

if __name__ == "__main__":
    capture_design_system()
