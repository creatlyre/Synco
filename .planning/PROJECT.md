# CalendarPlanner

## What This Is

A shared household calendar web application that lets two people (e.g., partners/spouses) collaboratively manage their schedule from a single source of truth. It supports recurring and one-time events, two-way sync with Google Calendar, natural-language event requests, and image-based event extraction — keeping both users aligned on the family schedule across all devices.

## Core Value

A shared calendar both partners can edit that stays in sync with Google Calendar, so the family schedule is always current everywhere — on the web and on their phones.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Two users can share a single calendar and each add/edit events
- [ ] Events can be recurring (e.g., weekly, monthly) or one-time
- [ ] View upcoming events for the current day and current month
- [ ] Export/sync an entire month to Google Calendar
- [ ] Two-way or push connectivity with Google Workspace Calendar
- [ ] Natural-language request processing to auto-add events to the calendar
- [ ] Image input: extract event date/name from images (e.g., flyers, screenshots) and add to calendar

### Out of Scope

- More than two concurrent users / team calendars — focus on household pair first
- Native mobile app — Google Calendar on phone handles mobile access via sync
- Full two-way Google Calendar sync as v1 — export/push covers the core need

## Context

- Target users: two people in the same household (e.g., couple)
- Platform: Python web application
- Primary integration: Google Calendar / Google Workspace Calendar (OAuth + API)
- Event creation methods: manual UI, natural language text request, image/OCR extraction
- The user wants to see the calendar from a browser and get event reminders on their phone via Google Calendar's notification system

## Constraints

- **Tech stack**: Python — backend must be Python-based
- **Scope**: Two-user household calendar; no multi-tenancy in v1
- **Integration**: Google Calendar API (OAuth2) required for sync/export
- **User count**: Exactly two users per calendar instance for v1

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python backend | User's stated tech preference | — Pending |
| Two-user model (not multi-user) | Simplest model that covers household use case | — Pending |
| Push sync to Google Calendar (not full two-way v1) | Reduces complexity; users read on phone via Google | — Pending |
| Image OCR for event extraction | Nice-to-have but differentiating feature | — Pending |

---
*Last updated: 2026-03-18 after initialization*
