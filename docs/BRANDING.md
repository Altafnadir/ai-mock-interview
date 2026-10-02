# Brand Identity Guide — Mock Interview AI

> **Official Brand System & Visual Identity Standards**  
> *Practice. Analyze. Get Hired.*

---

## 1. Brand Identity Overview

- **Brand Name**: `Mock Interview AI`
- **Tagline**: `Practice. Analyze. Get Hired.`
- **Primary Domain**: AI-Driven Multi-Modal Interview Preparation & Assessment
- **Selected Logo**: Option 2 (Candidate Silhouette + Hexagonal Neural Node + Concentric Audio Soundwaves)
- **Original Source Master**: `assets/logo-original.png` (Archived in `logo/OPTION 2.png`)

---

## 2. Brand Color Palette & Design Tokens

| Token | Hex Code | RGB | HSL | Semantic Role & WCAG Compliance |
| :--- | :--- | :--- | :--- | :--- |
| **`primary`** | `#1858E8` | `rgb(24, 88, 232)` | `hsl(222, 82%, 50%)` | Primary brand button, active states, key highlights. WCAG AA compliant on light backgrounds. |
| **`primary-dark`** | `#3B32C8` | `rgb(59, 50, 200)` | `hsl(244, 60%, 49%)` | Deep cognitive indigo, dark mode contrasts, header gradients, and interactive hover states. |
| **`accent`** | `#0BB0E8` | `rgb(11, 176, 232)` | `hsl(195, 91%, 48%)` | Electric cyan, AI feedback badges, score highlights, waveform animations, and focal points. |
| **`bg-dark`** | `#0B0F19` | `rgb(11, 15, 25)` | `hsl(223, 39%, 7%)` | Dark mode background (Deep Obsidian Navy). |
| **`bg-light`** | `#F8FAFC` | `rgb(248, 250, 252)` | `hsl(210, 40%, 98%)` | Light mode background (Clean Slate White). |

### CSS Variables & Tailwind Tokens
```css
:root {
  --brand-primary: #1858e8;
  --brand-primary-dark: #3b32c8;
  --brand-accent: #0bb0e8;
  --brand-bg-dark: #0b0f19;
  --brand-bg-light: #f8fafc;
}
```

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#1858e8',
          'primary-dark': '#3b32c8',
          accent: '#0bb0e8',
        }
      }
    }
  }
}
```

---

## 3. Brand Assets & Directory Structure

All production brand assets reside in `frontend/public/brand/` and are mirrored for backend reports in `backend/app/reports/assets/`.

| File | Resolution | Type | Location | Usage |
| :--- | :--- | :--- | :--- | :--- |
| `logo-icon.png` | 512×512 | PNG (32-bit Alpha) | `frontend/public/brand/` | Square emblem, collapsed sidebar, mobile navbar, avatars |
| `logo-icon-dark.png` | 512×512 | PNG (32-bit Alpha) | `frontend/public/brand/` | High-contrast variant optimized for dark UI themes |
| `logo-full.png` | 920×200 | PNG (32-bit Alpha) | `frontend/public/brand/` | Horizontal lockup (Icon + Mock Interview AI typography) |
| `logo-full-dark.png` | 920×200 | PNG (32-bit Alpha) | `frontend/public/brand/` | Horizontal lockup for dark surfaces with pure white typography |
| `logo-stacked.png` | 500×500 | PNG (32-bit Alpha) | `frontend/public/brand/` | Vertical stacked format for splash screens and landing headers |
| `logo-icon.svg` | Scalable Vector | SVG XML | `frontend/public/brand/` | Lossless vector rendering |
| `logo-full.svg` | Scalable Vector | SVG XML | `frontend/public/brand/` | Lossless vector lockup |
| `favicon.ico` | 16/32/48 multi-res | Windows Icon | `frontend/public/` | Browser tab favicon |
| `favicon-16.png` | 16×16 | PNG | `frontend/public/brand/` | Low-dpi desktop browser tabs |
| `favicon-32.png` | 32×32 | PNG | `frontend/public/brand/` | Standard and Retina desktop browser tabs |
| `apple-touch-icon.png` | 180×180 | PNG | `frontend/public/brand/` | iOS Home Screen bookmark icon |
| `android-chrome-192.png` | 192×192 | PNG | `frontend/public/brand/` | Android PWA launcher standard density |
| `android-chrome-512.png` | 512×512 | PNG | `frontend/public/brand/` | Android PWA splash screen high density |
| `og-image.png` | 1200×630 | PNG (79 KB) | `frontend/public/brand/` | OpenGraph & Twitter social preview banner |

---

## 4. Usage Across Application Surfaces

### 4.1. Web Frontend & Mobile Viewports
- **Landing Page (`/`)**: Centered glassmorphic navbar with `logo-full.png`, responsive to `logo-icon.png` on small screens. Footer embeds centered logo lockup with social links.
- **Authentication Flows (`/login`, `/register`, `/verify-otp`, `/forgot-password`, `/reset-password`)**: Stacked logo emblem positioned above form cards.
- **Candidate Layout**: Full horizontal logo when sidebar is expanded; icon-only when collapsed or displayed on mobile screens (`< 768px`).
- **Admin Portal (`/admin`)**: Horizontal logo accompanied by a distinctive violet `"Admin"` badge.
- **Shared Assessment Reports (`/shared/:token`)**: Clean brand header embedding `logo-full.png` with a "Verified Report" seal.

### 4.2. Transactional HTML Emails
- Header banner features inline base64-encoded `logo-full.png` with fallback text `Mock Interview AI`.
- Styled with brand palette buttons (`#1858E8`) and clean typography.

### 4.3. Generated PDF Reports & Posters
- **Full Comprehensive PDF (`report_{id}.pdf`)**: Header features `logo-icon.png` beside session metadata and candidate credentials.
- **1-Page AI Performance Summary (`summary_{id}.pdf`)**: Compact header emblem.
- **Performance Poster (`poster_{id}.pdf`)**: Dark-themed high-resolution performance badge with centered `logo-icon.png` and `#1858E8` accent border.

---

## 5. Design Guidelines & Sizing Rules

### 5.1. Minimum Sizing
- **Favicon**: Minimum 16×16 px.
- **Icon Only**: Minimum 24×24 px in compact menus; 32×32 px in standard navigational bars.
- **Full Horizontal Logo**: Minimum width 140 px (height ~32 px) to guarantee legible typography.

### 5.2. Clear Space Rule
- Maintain a minimum clear space surrounding the logo equal to **50% of the icon's height ($0.5 \times H$)** on all sides. No UI elements, text, or borders may encroach within this perimeter.

### 5.3. What NOT to Do
- ❌ **Do not distort or stretch** the logo aspect ratio. Always preserve 1:1 for the icon and proportional scaling for horizontal lockups.
- ❌ **Do not alter brand colors** or replace them with non-palette hues (e.g., lime green or bright magenta).
- ❌ **Do not place dark logo variants on dark backgrounds** or white variants on light backgrounds.
- ❌ **Do not add heavy drop shadows or rainbow glow effects** to the logo mark.
- ❌ **Do not separate icon components** or redraw individual vectors.
