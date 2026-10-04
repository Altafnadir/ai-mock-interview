import os
from PIL import Image

def slice_panels():
    img_path = "design/ui-reference.jpeg"
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found")
        return

    img = Image.open(img_path)
    W, H = img.size
    print(f"Base image size: {W}x{H}")

    os.makedirs("design/panels", exist_ok=True)
    os.makedirs("design/components", exist_ok=True)

    # Panel definitions based on the 5-row layout in ui-reference.jpeg
    # Row 1 (y: 0 to ~180): 4 panels
    # 01_landing: x 0..290, y 0..180
    # 02_login: x 290..500, y 0..180
    # 03_dashboard: x 500..830, y 0..180
    # 04_resume_analysis: x 830..1024, y 0..180

    # Let's inspect the exact boundaries programmatically or define coordinates
    # Total image is 1024 x 682
    # Row heights: approx 5 rows
    # Row 1: y 0 to 184
    # Row 2: y 180 to 320
    # Row 3: y 320 to 445
    # Row 4: y 445 to 560
    # Row 5: y 560 to 682

    panels = [
        # (name, box: (left, upper, right, lower))
        # Row 1
        ("01_landing", (0, 0, 290, 184)),
        ("02_login", (290, 0, 500, 184)),
        ("03_dashboard", (500, 0, 830, 184)),
        ("04_resume_analysis", (830, 0, 1024, 184)),

        # Row 2
        ("05_ai_question_generator", (0, 180, 260, 320)),
        ("06_mock_interview_setup", (260, 180, 480, 320)),
        ("07_interview_screen", (480, 180, 765, 320)),
        ("08_voice_analysis", (765, 180, 1024, 320)),

        # Row 3
        ("09_body_posture_analysis", (0, 320, 195, 445)),
        ("10_eye_contact_analysis", (195, 320, 395, 445)),
        ("11_emotion_detection", (395, 320, 630, 445)),
        ("12_grammar_language_analysis", (630, 320, 1024, 445)),

        # Row 4
        ("13_interview_report_results", (0, 445, 205, 560)),
        ("14_interview_history", (205, 445, 435, 560)),
        ("15_ai_coach_chat", (435, 445, 640, 560)),
        ("16_learning_center", (640, 445, 1024, 560)),

        # Row 5
        ("17_achievements_badges", (0, 560, 195, 682)),
        ("18_practice_goals", (195, 560, 385, 682)),
        ("19_settings", (385, 560, 565, 682)),
        ("20_admin_dashboard", (565, 560, 775, 682)),
        ("21_mobile_preview", (775, 560, 1024, 682)),
    ]

    for name, box in panels:
        cropped = img.crop(box)
        upscaled = cropped.resize((cropped.width * 2, cropped.height * 2), Image.LANCZOS)
        out_path = f"design/panels/{name}.png"
        upscaled.save(out_path, format="PNG")
        print(f"Saved {out_path} ({upscaled.size})")

    # Component crops
    # StatCard from Dashboard: x: 580..640, y: 35..65
    c_stat = img.crop((580, 35, 645, 65))
    c_stat.resize((c_stat.width * 3, c_stat.height * 3), Image.LANCZOS).save("design/components/stat_card.png")

    # ScoreRing from Resume Analysis: x: 875..925, y: 55..105
    c_ring = img.crop((880, 55, 930, 105))
    c_ring.resize((c_ring.width * 3, c_ring.height * 3), Image.LANCZOS).save("design/components/score_ring.png")

    # Live Analysis Panel from Screen 7: x: 685..755, y: 220..295
    c_live = img.crop((685, 218, 755, 295))
    c_live.resize((c_live.width * 3, c_live.height * 3), Image.LANCZOS).save("design/components/live_analysis_panel.png")

    # Video Card from Learning Center: x: 690..755, y: 485..535
    c_video = img.crop((690, 480, 755, 535))
    c_video.resize((c_video.width * 3, c_video.height * 3), Image.LANCZOS).save("design/components/video_card.png")

    # Chat Bubble from AI Coach: x: 440..550, y: 480..525
    c_chat = img.crop((440, 480, 550, 525))
    c_chat.resize((c_chat.width * 3, c_chat.height * 3), Image.LANCZOS).save("design/components/chat_bubble.png")

    # Badge Card from Achievements: x: 10..60, y: 615..660
    c_badge = img.crop((10, 615, 65, 665))
    c_badge.resize((c_badge.width * 3, c_badge.height * 3), Image.LANCZOS).save("design/components/badge_card.png")

    # Table Row from History: x: 210..430, y: 480..520
    c_table = img.crop((210, 480, 430, 520))
    c_table.resize((c_table.width * 3, c_table.height * 3), Image.LANCZOS).save("design/components/table_row.png")

    # Sidebar crop from Dashboard: x: 505..560, y: 25..120
    c_sidebar = img.crop((505, 25, 560, 120))
    c_sidebar.resize((c_sidebar.width * 3, c_sidebar.height * 3), Image.LANCZOS).save("design/components/sidebar.png")

    print("All panels and component crops saved successfully!")

if __name__ == "__main__":
    slice_panels()
