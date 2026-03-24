# Phase 4: Admin Dashboard — Research

**Researched:** 2026-03-24
**Phase:** 04-admin-dashboard-user-management-plan-assignment-admin-privileges-and-statistics

## Domain Analysis

### What This Phase Delivers

An admin dashboard for the CalendarPlanner (Synco) application that allows designated admin users to:
1. View and manage all registered users
2. Assign/change subscription plans for any user
3. View platform-wide statistics (user counts, plan distribution, billing metrics)
4. Grant/revoke admin privileges

### Current State Audit

**User model (`app/database/models.py`):** No `is_admin` field exists. User has: id, email, name, google_id, google tokens, calendar_id, timestamps, last_login.

**Auth dependencies (`app/auth/dependencies.py`):** `get_current_user` extracts user from Supabase JWT or legacy session token. No admin gating exists.

**Billing system (`app/billing/`):** Subscription model with plan (free/pro/family_plus), Stripe integration, BillingRepository with upsert_subscription. BillingEvents track signup/subscribe/cancel/churn/payment_failed.

**Database (`app/database/supabase_store.py`):** Uses Supabase REST API (PostgREST) with service role key. Supports select, insert, update, delete, and count operations.

**Templates:** Jinja2 templates in `app/templates/`, extending `base.html`. Tailwind CSS (prebuilt). Dark glassmorphic theme throughout.

**Existing patterns:**
- Routes: `app/{module}/routes.py` for API, `app/{module}/views.py` for HTML pages
- Services: `app/{module}/service.py` with business logic
- Repositories: `app/{module}/repository.py` for database access
- Dependencies: `app/{module}/dependencies.py` for FastAPI injections

## Technical Approach

### 1. Admin Role Implementation

**Approach:** Add `is_admin` boolean column to `users` table in Supabase.

- Database migration: `ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT false;`
- Update `User` dataclass in `models.py` to include `is_admin: bool = False`
- Update `_to_user()` in `app/users/repository.py` to parse `is_admin`
- Create `get_admin_user` dependency that extends `get_current_user` and checks `is_admin`

**Why boolean over role column:** Only two roles needed (user/admin). A role column would be over-engineering for a household app.

**First admin:** Set via direct Supabase SQL: `UPDATE users SET is_admin = true WHERE email = 'admin@example.com';`

### 2. Admin Dependencies

Create `app/admin/dependencies.py`:
- `get_admin_user`: Depends on `get_current_user`, raises 403 if not admin
- Reuse existing auth flow (Supabase JWT) — no separate admin auth

### 3. Admin Repository

Create `app/admin/repository.py`:
- `list_users(offset, limit)` → paginated user list from `users` table
- `get_user_detail(user_id)` → single user with their subscription
- `update_user_plan(user_id, plan)` → update subscription plan
- `update_user_admin(user_id, is_admin)` → toggle admin status
- `get_platform_stats()` → aggregate counts from users, subscriptions, billing_events
- `count_users()` → total user count

### 4. Admin Service

Create `app/admin/service.py`:
- Business logic layer between routes and repository
- Statistics aggregation (user count by plan, signups over time, active vs canceled)
- User search/filter

### 5. Admin Routes (API)

Create `app/admin/routes.py`:
- `GET /api/admin/users` — paginated user list with search
- `GET /api/admin/users/{user_id}` — user detail with subscription info
- `PATCH /api/admin/users/{user_id}/plan` — change user plan
- `PATCH /api/admin/users/{user_id}/admin` — toggle admin status
- `GET /api/admin/stats` — platform statistics

### 6. Admin Views (HTML)

Create `app/admin/views.py`:
- `GET /admin` — admin dashboard with stats overview
- `GET /admin/users` — user management page with table/search
- `GET /admin/users/{user_id}` — user detail page

### 7. Templates

- `app/templates/admin_dashboard.html` — stats cards, charts
- `app/templates/admin_users.html` — user table with pagination, search
- `app/templates/admin_user_detail.html` — user detail with plan assignment form

### 8. Navigation

- Add admin link to navbar (only visible when `user.is_admin = True`)
- Shield icon or similar admin indicator

## Validation Architecture

### Observable Truths
1. Admin user can access admin dashboard at `/admin`
2. Non-admin user gets 403 when accessing `/admin`
3. Admin can see list of all users with their plans
4. Admin can change a user's subscription plan
5. Admin can grant/revoke admin privileges to other users
6. Admin dashboard shows platform statistics (user count, plan distribution)
7. Admin-only nav link appears for admin users, hidden for regular users

### Key Links
- `get_admin_user` dependency → `get_current_user` → `User.is_admin` check
- Admin routes → AdminService → AdminRepository → SupabaseStore
- Admin views → templates → base.html (navbar admin link conditional)
- Plan assignment route → BillingRepository.upsert_subscription

### Risk Areas
- RLS policies: Admin queries need service role key to read all users (current pattern already uses service role)
- First admin bootstrap: Manual SQL needed — document in plan
- Plan assignment should not bypass Stripe (admin assigns plan in our DB but Stripe isn't updated — document as limitation or sync)

## Standard Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI + Python |
| Database | Supabase (PostgreSQL + PostgREST) |
| Auth | Supabase Auth + JWT cookies |
| Templates | Jinja2 + Tailwind CSS |
| Testing | pytest |
| Patterns | Repository → Service → Route |

## Dependencies

- No new external libraries needed
- Uses existing Supabase, FastAPI, Jinja2 stack
- Depends on Phase 3 (auth pages) being complete for login flow

## Don't Hand-Roll

- Use existing `SupabaseStore` for all DB operations
- Use existing `BillingRepository.upsert_subscription` for plan changes
- Use existing `get_current_user` as base for admin dependency
- Use existing base.html template with dark glassmorphic theme

---

*Research complete: 2026-03-24*
