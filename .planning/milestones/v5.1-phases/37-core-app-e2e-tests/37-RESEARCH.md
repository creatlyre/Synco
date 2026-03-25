# Phase 37: Core App E2E Tests — Research

**Researched:** 2026-03-25
**Level:** 1 (Quick Verification — building on Phase 36 infrastructure, known Playwright patterns)

## Standard Stack

- **Playwright** (`@playwright/test`) — Already installed in Phase 36 as devDependency
- **Setup projects** — Auth storage states created by Phase 36's `auth.setup.ts`
- **HTMX + Jinja2** — Server-rendered pages with HTMX partial swaps; tests must wait for HTMX content load

## Architecture Patterns

### HTMX Content Loading Strategy

This app renders server-side HTML via Jinja2 and loads dynamic content via HTMX `hx-get` + `hx-trigger="load"`. Key implication for E2E tests:

- Calendar page: `#month-grid` loads via `hx-get="/calendar/month?year=...&month=..."` on page load
- Calendar page: `#day-events` loads via `hx-get="/calendar/day?year=...&month=...&day=..."` on page load
- Notification badge: loads via `hx-get="/notifications/badge"` with `hx-trigger="load"`
- Notification dropdown: loads via `hx-get="/notifications/dropdown"` on bell click

**Wait strategy:** Use Playwright's `locator.waitFor()` or `expect(locator).toBeVisible()` after page.goto — Playwright auto-waits for elements. For HTMX-loaded content, wait for the content to appear inside the container rather than just the container div.

```typescript
// Good: Wait for HTMX content to load inside #month-grid
await page.goto('/calendar');
await expect(page.locator('#month-grid .day-cell').first()).toBeVisible();

// Bad: Only checks the empty container div exists
await expect(page.locator('#month-grid')).toBeVisible();
```

### Test File Organization (Phase 36 infrastructure)

Files go in `e2e/tests/` directory, matching Phase 36's config:
```
e2e/tests/
├── test_auth.spec.ts        # Auth flow tests
├── test_calendar.spec.ts    # Calendar view tests
├── test_dashboard.spec.ts   # Dashboard tests
├── test_notifications.spec.ts  # Notification UI tests
```

Each Playwright project (`free`, `pro`, `family-plus`) runs ALL files in `e2e/tests/`. Tests that need a specific account should use `test.skip()` or be placed in a describe block that checks the project name.

### Selector Strategy

Prefer in order:
1. **IDs** — `#month-grid`, `#notification-bell`, `#email`, `#password`, `#loginForm`
2. **Role-based** — `page.getByRole('heading', { name: '...' })`
3. **Text content** — `page.getByText('...')` for Polish UI text
4. **CSS classes** — `.btn-primary`, `.day-cell` as fallback

The app uses Polish as default locale — UI text assertions should use Polish strings or be locale-agnostic (check element existence, not text content).

### Route Map for Tests

| Test Area | Routes | Method |
|-----------|--------|--------|
| Login page | `GET /auth/login` | Renders login form |
| Login submit | `POST /auth/password-login` | JSON `{email, password}` → sets cookies, redirects to `/` |
| Register page | `GET /auth/register` | Renders register form |
| Dashboard | `GET /dashboard` | Home page (also `/` redirects here) |
| Calendar | `GET /calendar` | Calendar page with month grid |
| Calendar month grid | `GET /calendar/month` | HTMX partial for month days |
| Calendar day events | `GET /calendar/day` | HTMX partial for day's events |
| Notification badge | `GET /notifications/badge` | HTMX partial with unread count |
| Notification dropdown | `GET /notifications/dropdown` | HTMX partial with notification list |

### HTML Selectors From Templates

**Login (`login.html`):**
- Form: `#loginForm`
- Email input: `#email` (type="email")
- Password input: `#password` (type="password")
- Submit button: `.btn-primary`
- Error display: `#error` (div with class `error-msg`)

**Register (`register.html`):**
- Form: `#registerForm`
- Email input: `#email` (type="email")
- Password input: `#password` (type="password")
- Name input likely present (check actual template)

**Calendar (`calendar.html`):**
- Month grid container: `#month-grid` (HTMX loads content)
- Day events container: `#day-events` (HTMX loads content)
- Event entry button: `#event-entry-open-btn`
- Event entry modal: included from `partials/event_entry_modal.html`

**Dashboard (`dashboard.html`):**
- Today's events section: text `t('dashboard.today_events')`
- Quick event section: text `t('dashboard.quick_event')`
- Full event link: `a[href="/calendar?open=event-entry"]`
- Budget snapshot section present in template

**Navbar (`base.html`):**
- Notification bell container: `#notification-bell-container`
- Notification bell button: `#notification-bell`
- Dropdown loaded into: `#notification-bell-container` area via HTMX

## Don't Hand-Roll

- **Custom wait utilities** — Use Playwright's built-in auto-wait; `expect(locator).toBeVisible()` already retries
- **Session management** — Phase 36's storage state handles auth; just use the project config
- **HTMX interception** — Don't wait for HTMX-specific events; wait for the resulting DOM content instead

## Common Pitfalls

1. **HTMX content not loaded yet** — Calendar month grid loads async via HTMX after page load. Must wait for content inside `#month-grid`, not just the container div.
2. **Polish locale text** — UI text is in Polish by default. Use element selectors (IDs, CSS) over text content where possible. When text is needed, use the actual Polish strings.
3. **Login redirect timing** — Login form uses `fetch()` then `window.location.href = '/'`. The redirect is JavaScript-driven, not a form action redirect. Use `page.waitForURL('**/dashboard**')` or wait for not being on `/auth/login`.
4. **Notification dropdown is HTMX-loaded** — Bell click triggers `hx-get="/notifications/dropdown"` which swaps HTML into the dropdown area. Must wait for the dropdown content to appear after click.
5. **No dedicated /notifications page** — Notifications are a dropdown only (no full page). The feed is the dropdown panel in the navbar, not a separate route.
6. **Event entry modal** — Opening `#event-entry-open-btn` shows a modal. Tests should verify it opens but NOT submit (read-only tests).
7. **Dashboard URL** — Dashboard is at `/dashboard` (router prefix). The root `/` likely redirects or serves something else. Verify actual redirect behavior.

## Validation Architecture

### Observable Truths
1. Login with valid credentials lands on dashboard; invalid credentials show visible error
2. Register page renders form with email and password fields
3. Calendar month view renders grid with day cells and navigation
4. Dashboard loads with today's events section and budget snapshot
5. Notification bell is visible and dropdown loads on click

### Key Links
- `e2e/tests/test_auth.spec.ts` → `/auth/login` page → `#loginForm` → `/auth/password-login` API → redirect to dashboard
- `e2e/tests/test_calendar.spec.ts` → `/calendar` page → `#month-grid` (HTMX load) → day cells, `#event-entry-open-btn` → modal
- `e2e/tests/test_dashboard.spec.ts` → `/dashboard` page → today's events section, budget section, quick-add
- `e2e/tests/test_notifications.spec.ts` → `base.html` navbar → `#notification-bell` → `/notifications/dropdown` HTMX load

### Test-to-Requirement Mapping
| Requirement | Test File | What It Verifies |
|-------------|-----------|-----------------|
| AUTH-E2E-01 | test_auth.spec.ts | Valid login → dashboard redirect |
| AUTH-E2E-02 | test_auth.spec.ts | Invalid login → error message visible |
| AUTH-E2E-03 | test_auth.spec.ts | Register page renders form fields |
| AUTH-E2E-04 | test_auth.spec.ts | Logout clears session |
| CAL-E2E-01 | test_calendar.spec.ts | Month grid renders with day cells |
| CAL-E2E-02 | test_calendar.spec.ts | Navigation arrows change month |
| CAL-E2E-03 | test_calendar.spec.ts | Day click opens event entry modal |
| DASH-E2E-01 | test_dashboard.spec.ts | Dashboard loads as home page |
| DASH-E2E-02 | test_dashboard.spec.ts | Today's events section visible |
| DASH-E2E-03 | test_dashboard.spec.ts | Budget snapshot and quick-add visible |
| NOTF-E2E-01 | test_notifications.spec.ts | Bell icon visible in navbar |
| NOTF-E2E-02 | test_notifications.spec.ts | Bell click loads dropdown content |
