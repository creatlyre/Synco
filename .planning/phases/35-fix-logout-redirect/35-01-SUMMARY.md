---
phase: 35-fix-logout-redirect
plan: 01
status: complete
started: 2026-03-24T16:50:00Z
completed: 2026-03-24T16:56:28Z
commits:
  - hash: 0a3b564
    message: "fix(auth): redirect to login page on POST /auth/logout instead of raw JSON"
---

## What Changed

**Problem:** Clicking the logout button showed raw JSON `{"message":"Wylogowano"}` instead of redirecting to the login page.

**Fix:** Changed `POST /auth/logout` endpoint from returning a JSON dict to returning `RedirectResponse(url="/auth/login", status_code=303)`. The 303 See Other status is the correct code for POST-redirect-GET pattern.

### Files Modified

| File | Change |
|------|--------|
| `app/auth/routes.py` | Logout returns `RedirectResponse(303)` instead of JSON dict |
| `tests/test_auth.py` | Added `test_logout_redirects_to_login` and `test_logout_clears_cookies` |

### Key Decision
Used HTTP 303 (See Other) instead of 302 (Found) because 303 explicitly instructs the browser to follow the redirect with a GET request — the correct semantic for a POST-redirect-GET flow.

## Verification

- `pytest tests/test_auth.py -k test_logout -v` — 2/2 passed
- `pytest tests/test_auth.py -v` — 6/6 passed, zero regressions
