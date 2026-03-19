---
phase: 09-language-switcher-persistence-and-translation-coverage
plan: 02
type: execute
wave: 2
executed: true
status: complete
completed_at: "2026-03-19T14:30:00Z"
tasks_completed: 3
files_modified:
  - tests/test_calendar_views.py
  - tests/conftest.py
  - app/i18n.py
commits:
  - hash: "830d979"
    message: "feat(09-02): add locale reset fixture and integration tests for language switching"
key-files:
  created:
    - tests/conftest.py (fixture: locale_reset_client, helpers: get_page_in_locale, assert_locale_rendered)
    - tests/test_calendar_views.py (5 new locale integration tests)
  modified:
    - app/i18n.py (fixed set_locale_cookie_if_param httponly/samesite parameter names)
test-results:
  total: 117
  passed: 117
  failed: 0
  skipped: 0
  new_tests: 5
  regression: "None—all prior tests still pass"
---

## Wave 2: Integration Tests Complete

**Plan 09-02:** Language Switcher Integration and Bilingual Rendering Tests

### Objective

Write comprehensive integration tests to verify language switcher behavior, locale persistence, and bilingual rendering across critical user paths.

### Task Summary

**Task 1:** Added locale reset fixture and test helpers
- Created `locale_reset_client` fixture to clear locale cookie between tests
- Created `get_page_in_locale(client, path, locale)` helper for fetching in specific language
- Created `assert_locale_rendered(html, expected_locale)` helper to verify locale in HTML output
- Status: **Complete**

**Task 2:** Wrote 5 integration tests for locale behavior
1. `test_default_locale_is_polish`: Verifies first-time users see Polish UI by default
2. `test_switch_locale_from_polish_to_english`: Confirms UI updates when switching to English
3. `test_locale_cookie_persists_across_reload`: Validates locale cookie persists across page refresh
4. `test_english_locale_consistent_across_pages`: Ensures English renders consistently on / and /invite
5. `test_query_param_overrides_cookie`: Confirms ?lang=xx query param always overrides persisted locale
- Status: **Complete** — All 5 tests passing

**Task 3:** Full regression test suite
- Ran tests on test_calendar_views.py, test_auth.py, test_events_api.py, test_users.py
- Result: **69 tests passed, 0 regressions**
- Full suite (all tests): **117 tests passed, 0 new failures**
- Status: **Complete**

### What Was Built

**Locale Integration Layer:**
- Test fixture `locale_reset_client` for locale state isolation
- Test helpers for common locale scenarios (fetch in locale, assert locale rendered)
- 5 focused integration tests covering default locale, switching, persistence, and consistency

**Bug Fixes:**
- Fixed Starlette cookie parameter names: `httpOnly` → `httponly`, `sameSite` → `samesite`

### Verification

All integration tests verify key behaviors:
- Default Polish rendering (Phase 9 requirement I18N-02)
- Language switching and UI updates (Phase 9 requirement I18N-03)
- Persistence across sessions via httpOnly cookie (Phase 9 requirement I18N-03)
- Bilingual coverage on main routes (/ and /invite)
- Query param override for testing and sharing

### Success Criteria Met

✅ **Default Polish:** `test_default_locale_is_polish` — Polish copy present in calendar.html  
✅ **Switching:** `test_switch_locale_from_polish_to_english` — English copy rendered after ?lang=en  
✅ **Persistence:** `test_locale_cookie_persists_across_reload` — Cookie retained across reload  
✅ **Multi-page:** `test_english_locale_consistent_across_pages` — English on / and /invite  
✅ **Query override:** `test_query_param_overrides_cookie` — ?lang=xx sets new cookie  
✅ **Regression:** 117 tests passed, all prior functionality intact  

### Test Coverage Details

**Locale Tests:**
```
tests/test_calendar_views.py::test_default_locale_is_polish PASSED
tests/test_calendar_views.py::test_switch_locale_from_polish_to_english PASSED
tests/test_calendar_views.py::test_locale_cookie_persists_across_reload PASSED
tests/test_calendar_views.py::test_english_locale_consistent_across_pages PASSED
tests/test_calendar_views.py::test_query_param_overrides_cookie PASSED

Prior tests still passing (112 tests total)
```

**Regression Coverage:**
- Calendar views: 41 tests (locale + prior)
- Auth flows: 8 tests
- Events CRUD: 12 tests
- User/invite: 8 tests
- All other tests: 48 tests
- **Total: 117 tests, 0 failures**

### Known Issues / Deferred

None. Phase 9-02 is complete with all tests passing and no regressions.

### Next Steps

Phase 10: Verify parser works with Polish language after localization.

---

**Commit:** 830d979  
**Completion Time:** ~15 minutes (Wave 2 execution)  
**Test Status:** ✅ 117/117 passing
