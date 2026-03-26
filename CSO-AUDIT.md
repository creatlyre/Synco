# Dobry Plan — CSO Sales & Growth Audit

> **Date:** 2026-03-25
> **Scope:** Full commercial audit — brand strategy, marketing, pricing, wording, distribution channels, monetization opportunities, and growth levers.
> **Audience:** Founder / executive decision-making

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Brand & Positioning Audit](#2-brand--positioning-audit)
3. [Pricing & Monetization Audit](#3-pricing--monetization-audit)
4. [Marketing & Distribution Channels](#4-marketing--distribution-channels)
5. [Wording & Copy Audit](#5-wording--copy-audit)
6. [Sales Funnel Analysis](#6-sales-funnel-analysis)
7. [Feature Gating & Conversion Levers](#7-feature-gating--conversion-levers)
8. [Competitive Positioning](#8-competitive-positioning)
9. [Untapped Revenue Opportunities](#9-untapped-revenue-opportunities)
10. [Risk Assessment](#10-risk-assessment)
11. [Prioritized Action Plan](#11-prioritized-action-plan)

---

## 1. Executive Summary

### What Dobry Plan Is Today

Dobry Plan is an open-source (AGPL-3.0) household management app combining a shared calendar, budget tracker, and shopping list — targeting couples and families in Poland. It ships as a server-rendered FastAPI + HTMX web app with PWA capabilities and an Android TWA wrapper.

### Revenue Model

| Stream | Pricing | Status |
|--------|---------|--------|
| SaaS Free | 0 PLN | Live |
| SaaS Pro | 19 PLN/mo · 15 PLN/mo annual | Live (Stripe) |
| SaaS Family Plus | 29 PLN/mo · 24 PLN/mo annual | Live (Stripe) |
| Self-Hosted License | 199 PLN one-time | Live (Stripe) |

### Verdict

The product is **technically complete** and well-engineered (581 tests, E2E coverage, dual-language i18n, Stripe billing). The critical gap is **go-to-market execution** — the product needs distribution, social proof, and conversion optimization to turn users into paying customers.

**Overall Sales Readiness Score: 6.5/10**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Product completeness | 9/10 | Feature-rich, well-tested |
| Brand identity | 7/10 | Strong palette & voice, logo needs redo |
| Pricing structure | 7/10 | Solid tiers, some gaps (see §3) |
| Marketing copy | 7/10 | Good foundation, needs sharpening (see §5) |
| Distribution channels | 3/10 | No active channels beyond landing page |
| Social proof | 1/10 | Zero testimonials, reviews, or case studies |
| Conversion optimization | 5/10 | Funnel exists but untested with real traffic |
| SEO readiness | 6/10 | Structured data present, no content strategy |

---

## 2. Brand & Positioning Audit

### 2.1 Current Brand Identity

| Element | Status | Assessment |
|---------|--------|------------|
| Name | "Dobry Plan" | Excellent — memorable, locally resonant ("Good Plan" in Polish), .app domain secured |
| Tagline (EN) | "Your household, finally in sync" | Strong — outcome-focused, relatable |
| Tagline (PL) | "Twój dom, wreszcie ogarnięty" | Excellent — colloquial, emotionally resonant |
| Secondary tagline | "Dobry Plan na każdy dzień" | Good — everyday usage positioning |
| Color palette | Indigo → Violet on dark navy | Professional, distinctive, good contrast |
| Typography | Plus Jakarta Sans + DM Sans | Modern SaaS standard, good readability |
| Voice & tone | Friendly, practical, outcome-focused | Well-defined, consistently applied |
| Logo | Calendar + sync arrows | Concept is right but execution marked for redo (3/11 assets) |

### 2.2 Brand Strengths

- **Name resonance:** "Dobry Plan" works in both Polish and international contexts — short, pronounceable, positive connotation.
- **Visual identity:** The dark indigo/violet palette is distinctive and avoids the "generic SaaS blue" trap.
- **Voice consistency:** Every i18n string follows the brand voice guidelines — no jargon, benefit-led, direct address ("you/your").
- **Trust positioning:** Open-source + GDPR + no tracking cookies is a powerful differentiator in the Polish market.

### 2.3 Brand Weaknesses & Gaps

| Issue | Severity | Recommendation |
|-------|----------|----------------|
| **Logo assets incomplete** — 3 of 11 core visuals need redo, 6 still todo | HIGH | Block launch marketing until logo suite is finalized. Inconsistent logos erode perceived quality. |
| **No OG image** — social shares currently fall back to wordmark | MEDIUM | Create a purpose-built OG image (1200x630) showing the product in use. Social sharing is the #1 organic discovery channel. |
| **No app store screenshots** — TWA listed but no Play Store presence | MEDIUM | Even a "coming soon" listing captures intent. |
| **No brand video** — landing page is text + static images only | LOW | A 30-second demo video would boost conversion 20-30% (industry average). |
| **Single-founder branding** — "Built by a developer who needed it" | NOTE | This is a strength NOW (authentic indie maker), but will need evolution to "trusted team" messaging at scale. |

### 2.4 Positioning Map

```
                        HIGH PRICE
                            |
              Coynt          |         Splitwise
              (PL)           |         (Global)
                             |
   SINGLE-PURPOSE ——————————+———————————— ALL-IN-ONE
                             |
              Google          |         Dobry Plan
              Calendar        |         (you are here)
              (Free)          |
                             |
                        LOW PRICE
```

**Current position:** Low-price, all-in-one household tool.
**Strategic advantage:** No direct competitor combines calendar + budget + shopping in one app for the Polish market.

---

## 3. Pricing & Monetization Audit

### 3.1 Current Pricing Architecture

| Tier | Monthly | Annual | Annual Savings | Target Segment |
|------|---------|--------|---------------|----------------|
| Free | 0 PLN | — | — | First-time users, evaluation |
| Pro | 19 PLN/mo | 180 PLN/yr (15/mo) | 17% | Active households |
| Family Plus | 29 PLN/mo | 288 PLN/yr (24/mo) | 17% | Larger families |
| Self-Hosted | — | 199 PLN (one-time) | — | Privacy-conscious, orgs |

### 3.2 Pricing Strengths

- **Aggressive free tier** removes all signup friction — "Free forever, no credit card" is a proven conversion headline.
- **PLN pricing** is correct for Polish market — avoids cognitive friction of EUR/USD conversion.
- **Annual discount at 17%** is standard SaaS best practice.
- **Self-hosted one-time model** captures a distinct segment (devs, orgs with AGPL concerns).

### 3.3 Pricing Weaknesses & Opportunities

| Issue | Impact | Recommendation |
|-------|--------|----------------|
| **Pro → Family Plus gap is unclear** | Users can't justify the jump | Family Plus only adds "extended storage" and "priority support" — these are vague. Specify concrete limits (e.g., "5 years of budget history" vs "3 years") and add *at least one exclusive feature*. |
| **No trial for Pro features** | Lost conversions | Offer a **14-day free trial** of Pro on every new account. Users who experience NLP quick-add and charts rarely go back. |
| **Self-hosted price may be too low** | Leaving money on table | 199 PLN (~$50) is very cheap for a commercial license. DevOps-oriented buyers expect $99-$299. Consider raising to 399 PLN or offering tiered support packages (Basic 199 PLN / Priority 499 PLN). |
| **No "per household" vs "per user" clarity** | Confusion at checkout | The pricing page doesn't clearly state whether one subscription covers the household or each user needs their own. Explicitly state: "One subscription covers your entire household." |
| **No seat-based pricing path** | Limits B2B | If small offices or co-living situations adopt Dobry Plan, there's no 5+ user pricing. Consider a "Team" tier at 49-79 PLN/mo for 5-10 members. |
| **Annual-only discount is weak** | Low annual adoption | 17% is the floor. Consider 20-25% annual discount, or offer "2 months free" framing instead of percentage — it's psychologically stronger. |
| **No lifetime deal** | Missing AppSumo/indie market | A one-time lifetime deal (e.g., 499 PLN) would generate early revenue and advocacy from the Polish indie/startup community. |

### 3.4 Revenue Projections (Scenarios)

**Scenario A — Organic growth only (no paid acquisition)**

| Month | Free Users | Pro | Family Plus | Self-Hosted | MRR |
|-------|-----------|-----|-------------|-------------|-----|
| M1 | 50 | 2 | 0 | 1 | 38 PLN + 199 PLN |
| M3 | 200 | 8 | 2 | 2 | 210 PLN |
| M6 | 500 | 25 | 5 | 5 | 620 PLN |
| M12 | 1,500 | 75 | 15 | 10 | 1,860 PLN |

**Scenario B — With content marketing + 14-day Pro trial**

| Month | Free Users | Pro | Family Plus | Self-Hosted | MRR |
|-------|-----------|-----|-------------|-------------|-----|
| M3 | 400 | 20 | 4 | 3 | 496 PLN |
| M6 | 1,200 | 70 | 15 | 8 | 1,765 PLN |
| M12 | 4,000 | 250 | 50 | 20 | 6,200 PLN |

**Break-even estimate:** Railway hosting (~$5-10/mo) + Supabase (~$25/mo) + domain (~$15/yr) = ~150 PLN/mo fixed costs. Break-even at ~8 Pro subscribers.

---

## 4. Marketing & Distribution Channels

### 4.1 Current State

| Channel | Status | Assessment |
|---------|--------|------------|
| Landing page (dobryplan.app) | Live | Good foundation, needs social proof |
| Google search (SEO) | Partial | Structured data present, no blog/content |
| Google Play Store (TWA) | Config ready, not published | Major missed distribution |
| Social media | None | No Twitter/X, no Facebook, no LinkedIn presence |
| Email marketing | SMTP configured | No newsletter, no drip campaigns |
| Referral program | None | No invite incentives beyond basic sharing |
| Content marketing | None | No blog, no guides, no video |
| Community | None | No Discord/Slack/forum |
| Paid acquisition | None | No Google Ads, no Facebook Ads |
| PR / press | None | No media mentions or launch announcements |
| Product Hunt | None | Not launched |
| GitHub presence | AGPL repo exists | No promotional README for discovery |

### 4.2 Channel Priority Matrix

| Channel | Effort | Impact | Timeline | Priority |
|---------|--------|--------|----------|----------|
| **Product Hunt launch** | Low | High | 1 day | P0 — DO FIRST |
| **Google Play Store listing** | Low | Medium | 2-3 days | P0 |
| **SEO blog (Polish)** | Medium | High | Ongoing | P1 |
| **Twitter/X presence** | Low | Medium | Ongoing | P1 |
| **Email drip sequence** | Medium | High | 1 week | P1 |
| **GitHub README marketing** | Low | Low-Med | 1 day | P2 |
| **YouTube demo video** | Medium | Medium | 3-5 days | P2 |
| **Facebook groups (PL parenting/household)** | Low | Medium | Ongoing | P2 |
| **Wykop/Reddit (r/Polska)** | Low | Low-Med | 1 day | P2 |
| **Referral program** | Medium | High | 1-2 weeks | P3 |
| **Google Ads (PL keywords)** | High (cost) | Medium | Ongoing | P3 |
| **Partnership with Polish blogs** | Medium | Medium | 2-4 weeks | P3 |

### 4.3 Channel-Specific Strategies

#### Product Hunt Launch (P0)
- **Tagline:** "Open-source shared Calendar, Budget & Shopping list for households"
- **First comment (maker):** Tell the founder story — built for your wife, open-source, Polish-made
- **Timing:** Tuesday-Thursday, 00:01 PST
- **Assets needed:** 5 screenshots, 1 GIF, logo, 80-character tagline
- **Expected outcome:** 200-500 upvotes (household productivity niche), 100-300 signups

#### Google Play Store (P0)
- TWA config is complete (`app.dobryplan.twa`, Bubblewrap-generated)
- Write Play Store listing: title, short description, full description, screenshots
- **Title:** "Dobry Plan — Shared Calendar & Budget"
- **Short description:** "Household calendar, budget tracker & shopping list. Free & open source."
- Google Play listing drives organic Android installs with near-zero maintenance

#### SEO Blog Strategy (P1)
- **Target keywords (Polish):**
  - "wspólny kalendarz rodzinny" (shared family calendar)
  - "budżet domowy aplikacja" (household budget app)
  - "lista zakupów aplikacja" (shopping list app)
  - "planowanie domowe" (household planning)
  - "darmowy kalendarz dla par" (free calendar for couples)
- **Content pillars:**
  1. Household organization tips (top of funnel)
  2. Feature tutorials / how-to guides (mid funnel)
  3. Comparison posts: "Dobry Plan vs Splitwise vs Google Calendar" (bottom funnel)
  4. Self-hosting guides for technical audience
- **Publishing cadence:** 2 posts/month minimum
- **ROI:** Long-tail Polish keywords have low competition; achievable #1 rankings in 2-3 months

#### Email Drip Campaigns (P1)

**Signup → Day 7 sequence:**

| Day | Subject | Purpose |
|-----|---------|---------|
| 0 | "Welcome to Dobry Plan! Here's your first step" | Onboarding: invite household member |
| 1 | "Try quick-add: type 'dentist Thursday 3pm'" | Feature activation (NLP) |
| 3 | "Your household budget in 5 minutes" | Feature activation (budget) |
| 5 | "Shopping trips just got 30 minutes shorter" | Feature activation (shopping) |
| 7 | "You've been using the free plan for a week..." | Soft upgrade prompt (Pro trial) |

**Churned-user reactivation (7-14 days inactive):**

| Day | Subject | Purpose |
|-----|---------|---------|
| 7 | "We noticed you haven't been back" | Win-back with value reminder |
| 14 | "Your partner added 3 events this week" | Social hook / FOMO (if applicable) |

---

## 5. Wording & Copy Audit

### 5.1 High-Impact Headlines — Current vs. Recommended

| Location | Current Copy | Assessment | Recommended Alternative |
|----------|-------------|------------|------------------------|
| **Hero headline** | "Your household, finally in sync" | Strong but generic | Keep — but A/B test: "Stop double-booking. Start living." |
| **Hero sub** | "Calendar, budget, and shopping list in one place. For couples, families, and anyone sharing a household." | Too long, buries the benefit | "One app for your calendar, budget, and groceries. Built for two." |
| **Hero badge** | "Free forever • Open Source • No credit card" | Good trust signal | Keep as-is — conversion-optimized |
| **Primary CTA** | "Start for free" | Standard but safe | A/B test: "Create your household" (more specific) |
| **Secondary CTA** | "See pricing" | Too passive | "Compare plans" (implies options, not cost) |
| **Features heading** | "Everything you need — in one app" | Generic | "Three apps you use daily — combined into one" |
| **Calendar feature** | "One shared calendar, synced with Google Calendar. Never miss an appointment again." | Good | "Never miss an appointment again. One shared calendar, synced with Google." (Lead with benefit) |
| **Budget feature** | "See where every zloty goes. No more end-of-month surprises." | Excellent | Keep — strong emotional hook |
| **Shopping feature** | "Shared list auto-grouped by store aisle. Groceries in 15 minutes, not 45." | Excellent — specific time claim | Keep — concrete, measurable benefit |
| **Final CTA heading** | "Ready to run your household together?" | Weak question | "Your household is waiting. Start now." (urgency) |
| **Final CTA note** | "Free account • 30-second setup • No credit card" | Good trust micro-copy | Add: "Join 100+ households already synced" (social proof, even if aspirational at launch) |
| **Founder story heading** | "Built by a developer who needed it" | Authentic | Keep — indie maker credibility is gold |
| **Pricing page title** | "Pricing" | Bare minimum | "Simple pricing. No surprises." |
| **Pricing subtitle** | "Choose the right plan for your household" | Passive | "Every plan includes your entire household." |
| **Pro tier desc** | "For households that want more" | Vague | "Unlock the full toolkit. Charts, OCR, unlimited categories." |
| **Family Plus desc** | "Everything for the whole family" | Overlaps with Pro | "Pro + priority support & future features included." |
| **Self-hosted desc** | "Own your data. Run Dobry Plan on your own server." | Good for technical audience | Keep — speaks directly to the buyer persona |

### 5.2 Wording Gaps & Missing Copy

| Missing Element | Impact | What to Write |
|-----------------|--------|---------------|
| **Social proof** | CRITICAL | No testimonials, user counts, or review quotes anywhere. Add at least 3 testimonial blocks (can use early beta testers or own household experience). |
| **Objection handling** | HIGH | No FAQ on pricing page. Add: "Is one subscription per person or per household?", "Can I switch plans?", "What happens to my data if I cancel?" |
| **Upgrade prompts (in-app)** | HIGH | When a free-tier user hits a gate (e.g., tries to add 2nd custom category), the wording matters. Currently: none found. Recommend: "Unlock unlimited categories with Pro — try free for 14 days." |
| **Annual plan persuasion** | MEDIUM | The "Save 17%" badge is minimal. Add: "Most popular" badge on annual, or "Pay for 10 months, get 12" framing. |
| **Exit-intent / cancel flow** | MEDIUM | What copy does the user see when canceling? This is a retention moment. Add: "We'll miss you! Your data stays safe. You can reactivate anytime." |
| **Error/empty states** | LOW | Empty calendar, empty budget, empty shopping list — these are onboarding moments. Current status: "⬜ Todo" in image prompts. |
| **404 / offline page** | LOW | `public/offline.html` exists but copy not audited. Should reinforce brand voice. |

### 5.3 Polish vs. English Copy Parity

| Area | Status | Notes |
|------|--------|-------|
| Landing page | ✅ Full parity | All i18n keys present in both languages |
| Pricing page | ✅ Full parity | Both PLN currency |
| Auth pages | ✅ Full parity | Signup/login/OAuth |
| Legal pages | ⚠️ Partial | Terms/privacy/refund may need Polish legal review |
| In-app features | ✅ Full parity | Budget, calendar, shopping |
| Blog / content | ❌ N/A | No blog exists yet |
| Email templates | ⚠️ Unknown | SMTP configured but template copy not audited |

### 5.4 Keyword Density & SEO Copy

**Primary keywords (should appear on landing page):**

| Keyword (PL) | Present? | Recommendation |
|--------------|----------|----------------|
| wspólny kalendarz | ❌ | Add to meta description and H2 |
| budżet domowy | ❌ | Add to budget feature section |
| lista zakupów | ❌ | Add to shopping section |
| planowanie rodzinne | ❌ | Add to hero subtitle |
| synchronizacja kalendarza | ❌ | Add to Google Sync section |
| open source | ✅ | Present in trust badges |
| darmowa aplikacja | ❌ | Add to hero badge area |

**Assessment:** The Polish landing page is missing critical local SEO keywords. The i18n strings are written in natural Polish but don't include the search terms people actually type. Add these keywords naturally without keyword-stuffing.

---

## 6. Sales Funnel Analysis

### 6.1 Current Funnel

```
AWARENESS                    INTEREST                    ACTIVATION
Landing page ─────────────→ Pricing page ─────────────→ Signup (Google/email)
(organic/direct)             "See pricing" CTA           "Start for free" CTA
     │                            │                            │
     │ PROBLEM: No traffic        │ OK: Clear tiers            │ OK: 30-second flow
     │ sources feeding this       │                            │
     ▼                            ▼                            ▼
                                                         ENGAGEMENT
                                                    Invite partner → Create event
                                                         │
                                                         │ PROBLEM: No guided
                                                         │ onboarding or tooltips
                                                         ▼
                                                     CONVERSION
                                                    Hit free-tier limit → Upgrade
                                                         │
                                                         │ PROBLEM: Upgrade
                                                         │ prompts not found
                                                         ▼
                                                     RETENTION
                                                    Daily use → Annual renewal
                                                         │
                                                         │ PROBLEM: No retention
                                                         │ email, no engagement
                                                         │ tracking
                                                         ▼
                                                     REFERRAL
                                                    Invite others → Viral growth
                                                         │
                                                         │ PROBLEM: No referral
                                                         │ incentives
                                                         ▼
```

### 6.2 Funnel Leak Points

| Stage | Leak | Fix | Impact |
|-------|------|-----|--------|
| **Awareness → Interest** | No traffic acquisition strategy | SEO blog, Product Hunt, Google Play, social media | CRITICAL |
| **Interest → Activation** | No social proof on landing/pricing | Add testimonials, user count, "trusted by X households" | HIGH |
| **Activation → Engagement** | No onboarding wizard | Add a 3-step guided tour post-signup: invite partner → add event → explore budget | HIGH |
| **Engagement → Conversion** | No in-app upgrade prompts at feature gates | Show contextual upgrade CTA when user hits free-tier limits | HIGH |
| **Conversion → Retention** | No engagement emails, no usage dashboard | Build email drip + in-app activity digest | MEDIUM |
| **Retention → Referral** | No referral program | "Invite a friend, get 1 month Pro free" | MEDIUM |

### 6.3 Conversion Rate Benchmarks

| Metric | Industry Average (Freemium SaaS) | Target for Dobry Plan |
|--------|----------------------------------|----------------------|
| Visitor → Signup | 2-5% | 5% (strong free tier removes friction) |
| Signup → Active (Day 7) | 20-40% | 30% |
| Free → Paid | 2-5% | 3-5% |
| Monthly → Annual | 30-50% | 40% (needs stronger incentive) |
| Monthly churn | 5-8% | <5% (household stickiness helps) |

---

## 7. Feature Gating & Conversion Levers

### 7.1 Current Feature Gates

| Feature | Free | Pro | Family Plus | Gate Quality |
|---------|------|-----|-------------|-------------|
| Shared calendar | ✅ | ✅ | ✅ | N/A (core, never gate) |
| Budget tracker | ✅ | ✅ | ✅ | N/A (core) |
| Shopping list | ✅ | ✅ | ✅ | N/A (core) |
| Google Sync | ✅ | ✅ | ✅ | **RECONSIDER** — this is a power feature |
| Custom categories | 1 | ∞ | ∞ | GOOD — natural limit, users feel it quickly |
| Expense charts | ❌ | ✅ | ✅ | GOOD — visual value is obvious |
| NLP quick-add | ❌ | ✅ | ✅ | EXCELLENT — "try it, love it, upgrade" |
| OCR receipts | ❌ | ✅ | ✅ | GOOD — novelty drives upgrades |
| Email notifications | ❌ | ✅ | ✅ | OK — users may not miss what they haven't tried |
| Extended storage | ❌ | ❌ | ✅ | WEAK — what's the limit? Not specified. |
| Priority support | ❌ | ❌ | ✅ | WEAK for consumers — support tiers matter in B2B, not households |

### 7.2 Gating Recommendations

| Recommendation | Rationale |
|----------------|-----------|
| **Let free users try NLP quick-add 5 times** | Let them experience it, then gate. "You've used 5 of 5 free quick-adds this month. Upgrade for unlimited." This is the #1 conversion trigger. |
| **Show chart previews to free users** | Show a blurred/low-res budget chart with a "Unlock with Pro" overlay. Visual FOMO is powerful. |
| **Define storage limits explicitly** | "Free: 2 years history / Pro: 5 years / Family Plus: unlimited" — concrete limits drive urgrades more than vague "extended storage." |
| **Gate Google Calendar import (not export)** | Free users get export only (push to Google). Import (pull from Google) becomes a Pro feature. This creates a one-way funnel. |
| **Add "Household insights" as Pro feature** | Monthly usage summary email: "This month, your household tracked 45 events, spent 3,200 PLN, and saved 40 minutes on shopping." People love data about data. |

### 7.3 Upgrade Trigger Points (Where to Show CTAs)

| Trigger | User Action | CTA Copy |
|---------|-------------|----------|
| Hit 1 custom category limit | Tries to create 2nd category | "One more category? Unlock unlimited with Pro." |
| View budget without charts | Opens budget overview page | Blurred chart preview: "See where your money goes — visually." |
| Type NLP quick-add query (if gated) | Uses quick-add for 6th time | "Love quick-add? Upgrade to Pro for unlimited smart events." |
| Try OCR upload | Taps OCR button | "Scan receipts in one tap. Upgrade to Pro." |
| 7 days after signup | Time-based trigger | Email: "You've been using Dobry Plan for a week — try Pro free for 14 days." |
| Partner joins household | Partner accepts invitation | "Double the people, double the value. Try Pro — free for 14 days." |

---

## 8. Competitive Positioning

### 8.1 Competitive Landscape (Polish Market)

| Competitor | Category | Price | Strengths | Weaknesses vs. Dobry Plan |
|-----------|----------|-------|-----------|---------------------------|
| **Google Calendar** | Calendar only | Free | Ubiquitous, mobile apps | No budget, no shopping, no household focus |
| **Splitwise** | Expense splitting | Freemium ($5/mo Pro) | Strong brand, social debt tracking | No calendar, no shopping list, global-focused |
| **Notion** | General productivity | Freemium ($10+/mo) | Extremely flexible | Complex, not household-optimized, expensive |
| **Coynt** | Budget (PL) | Free/Premium | Polish-focused, budget-specific | No calendar, no shopping list |
| **Listonic** | Shopping list (PL) | Free/Premium | Polish-made, strong shopping features | No calendar, no budget |
| **Todoist/TickTick** | Task management | Freemium | Mature, cross-platform | Not household-focused, no budget |
| **Excel/Google Sheets** | Everything (manual) | Free | Familiar | Manual, no automation, no sync |

### 8.2 Dobry Plan's Unique Selling Proposition (USP)

**"The only app that combines shared calendar, household budget, and shopping list — in one place, for free, open-source, and built for Polish families."**

No single competitor covers all three verticals. Users currently cobble together 2-3 apps (Google Calendar + Splitwise + Listonic). Dobry Plan replaces the stack.

### 8.3 Positioning Statement

> For **couples and families in Poland** who are tired of juggling multiple apps to manage their household, **Dobry Plan** is a **free, open-source household management app** that **combines calendar, budget, and shopping in one place** — unlike Google Calendar, Splitwise, or Listonic which only solve one piece of the puzzle.

---

## 9. Untapped Revenue Opportunities

### 9.1 Near-Term (0-6 months)

| Opportunity | Revenue Potential | Effort | Details |
|-------------|-------------------|--------|---------|
| **14-day Pro trial on signup** | +30-50% conversion | LOW | Auto-enable Pro for 14 days. Let users experience value before asking them to pay. Standard SaaS practice. |
| **Annual plan "2 months free" framing** | +10-15% annual adoption | LOW | Reframe "Save 17%" as "Get 2 months free." More tangible. |
| **Product Hunt launch** | 100-300 signups, press coverage | LOW | Free distribution to early adopters and tech-savvy households. |
| **Google Play Store listing** | Ongoing Android installs | LOW | TWA config already exists. Just publish. |
| **Polish SEO content** | 500-2000 monthly organic visitors in 3-6 months | MEDIUM | 2 blog posts/month targeting household management keywords. |
| **Lifetime deal (LTD)** | 3,000-10,000 PLN one-time burst | MEDIUM | Offer 499 PLN lifetime Pro access on AppSumo or Dealify. Funds development, builds early base. |

### 9.2 Medium-Term (6-12 months)

| Opportunity | Revenue Potential | Effort | Details |
|-------------|-------------------|--------|---------|
| **Referral program** | +15-25% organic growth | MEDIUM | "Invite a friend → both get 1 month Pro free." Household apps are inherently social (partner invites). |
| **White-label / B2B licensing** | 2,000-10,000 PLN/client | HIGH | Coworking spaces, family-focused organizations, HR benefit programs could deploy branded Dobry Plan instances. |
| **API access tier** | 49-99 PLN/mo | MEDIUM | Developer-tier subscription for API access to calendar/budget data. Attracts automation/integration users. |
| **Integration marketplace** | Commission-based | HIGH | Bank transaction import, Smart Home integration, Polish grocery store loyalty card sync. |
| **Household insights / reports** | Feature upsell | LOW | Monthly PDF/email digest: "Your household this month" — summary of events, spending, shopping. Premium-only. |

### 9.3 Long-Term (12+ months)

| Opportunity | Revenue Potential | Effort | Details |
|-------------|-------------------|--------|---------|
| **Native mobile apps** | 2-3x Pro conversion | VERY HIGH | Mobile users convert at higher rates. But defer until product-market fit is validated. |
| **Multi-household support** | New tier at 79-149 PLN/mo | HIGH | Property managers, nannies, elderly care — one person managing multiple households. |
| **B2B team plans** | 49-199 PLN/mo per team | MEDIUM | Shared offices, small companies using calendar + budget for team coordination. |
| **International expansion** | 10x TAM | HIGH | Localize for German, Czech, and other CEE markets. Similar household culture + PLN-adjacent pricing. |
| **Sponsored integrations** | Partnership revenue | MEDIUM | Polish grocery chains (Biedronka, Lidl) pay for featured store sections in shopping list. |

### 9.4 Revenue Opportunity Summary

```
                Revenue Impact
                    ▲
                    │
          HIGH      │  ● Native apps (long-term)
                    │  ● B2B licensing
                    │  ● International expansion
                    │
          MEDIUM    │  ● SEO blog content        ● Lifetime deal
                    │  ● Referral program         ● Pro trial
                    │  ● Google Play listing
                    │
          LOW       │  ● Product Hunt             ● Annual reframing
                    │
                    └──────────────────────────────────────────────►
                    LOW           MEDIUM          HIGH
                                  Effort
```

---

## 10. Risk Assessment

### 10.1 Revenue Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Low conversion rate** (free → paid < 1%) | Medium | HIGH | Implement Pro trial, upgrade prompts, A/B test pricing page |
| **Churn from lack of mobile app** | Medium | Medium | PWA covers 95% of use cases; invest in PWA install prompts |
| **Google Calendar dependency** | Low | HIGH | Core product works without Google; sync is additive |
| **Stripe payment failures** (Polish cards) | Low | Medium | Already handling `invoice.payment_failed` webhook; add dunning emails |
| **Self-hosted cannibalizes SaaS** | Low | Low | AGPL friction is real; most users prefer hosted. Monitor. |

### 10.2 Competitive Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Google adds budget/shopping to Google Calendar** | Very Low | HIGH | Move fast; build community moat; open-source loyalty |
| **Notion launches household template** | Low | Medium | Notion is complex; simplicity is Dobry Plan's advantage |
| **Polish-made competitor emerges** | Medium | Medium | First-mover advantage in this niche; community + open-source lock-in |

### 10.3 Brand Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **"Open source = not serious"** perception | Medium | Medium | Professional landing page, Stripe billing, and consistent brand counter this |
| **Solo founder = bus factor** | HIGH | HIGH | Document all operations; automate deployments; consider co-founder or key contributor |
| **Logo inconsistency** | Happening now | Medium | Finalize logo suite before any marketing push |

---

## 11. Prioritized Action Plan

### Phase 1: Launch Readiness (Week 1-2)

| # | Action | Owner | Blocker? |
|---|--------|-------|----------|
| 1 | **Finalize logo suite** (3 redo + 6 new assets) | Design | YES — blocks all marketing |
| 2 | **Create OG image** (1200x630) for social sharing | Design | Blocks Product Hunt |
| 3 | **Publish Google Play Store listing** with TWA | Dev | TWA config ready |
| 4 | **Add 3 testimonial blocks** to landing page (use early testers) | Copy | Blocks social proof |
| 5 | **Add FAQ section** to pricing page | Copy | Reduces support load |
| 6 | **Clarify "per household" pricing** on pricing page | Copy | Removes conversion friction |

### Phase 2: Conversion Optimization (Week 2-4)

| # | Action | Owner | Blocker? |
|---|--------|-------|----------|
| 7 | **Implement 14-day Pro trial** for all new signups | Dev | #1 conversion lever |
| 8 | **Add in-app upgrade prompts** at free-tier feature gates | Dev | #2 conversion lever |
| 9 | **Add onboarding wizard** (invite → event → budget) | Dev | Improves activation |
| 10 | **Reframe annual plan** to "Get 2 months free" | Copy | Quick win |
| 11 | **Define concrete storage/history limits** per tier | Product | Justifies Family Plus pricing |
| 12 | **Add Polish SEO keywords** to landing page i18n strings | Copy/SEO | Improves organic discovery |

### Phase 3: Distribution (Week 3-6)

| # | Action | Owner | Blocker? |
|---|--------|-------|----------|
| 13 | **Product Hunt launch** | Founder | Needs logo + OG image (Phase 1) |
| 14 | **Create Twitter/X account** (@dobryplan) | Marketing | Start building audience |
| 15 | **Write first 2 SEO blog posts** (Polish) | Content | Targets long-tail keywords |
| 16 | **Set up email drip** (signup → Day 7 sequence) | Dev/Marketing | Improves activation + conversion |
| 17 | **Post in Polish community groups** (Facebook, Wykop, Reddit) | Founder | Authentic maker story |

### Phase 4: Growth (Month 2-3)

| # | Action | Owner | Blocker? |
|---|--------|-------|----------|
| 18 | **Implement referral program** ("invite a friend, get Pro free") | Dev | Viral growth loop |
| 19 | **Create comparison landing pages** (vs Splitwise, vs Google Calendar) | Content/SEO | Bottom-funnel capture |
| 20 | **Record 30-second demo video** | Founder | Boosts landing page conversion |
| 21 | **Consider lifetime deal** (AppSumo, Dealify, or self-hosted) | Business | Early revenue + advocacy |
| 22 | **A/B test headline** ("Your household, finally in sync" vs alternatives) | Dev/Marketing | Data-driven copy optimization |

---

## Appendix A: Key Metrics Dashboard

Track these from Day 1:

| Metric | Tool | Frequency |
|--------|------|-----------|
| Signups (total + daily) | Supabase user count | Daily |
| Active users (DAU/WAU/MAU) | Supabase events/logins | Weekly |
| Free → Pro conversion rate | Stripe | Weekly |
| MRR | Stripe Dashboard | Weekly |
| Churn rate | Stripe (canceled subscriptions / active) | Monthly |
| Landing page → Signup rate | Server logs or Plausible Analytics | Weekly |
| Top traffic sources | Plausible or server logs | Weekly |
| Google Play installs | Play Console | Weekly |
| Blog traffic | Plausible | Monthly |

> **Analytics recommendation:** Use [Plausible Analytics](https://plausible.io) (privacy-first, GDPR-compliant, no cookies). Aligns perfectly with the "no tracking cookies" brand promise. ~$9/mo.

---

## Appendix B: Wording Quick-Reference Card

Use this card for all marketing materials:

| Context | DO write | DON'T write |
|---------|----------|-------------|
| Product name | "Dobry Plan" | "DP", "DobryPlan", "dobry plan" |
| Audience | "your household", "couples and families" | "users", "customers", "consumers" |
| Features | "shared calendar", "budget tracker", "shopping list" | "CRUD operations", "NLP parsing", "event management system" |
| Benefit | "Never double-book again" | "Bidirectional calendar synchronization" |
| Price | "Free forever", "No credit card needed" | "Freemium model", "0 PLN/mo" |
| Trust | "Open source — see every line of code" | "AGPL-3.0 licensed" |
| CTA | "Start for free", "Create your household" | "Sign up", "Register now" |
| Urgency | "Join 100+ households", "Set up in 30 seconds" | "Limited time offer", "Act now" |

---

*This audit was prepared for Dobry Plan executive review. All recommendations are prioritized by expected revenue impact relative to implementation effort. Review quarterly and update as metrics become available.*
