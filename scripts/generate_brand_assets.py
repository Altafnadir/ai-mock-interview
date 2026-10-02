import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = r"d:\ai-mock-interview\frontend\public\brand"
SRC_LOGO = r"d:\ai-mock-interview\assets\logo-original.png"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load source image and remove background cleanly
src_img = Image.open(SRC_LOGO).convert("RGBA")
arr = np.array(src_img, dtype=float)

# Background is [254, 254, 254]
# Calculate color difference from pure white/near white
diff = np.max(np.abs(arr[:, :, :3] - 254.0), axis=2)

# Anti-aliased alpha thresholding:
# diff < 6: fully transparent (alpha = 0)
# diff > 30: fully opaque (alpha = 255)
# between 6 and 30: linear ramp to avoid jagged/pixelated edges
alpha = np.clip((diff - 6.0) / (30.0 - 6.0), 0.0, 1.0) * 255.0

# Preserve foreground RGB and set smooth alpha
arr[:, :, 3] = alpha
clean_img = Image.fromarray(arr.astype(np.uint8), mode="RGBA")

# Bounding box of non-transparent content
bbox = clean_img.getbbox()
cropped_icon = clean_img.crop(bbox)

# Add square padding (10% on each side) so icon is centered
w, h = cropped_icon.size
max_dim = max(w, h)
pad = int(max_dim * 0.08)
square_dim = max_dim + 2 * pad
icon_square = Image.new("RGBA", (square_dim, square_dim), (0, 0, 0, 0))
offset_x = (square_dim - w) // 2
offset_y = (square_dim - h) // 2
icon_square.paste(cropped_icon, (offset_x, offset_y), cropped_icon)

print("Icon processed cleanly. Square dimensions:", square_dim)

# --- 2. Generate logo-icon.png (High-Res 512x512 transparent) ---
icon_512 = icon_square.resize((512, 512), Image.Resampling.LANCZOS)
icon_512.save(os.path.join(OUTPUT_DIR, "logo-icon.png"), "PNG", optimize=True)

# --- 3. Generate logo-icon-dark.png (Optimized for dark background) ---
# Dark mode icon: slightly increase luminance/vibrancy so cyan & royal blue pop on dark slate
icon_dark = icon_512.copy()
# Subtle cyan outer glow for dark backgrounds
glow = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow.paste(icon_dark, (0, 0), icon_dark)
icon_dark.save(os.path.join(OUTPUT_DIR, "logo-icon-dark.png"), "PNG", optimize=True)

# --- 4. Font setup for Full & Stacked logos ---
font_path_bold = r"C:\Windows\Fonts\segoeuib.ttf"
font_path_reg = r"C:\Windows\Fonts\segoeui.ttf"

# --- 5. Generate logo-full.png (Horizontal, Light Mode) ---
# Canvas: 900 x 200 (icon 160x160 + "Mock Interview AI" + Tagline)
canvas_w, canvas_h = 920, 200
full_light = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
icon_160 = icon_square.resize((160, 160), Image.Resampling.LANCZOS)
full_light.paste(icon_160, (20, 20), icon_160)

draw_light = ImageDraw.Draw(full_light)
font_title = ImageFont.truetype(font_path_bold, 58)
font_badge = ImageFont.truetype(font_path_bold, 40)
font_tagline = ImageFont.truetype(font_path_reg, 24)

# "Mock Interview" in Deep Slate (#0f172a)
# "AI" in Royal Blue gradient / accent (#1858e8)
title_text = "Mock Interview"
draw_light.text((200, 42), title_text, fill=(15, 23, 42, 255), font=font_title)

# Draw AI badge next to title
bbox_title = draw_light.textbbox((200, 42), title_text, font=font_title)
ai_x = bbox_title[2] + 16
ai_y = 48
# Gradient-like AI badge pill
badge_w = 78
badge_h = 56
draw_light.rounded_rectangle([(ai_x, ai_y), (ai_x + badge_w, ai_y + badge_h)], radius=12, fill=(24, 88, 232, 255))
draw_light.text((ai_x + 15, ai_y + 4), "AI", fill=(255, 255, 255, 255), font=font_badge)

# Tagline below
draw_light.text((202, 118), "Practice. Analyze. Get Hired.", fill=(100, 116, 139, 255), font=font_tagline)
full_light.save(os.path.join(OUTPUT_DIR, "logo-full.png"), "PNG", optimize=True)

# --- 6. Generate logo-full-dark.png (Horizontal, Dark Mode) ---
full_dark = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
full_dark.paste(icon_160, (20, 20), icon_160)
draw_dark = ImageDraw.Draw(full_dark)

# "Mock Interview" in Crisp White (#ffffff)
draw_dark.text((200, 42), title_text, fill=(255, 255, 255, 255), font=font_title)
# Badge pill in electric cyan / blue
draw_dark.rounded_rectangle([(ai_x, ai_y), (ai_x + badge_w, ai_y + badge_h)], radius=12, fill=(11, 176, 232, 255))
draw_dark.text((ai_x + 15, ai_y + 4), "AI", fill=(15, 23, 42, 255), font=font_badge)
# Tagline in Light Slate (#94a3b8)
draw_dark.text((202, 118), "Practice. Analyze. Get Hired.", fill=(148, 163, 184, 255), font=font_tagline)
full_dark.save(os.path.join(OUTPUT_DIR, "logo-full-dark.png"), "PNG", optimize=True)

# --- 7. Generate logo-stacked.png (Vertical, Icon Above Name) ---
stacked_w, stacked_h = 500, 500
stacked = Image.new("RGBA", (stacked_w, stacked_h), (0, 0, 0, 0))
icon_260 = icon_square.resize((260, 260), Image.Resampling.LANCZOS)
stacked.paste(icon_260, ((stacked_w - 260) // 2, 30), icon_260)

draw_stk = ImageDraw.Draw(stacked)
font_stk_title = ImageFont.truetype(font_path_bold, 44)
font_stk_sub = ImageFont.truetype(font_path_reg, 20)

stk_title = "Mock Interview AI"
bbox_stk = draw_stk.textbbox((0, 0), stk_title, font=font_stk_title)
tw = bbox_stk[2] - bbox_stk[0]
draw_stk.text(((stacked_w - tw) // 2, 320), stk_title, fill=(15, 23, 42, 255), font=font_stk_title)

stk_tag = "Practice. Analyze. Get Hired."
bbox_tag = draw_stk.textbbox((0, 0), stk_tag, font=font_stk_sub)
tgw = bbox_tag[2] - bbox_tag[0]
draw_stk.text(((stacked_w - tgw) // 2, 385), stk_tag, fill=(100, 116, 139, 255), font=font_stk_sub)
stacked.save(os.path.join(OUTPUT_DIR, "logo-stacked.png"), "PNG", optimize=True)

# --- 8. Favicons and Icons ---
fav_16 = icon_square.resize((16, 16), Image.Resampling.LANCZOS)
fav_16.save(os.path.join(OUTPUT_DIR, "favicon-16.png"), "PNG")

fav_32 = icon_square.resize((32, 32), Image.Resampling.LANCZOS)
fav_32.save(os.path.join(OUTPUT_DIR, "favicon-32.png"), "PNG")

fav_48 = icon_square.resize((48, 48), Image.Resampling.LANCZOS)

# Multi-resolution favicon.ico
fav_32.save(
    os.path.join(OUTPUT_DIR, "favicon.ico"),
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48)]
)
# Also place favicon.ico in root frontend/public/
fav_32.save(
    r"d:\ai-mock-interview\frontend\public\favicon.ico",
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48)]
)

# Apple touch icon 180x180
apple_icon = icon_square.resize((180, 180), Image.Resampling.LANCZOS)
apple_icon.save(os.path.join(OUTPUT_DIR, "apple-touch-icon.png"), "PNG")

# Android Chrome icons
icon_192 = icon_square.resize((192, 192), Image.Resampling.LANCZOS)
icon_192.save(os.path.join(OUTPUT_DIR, "android-chrome-192.png"), "PNG")

icon_512 = icon_square.resize((512, 512), Image.Resampling.LANCZOS)
icon_512.save(os.path.join(OUTPUT_DIR, "android-chrome-512.png"), "PNG")

# --- 9. Social Open Graph Banner: og-image.png (1200x630) ---
og = Image.new("RGBA", (1200, 630), (10, 15, 30, 255))
og_draw = ImageDraw.Draw(og)

# Subtle background radial glow
for r in range(400, 0, -20):
    alpha_glow = int(18 * (1.0 - r / 400.0))
    og_draw.ellipse([600 - r, 315 - r, 600 + r, 315 + r], fill=(24, 88, 232, alpha_glow))

# Large icon centered-left: 360x360
icon_360 = icon_square.resize((360, 360), Image.Resampling.LANCZOS)
og.paste(icon_360, (100, 135), icon_360)

# Typography on right
font_og_title = ImageFont.truetype(font_path_bold, 68)
font_og_sub = ImageFont.truetype(font_path_bold, 36)
font_og_desc = ImageFont.truetype(font_path_reg, 24)

og_draw.text((510, 180), "Mock Interview", fill=(255, 255, 255, 255), font=font_og_title)
# AI Badge Pill
og_draw.rounded_rectangle([(1030, 186), (1125, 256)], radius=16, fill=(11, 176, 232, 255))
font_og_ai = ImageFont.truetype(font_path_bold, 48)
og_draw.text((1045, 192), "AI", fill=(10, 15, 30, 255), font=font_og_ai)

og_draw.text((512, 275), "Practice. Analyze. Get Hired.", fill=(11, 176, 232, 255), font=font_og_sub)
og_draw.text((512, 345), "AI-Powered Multimodal Interview Preparation Platform", fill=(203, 213, 225, 255), font=font_og_desc)
og_draw.text((512, 385), "Computer Vision • Speech Acoustics • STAR Method • Gemini Feedback", fill=(148, 163, 184, 255), font=font_og_desc)

# Border line
og_draw.rounded_rectangle([(2, 2), (1198, 628)], radius=20, outline=(30, 41, 59, 255), width=2)
og.convert("RGB").save(os.path.join(OUTPUT_DIR, "og-image.png"), "JPEG", quality=92, optimize=True)

# --- 10. Generate Vector SVG representation (logo-icon.svg & logo-full.svg) ---
svg_icon_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="none">
  <defs>
    <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B32C8" />
      <stop offset="60%" stop-color="#1858E8" />
      <stop offset="100%" stop-color="#0BB0E8" />
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0BB0E8" />
      <stop offset="100%" stop-color="#38BDF8" />
    </linearGradient>
  </defs>
  <!-- Embedded High-Fidelity Silhouette with Scalable Styling -->
  <g transform="translate(32, 32)">
    <!-- Candidate Head Silhouette Profile -->
    <path d="M 224 40 C 130 40 50 115 50 215 C 50 260 65 295 85 330 L 85 410 C 85 425 95 435 110 435 L 180 435 C 190 435 198 425 198 410 L 198 385 C 220 395 242 395 260 385 C 275 365 285 340 285 315 C 295 310 305 300 305 285 C 305 272 295 265 285 260 C 295 240 310 220 310 190 C 310 105 280 40 224 40 Z" fill="none" stroke="url(#primaryGrad)" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- AI Vision Camera Eye / Neural Aperture -->
    <circle cx="190" cy="180" r="70" fill="none" stroke="url(#primaryGrad)" stroke-width="18" stroke-dasharray="85 25"/>
    <circle cx="190" cy="180" r="42" fill="none" stroke="url(#primaryGrad)" stroke-width="16"/>
    <circle cx="190" cy="180" r="22" fill="url(#cyanGrad)"/>
    <circle cx="200" cy="172" r="7" fill="#FFFFFF"/>
    
    <!-- Speech Soundwave Vibrations -->
    <path d="M 330 250 A 40 40 0 0 1 330 310" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>
    <path d="M 360 230 A 70 70 0 0 1 360 330" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>
    <path d="M 390 210 A 100 100 0 0 1 390 350" fill="none" stroke="url(#cyanGrad)" stroke-width="18" stroke-linecap="round"/>
  </g>
</svg>'''

with open(os.path.join(OUTPUT_DIR, "logo-icon.svg"), "w", encoding="utf-8") as f:
    f.write(svg_icon_content)

svg_full_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 200" fill="none">
  <defs>
    <linearGradient id="fullPrim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B32C8" />
      <stop offset="60%" stop-color="#1858E8" />
      <stop offset="100%" stop-color="#0BB0E8" />
    </linearGradient>
    <linearGradient id="fullCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0BB0E8" />
      <stop offset="100%" stop-color="#38BDF8" />
    </linearGradient>
  </defs>
  <g transform="translate(10, 15) scale(0.33)">
    <!-- Head Profile -->
    <path d="M 224 40 C 130 40 50 115 50 215 C 50 260 65 295 85 330 L 85 410 C 85 425 95 435 110 435 L 180 435 C 190 435 198 425 198 410 L 198 385 C 220 395 242 395 260 385 C 275 365 285 340 285 315 C 295 310 305 300 305 285 C 305 272 295 265 285 260 C 295 240 310 220 310 190 C 310 105 280 40 224 40 Z" fill="none" stroke="url(#fullPrim)" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="190" cy="180" r="70" fill="none" stroke="url(#fullPrim)" stroke-width="18" stroke-dasharray="85 25"/>
    <circle cx="190" cy="180" r="42" fill="none" stroke="url(#fullPrim)" stroke-width="16"/>
    <circle cx="190" cy="180" r="22" fill="url(#fullCyan)"/>
    <circle cx="200" cy="172" r="7" fill="#FFFFFF"/>
    <path d="M 330 250 A 40 40 0 0 1 330 310" fill="none" stroke="url(#fullCyan)" stroke-width="18" stroke-linecap="round"/>
    <path d="M 360 230 A 70 70 0 0 1 360 330" fill="none" stroke="url(#fullCyan)" stroke-width="18" stroke-linecap="round"/>
    <path d="M 390 210 A 100 100 0 0 1 390 350" fill="none" stroke="url(#fullCyan)" stroke-width="18" stroke-linecap="round"/>
  </g>
  <text x="180" y="90" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="54" fill="#0F172A">Mock Interview</text>
  <rect x="585" y="44" width="76" height="54" rx="12" fill="#1858E8" />
  <text x="602" y="85" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="38" fill="#FFFFFF">AI</text>
  <text x="182" y="132" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="22" fill="#64748B">Practice. Analyze. Get Hired.</text>
</svg>'''

with open(os.path.join(OUTPUT_DIR, "logo-full.svg"), "w", encoding="utf-8") as f:
    f.write(svg_full_content)

print("Brand assets successfully generated in", OUTPUT_DIR)
