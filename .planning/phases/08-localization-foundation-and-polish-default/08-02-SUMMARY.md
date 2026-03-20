---
phase: 08-localization-foundation-and-polish-default
plan: 02
subsystem: ui
tags: [jinja2, templates, i18n, localization, auth-routes, api-messages]

requires:
  - phase: 08-01
    provides: "i18n contracts (resolve_locale, translate, inject_template_i18n) and locale dictionaries"
provides:
  - "All template copy driven by {{ t('key') }} translation calls"
  - "Localized auth/events/users API response messages"
  - "HTML lang attribute from resolved locale"
affects: [08-03-PLAN, 09, 10]

tech-stack:
  added: []
  patterns:
    - "{{ t('namespace.key') }} Jinja translation pattern across all templates"
    - "translate(key, locale) in Python route handlers for API messages"

key-files:
  created: []
  modified:
    - app/templates/base.html
    - app/templates/calendar.html
    - app/templates/invite.html
    - app/templates/partials/day_events.html
    - app/templates/partials/month_grid.html
    - app/templates/partials/event_entry_modal.html
    - app/templates/partials/event_form.html
    - app/templates/partials/fallback_form.html
    - app/templates/partials/quick_add_modal.html
    - app/auth/routes.py
    - app/events/routes.py
    - app/users/routes.py

key-decisions:
  - "Replace all hardcoded English strings in templates with t() calls"
  - "Localize HTTPException detail messages in auth/events/users routes"
  - "Preserve DOM IDs, CSS classes, and event handlers during migration"

patterns-established:
  - "{{ t('section.key') }} for all user-visible template text"
  - "translate(key, locale) for API error/success messages"

requirements-completed: [I18N-04]

duration: ~30min
completed: 2026-03-19
---

# Phase 08 Plan 02: Template & API Copy Migration to Translation Keys

**Migrated all user-facing template copy and API messages from hardcoded English to i18n translation keys.**

## Accomplishments
- Converted all 9 templates (base, calendar, invite, 6 partials) to use `{{ t('...') }}` translation calls
- Localized auth route messages (login/logout/callback success/error)
- Localized events route validation and error messages
- Localized users route invite/household messages
- Set HTML `lang` attribute from resolved locale in base.html

## Task Commits

1. **Task 1: Convert template and modal copy to translation keys** - `2a4dd7c` (feat)
2. **Task 2: Localize user-facing API messages in auth, events, and users routes** - `2a4dd7c` (feat)

## Files Created/Modified
- `app/templates/base.html` - Title, nav, logout button via t() calls; lang attribute
- `app/templates/calendar.html` - All sidebar labels, sync panel, entry forms localized
- `app/templates/invite.html` - Invite form labels and buttons localized
- `app/templates/partials/*.html` - All 6 partials migrated to translation keys
- `app/auth/routes.py` - Auth success/error messages through translate()
- `app/events/routes.py` - Parse/upload validation messages localized
- `app/users/routes.py` - Invite/household messages localized

## Decisions Made
- Preserved all DOM IDs and CSS classes during migration to avoid UI test breakage
- Used namespaced keys (e.g., `calendar.loading`, `auth.login_success`, `invite.send`)

## Deviations from Plan
None - all templates and routes migrated as planned. Work landed in the same commit as Plan 01.
