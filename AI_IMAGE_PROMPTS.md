# Synco — AI Image Generation Prompts

> Save this file as a reference for generating images with AI tools (Midjourney, DALL-E, Ideogram, Leonardo AI, etc.)
> After generating, export as **WebP** (quality 80-85%) for web use.

---

## Progress

| # | Section | Status | Files |
|---|---------|--------|-------|
| 1 | Logo — Logomark | ✅ Done | `logo-mark.webp` |
| 2 | Logo — Wordmark | ✅ Done | `logo-wordmark.webp` |
| 3 | Logo — App Icon | ✅ Done | `logo-app-512.png` |
| 4 | Hero Background | ✅ Done | `hero-bg.webp` |
| 5 | OG Image | ⬜ Todo | using wordmark as fallback |
| 6 | Feature Illustrations (×6) | ✅ Done | `feature-*.webp` |
| 7 | Empty States (×4) | ⬜ Todo | — |
| 8 | Error Pages (×3) | ⬜ Todo | — |
| 9 | Onboarding (×3) | ⬜ Todo | — |
| 10 | Pricing Tiers (×3) | ⬜ Todo | — |
| 11 | Email Header | ⬜ Todo | — |

**Done: 6/11** · Remaining: OG image, empty states, error pages, onboarding, pricing, email

---

## Brand Context

- **App:** Synco — shared household calendar, budget tracker & shopping list
- **Tagline:** "Your household, finally in sync"
- **Audience:** Couples & families
- **Colors:** Indigo #6366f1, Purple #8b5cf6, Navy background #0f0a2e
- **Fonts:** Plus Jakarta Sans (display), DM Sans (body)
- **Tone:** Modern, trustworthy, warm yet professional

---

## 1. LOGO — Logomark (Icon Only) ✅ DONE

> **File:** `public/images/logo-mark.webp` — used in navbar (landing, base, offline)
> **Use for:** Favicon, PWA icon, app icon, social avatar

```
A minimal, modern logomark for "Synco" — a household sync app combining shared 
calendar, budget tracking, and shopping lists for couples and families. The logo 
conveys synchronization and togetherness through a clean geometric symbol. Two 
overlapping or interlocking abstract rounded shapes that suggest two people or 
devices staying in sync. Gradient from indigo (#6366f1) to violet (#8b5cf6). 
Flat design, no text, no shadows, no 3D effects. Must be recognizable at 16x16px 
favicon and 512x512px app icon. Clean vector aesthetic like Linear, Notion, or 
Cal.com. Transparent background, centered, single continuous form. Square 1:1.
```

---

## 2. LOGO — Logomark + Wordmark ✅ DONE

> **File:** `public/images/logo-wordmark.webp` — used for OG/Twitter meta image
> **Use for:** Navbar, footer, email header, documents

```
Logo for "Synco", a modern household management web app (calendar + budget + 
shopping list). Logomark: two soft overlapping rounded shapes forming an abstract 
"S" suggesting sync/connection between two people. Colors: indigo #6366f1 to 
purple #8b5cf6 gradient. Word "Synco" to the right in Plus Jakarta Sans 700 
weight, letter-spacing -0.02em, white (#ffffff). Dark navy background (#0f0a2e). 
Flat minimal SaaS aesthetic, no gradients on text, no ornamentation. The mark 
alone must work as a favicon. Wide format ~3:1 with text.
```

---

## 3. LOGO — App Icon (PWA / Mobile) ✅ DONE

> **File:** `public/icons/logo-app-512.png` — used in PWA manifest + apple-touch-icon
> **Use for:** PWA install icon, Android/iOS home screen
> **Export:** 512x512 PNG + 192x192 PNG + maskable variants

```
App icon for "Synco" household planner. Two interlocking rounded shapes forming a 
subtle "S" representing sync between family members. Solid indigo-to-purple 
gradient (#6366f1 to #8b5cf6) on the mark, placed on deep navy (#0f0a2e) 
rounded-square background. iOS/Android app icon style — centered, bold, no text, 
no fine details that disappear at small sizes. Clean vector, flat design, 
1024x1024px.
```

---

## 4. HERO BACKGROUND — Landing Page ✅ DONE

> **File:** `public/images/hero-bg.webp` — landing hero with gradient overlay + preload
> **Use for:** Landing page hero section background behind text and CTAs
> **Export:** 1920x900 WebP, quality 80%

```
Abstract dark-themed hero background illustration for a SaaS landing page. Deep 
navy base (#0f0a2e) with subtle flowing geometric mesh gradients and soft glowing 
light trails in indigo (#6366f1) and purple (#8b5cf6). Feels like a constellation 
map or data-flow visualization fading into darkness. Premium, modern, slightly 
futuristic. No text, no people, no UI elements. Must be subtle enough to sit 
behind white text and buttons without competing. Ultra-wide 1920x900.
```

---

## 5. OG IMAGE — Social Sharing Preview ⬜ TODO

> **Status:** Using `logo-wordmark.webp` as temporary fallback — a dedicated 1200x630 OG image would be better
> **Use for:** Open Graph / Twitter Card when someone shares a Synco link
> **Export:** 1200x630 WebP

```
Social media preview card for "Synco" app. Dark navy background (#0f0a2e) with 
subtle indigo-purple gradient glow in center. The Synco logo mark (two 
interlocking rounded shapes, indigo-purple gradient) centered-left, with "Synco" 
text in white Plus Jakarta Sans 800 weight to the right. Below: tagline "Your 
household, finally in sync" in lighter gray. Small icons representing calendar, 
budget chart, and shopping cart in a row at bottom. Clean, professional, no 
clutter. 1200x630px.
```

---

## 6. FEATURE ILLUSTRATIONS — Landing Page Cards ✅ DONE

> **Files:** `public/images/feature-{calendar,budget,shopping,notifications,sync,pwa}.webp`
> **Use for:** Feature section cards on landing page (6 features)
> **Export:** 400x300 WebP each

### 6a. Shared Calendar
```
Minimal isometric illustration of a floating calendar with two colored pins/markers 
on it (one indigo #6366f1, one emerald #10b981) representing two people's events. 
Soft glow around the calendar. Dark navy background (#0f0a2e). Modern flat style 
with subtle depth. No text. 400x300px.
```

### 6b. Budget Tracker
```
Minimal isometric illustration of a floating pie chart or bar graph with coins and 
a small wallet. Colors: amber #f59e0b primary, with indigo #6366f1 accents. Soft 
glow. Dark navy background (#0f0a2e). Modern flat style, clean lines. No text. 
400x300px.
```

### 6c. Shopping List
```
Minimal isometric illustration of a floating checklist/notepad with grocery items 
being checked off, a small shopping cart nearby. Colors: emerald #10b981 primary, 
with subtle white accents. Soft glow. Dark navy background (#0f0a2e). Modern flat 
style. No text. 400x300px.
```

### 6d. Notifications
```
Minimal isometric illustration of a floating phone with notification bell and 
small alert bubbles radiating outward. Colors: pink #ec4899 primary, with white 
accents. Soft glow. Dark navy background (#0f0a2e). Modern flat style. No text. 
400x300px.
```

### 6e. Google Sync
```
Minimal isometric illustration of two devices (phone and laptop) with circular 
sync arrows between them. Colors: blue #3b82f6 primary, with white sync arrows. 
Soft glow. Dark navy background (#0f0a2e). Modern flat style. No text. 400x300px.
```

### 6f. Works Everywhere (PWA)
```
Minimal isometric illustration of multiple floating devices — phone, tablet, 
laptop — arranged in a fan/cascade, all showing the same screen. Colors: violet 
#8b5cf6 primary, with white screen accents. Soft glow. Dark navy background 
(#0f0a2e). Modern flat style. No text. 400x300px.
```

---

## 7. EMPTY STATE ILLUSTRATIONS ⬜ TODO

> **Use for:** Shown when a section has no data yet (motivates user to add content)
> **Export:** 300x250 WebP each

### 7a. No Events
```
Friendly minimal illustration of an empty calendar page with a subtle dotted 
outline where events would go, and a small "+" sparkle. Soft indigo (#6366f1) 
tones on dark transparent background. Gentle, inviting, not sad. Line-art style 
with soft glow accents. No text. 300x250px.
```

### 7b. No Budget Data
```
Friendly minimal illustration of an empty chart/graph frame with a small coin 
floating nearby and sparkle accents suggesting "start here." Soft amber (#f59e0b) 
and indigo tones on dark transparent background. Line-art style. No text. 
300x250px.
```

### 7c. Empty Shopping List
```
Friendly minimal illustration of a blank notepad/checklist with a small pencil and 
sparkle suggesting "add your first item." Soft emerald (#10b981) tones on dark 
transparent background. Line-art style. No text. 300x250px.
```

### 7d. No Notifications
```
Friendly minimal illustration of a quiet bell with small "zzz" or peaceful waves 
around it, suggesting everything is in order. Soft pink (#ec4899) tones on dark 
transparent background. Line-art style. No text. 300x250px.
```

---

## 8. ERROR PAGE ILLUSTRATIONS ⬜ TODO

> **Use for:** 404 Not Found, 500 Server Error, Offline page
> **Export:** 400x300 WebP each

### 8a. 404 — Page Not Found
```
Whimsical minimal illustration of a calendar page flying away or a disconnected 
puzzle piece floating in space. Indigo (#6366f1) and purple (#8b5cf6) tones on 
dark navy (#0f0a2e). Playful but not childish — maintains the app's premium feel. 
No text. 400x300px.
```

### 8b. 500 — Server Error
```
Minimal illustration of a small calendar icon with a subtle glitch effect or 
static lines through it. Indigo and red-ish purple tones on dark navy (#0f0a2e). 
Suggests "something went wrong" without being alarming. No text. 400x300px.
```

### 8c. Offline
```
Minimal illustration of a cloud with a crossed-out wifi signal, with the Synco 
logo mark faintly visible behind it. Soft muted indigo tones on dark navy 
(#0f0a2e). Calm, reassuring — "you'll be back online soon." No text. 400x300px.
```

---

## 9. ONBOARDING / WELCOME ILLUSTRATIONS ⬜ TODO

> **Use for:** First-time user walkthrough or welcome modal
> **Export:** 500x400 WebP each

### 9a. Welcome — Connect Your Household
```
Warm illustration of two abstract human silhouettes (simple geometric shapes, not 
realistic) connecting through a glowing sync line/circle. Indigo and purple 
gradient tones on dark navy. Feels welcoming and inclusive — couple or family 
joining together. Modern, minimal. No text. 500x400px.
```

### 9b. Step 2 — Set Up Calendar
```
Illustration of hands (abstract, geometric) placing colorful event blocks onto a 
calendar grid. Indigo primary with emerald and amber accent blocks. Dark navy 
background. Modern minimal style. No text. 500x400px.
```

### 9c. Step 3 — Track Budget
```
Illustration of a friendly graph trending upward with small coin/money icons 
floating around it. Amber and indigo tones on dark navy. Suggests financial 
clarity and control. Modern minimal. No text. 500x400px.
```

---

## 10. PRICING PAGE — Plan Tier Illustrations ⬜ TODO

> **Use for:** Pricing cards to visually differentiate Free vs Pro vs Family+
> **Export:** 200x200 WebP each

### 10a. Free Tier
```
Simple clean icon illustration: a single small calendar with a checkmark. Muted 
white/gray tones with subtle indigo hint. On dark background. Minimal, 
understated. 200x200px.
```

### 10b. Pro Tier
```
Elevated icon illustration: a calendar with a glowing star/crown above it, 
radiating light. Vibrant indigo (#6366f1) to purple (#8b5cf6) gradient with bright 
glow. On dark background. Premium feel. 200x200px.
```

### 10c. Family+ Tier
```
Warm icon illustration: multiple overlapping calendars (2-3) with a heart or 
connection symbol between them. Emerald (#10b981) and indigo tones with warm glow. 
On dark background. Community/family feel. 200x200px.
```

---

## 11. EMAIL HEADER — Notification Emails ⬜ TODO

> **Use for:** Top banner in transactional/notification emails
> **Export:** 600x120 WebP

```
Slim email header banner for Synco notifications. Dark navy (#0f0a2e) background 
with subtle indigo-to-purple gradient strip at top (3px). Synco logo mark 
centered or left-aligned. Clean, professional, lightweight. No heavy imagery — 
must load fast in email clients. 600x120px.
```

---

## Usage Guide

### After generating images:

1. **Export as WebP** — quality 80-85% for photos/illustrations, 90% for logo/icons
2. **Place files in** `public/images/` (create directory) or `public/icons/` for logo variants
3. **Naming convention:** `hero-bg.webp`, `feature-calendar.webp`, `empty-no-events.webp`, etc.
4. **Reference in templates:** `<img src="/static/images/hero-bg.webp" alt="..." loading="lazy">`
5. **For logo SVG:** Keep current `public/icons/logo.svg` and add raster variants alongside
6. **PWA icons:** Export logo at 192x192 and 512x512 PNG (not WebP — PWA manifest needs PNG)
7. **Lazy load** all non-critical images: `loading="lazy"` attribute
8. **Provide fallbacks** for older browsers: `<picture>` element with PNG fallback

### Priority order for maximum impact:
1. Logo (sections 1-3) — brand identity
2. Hero background (section 4) — first impression
3. OG image (section 5) — social sharing
4. Feature illustrations (section 6) — landing page richness
5. Empty states (section 7) — in-app polish
6. Error pages (section 8) — completeness
7. Onboarding (section 9) — first-run experience
8. Pricing illustrations (section 10) — conversion
9. Email header (section 11) — transactional polish
