# Design System Tokens & Measurements

Extracted directly from the 21-screen UI reference (`design/ui-reference.jpeg`) and panel crops.

## 1. Color Palette

| Token | Hex Code | Role / Usage |
| :--- | :--- | :--- |
| `page-bg` | `#F5F7FB` | Main application background (White theme baseline) |
| `card-bg` | `#FFFFFF` | Primary card background |
| `card-border` | `#E5E7EB` | Subtle card & input border |
| `primary` | `#4F46E5` | Brand Indigo (buttons, active states, score rings) |
| `primary-hover` | `#4338CA` | Hover state for primary buttons |
| `primary-light` | `#EEF2FF` | Active navigation pill background / accent tint |
| `navy-panel` | `#0B1437` | Split login left hero panel & Live Interview HUD |
| `navy-card` | `#111C44` | Dark cards within navy HUD |
| `navy-border` | `#1B254B` | Dark panel borders |
| `text-primary` | `#0F172A` | Primary typography (headings, numbers, labels) |
| `text-secondary` | `#64748B` | Subtext, muted labels, timestamps |
| `success` | `#22C55E` | Excellent/Very Good badge, positive deltas, checkmarks |
| `success-light` | `#DCFCE7` | Success pill background |
| `warning` | `#F59E0B` | Good/Moderate badge, cautions, streaks |
| `warning-light` | `#FEF3C7` | Warning pill background |
| `danger` | `#EF4444` | Needs practice/critical alerts, hang up / end buttons |
| `danger-light` | `#FEE2E2` | Danger pill background |

## 2. Layout Measurements

- **Sidebar Width**: `240px` (Desktop 1440px), collapsed on mobile (`390px` uses `MobileBottomNav`)
- **Topbar Height**: `64px` (`h-16`)
- **Container Max Width**: `1440px` with fluid responsive padding (`px-4 sm:px-6 lg:px-8`)
- **Card Border Radius**: `16px` (`rounded-2xl` for cards, `rounded-xl` for inner components)
- **Button Heights**:
  - `sm`: `32px` (`h-8`, `px-3`, text `12px`)
  - `md`: `40px` (`h-10`, `px-4`, text `14px`, `rounded-xl`)
  - `lg`: `48px` (`h-12`, `px-6`, text `16px`, `rounded-xl`)
- **Donut / ScoreRing Dimensions**:
  - Standard (Cards & Reports): `120px` diameter, `10px` stroke width
  - Compact (Stats / Mobile): `80px` diameter, `8px` stroke width
- **Chart Line Width**: `2.5px` with gradient fill opacity `0.2`

## 3. Standardized Score Rating System

Shared across all 21 screens and backend evaluations:

| Score Range | Status Rating | Pill Background | Text Color | Icon / Indicator |
| :--- | :--- | :--- | :--- | :--- |
| `≥ 88` | **Excellent** | `#DCFCE7` | `#15803D` | Sparkle / Check |
| `83 – 87` | **Very Good** | `#E0F2FE` | `#0369A1` | Thumbs Up |
| `70 – 82` | **Good** | `#FEF3C7` | `#B45309` | Check Circle |
| `55 – 69` | **Needs Improvement** | `#FFEDD5` | `#C2410C` | Alert Triangle |
| `< 55` | **Needs Practice** | `#FEE2E2` | `#B91C1C` | Info / Target |

## 4. Theme Compatibility Matrix

- **White (Mockup Baseline)**: `#F5F7FB` background, `#FFFFFF` cards, `#0F172A` text.
- **Black**: `#000000` background, `#0A0A0A` cards, `#F8FAFC` text, `#4F46E5` accent.
- **Blue**: `#0B1B3F` background, `#12285C` cards, `#E8F0FF` text, `#3B82F6` accent.
- **System**: Automatically synchronizes with OS light/dark preferences.
