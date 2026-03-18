# Domain Pitfalls: Shared Household Calendar Web App

**Domain:** Shared household calendar (Python/Google Calendar)
**Researched:** March 18, 2026
**Confidence Level:** MEDIUM (mix of official docs, common patterns, and known issues)

---

## Critical Pitfalls

### Pitfall 1: Refresh Token Exhaustion

**What goes wrong:**
Your app requests a new refresh token for each user session or authorization, silently discarding old tokens. After ~50-100 authorizations, Google hits its per-user-per-OAuth-client limit (100 refresh tokens max), and begins invalidating older tokens. Users start seeing "invalid_grant" errors unpredictably.

Moreover, if a refresh token hasn't been used for 6 months, Google *automatically* revokes it. Combined with token rotation patterns, this causes surprise auth failures in production.

**Why it happens:**
- Developers assume unlimited refresh tokens (OAuth spec is vague)
- Testing is localized; token expiration isn't visible in early phases
- No monitoring on token state; failure detected only when users complain
- Misunderstanding of "Testing" vs. "Production" consent screen (Testing mode tokens expire in 7 days)

**Consequences:**
- Users get auth errors and can't access the app
- App crashes if no fallback exists when refresh fails
- Requires forcing users through re-authentication, disrupting household workflow

**Prevention:**
- **Store one refresh token per user permanently** in secure database (encrypted field)
- **Reuse the same refresh token** for all API calls; never request a new one unless explicitly revoked
- Implement **token refresh error handling:** if refresh fails, flag user for re-authentication but don't throw
- Monitor/alert on `invalid_grant` errors (sign of token expiration)
- Use **"Production" consent screen** (not "Testing") from day one—changes token lifetime from 7 days to indefinite
- Implement **graceful degradation:** if Google auth fails, show calendar read-only or queue edits for later sync

**Detection (warning signs):**
- Users reporting "Please log in again" errors after weeks of normal use
- Logs showing 401 Unauthorized → 400 invalid_grant in cascades
- Higher auth failure rates as user population grows

**Phase mapping:**
- **Phase 2-3 (Core OAuth/Sync):** Implement secure token storage and refresh error handling
- **Phase 8+ (Monitoring):** Add token health alerts and rotation strategy

---

### Pitfall 2: Recurrence Rule Timezone & DST Disasters

**What goes wrong:**
You store a recurring event in User A's timezone (EST). When User B views from PST or User B checks the calendar after DST flip, the event times shift unexpectedly. Worse: modifying a single instance of a recurring event can cause duplicates or deletions if your logic doesn't account for timezone-adjusted recurrences.

Example: Weekly Tuesday at 9am EST. DST ends (EST → EDT jump). Google Calendar's recurrence engine recalculates; your local cache shows it at 8am instead of showing no change at all. If you try to sync this back, you create a spurious "changed" event.

**Why it happens:**
- RRULE (RFC 5545 recurrence rules) assume UTC, but most user calendars are timezone-bound
- Timezone database (tzdata) changes yearly; library versions may be stale
- Editing "this and following" occurrences requires recalculating the entire series
- Google Calendar API sometimes returns times in different formats (floating vs. fixed timezone)

**Consequences:**
- Events show at wrong times for different users
- Daylight saving transitions cause "phantom" events or shifted times
- Modifying one instance breaks subsequent instances or creates duplicates
- Sync loops where the same event gets pushed back-and-forth between app and Google Calendar

**Prevention:**
- **Always store times in UTC internally.** Render to users in their local timezone only at UI layer
- **Use a mature RRULE library** (e.g., `dateutil` in Python or `rrule.js`)—don't implement recurrence yourself
- **Test with DST boundaries explicitly:** e.g., Nov 5, 2025 (fall back), Mar 9, 2025 (spring forward)
- **Never edit a single occurrence of a recurring event** in v1; disallow it or refactor to use Google's VEVENT model (exception instances)
- **Sync strategy:** Always fetch the full series from Google when syncing, don't assume local copies are current
- **Timezone canon:** Store user's home timezone in DB (not inferred from browser); use it consistently for all recurrence math
- **Document the rule:** When showing "Repeats weekly on Tuesday," explicitly state timezone (e.g., "EST") if it's user-specific

**Detection (warning signs):**
- Users reporting times off by 1 hour around DST transitions
- Recurring events appearing twice (both old and new calculation)
- App logs showing RRULE parse errors or "UTC offset mismatch"

**Phase mapping:**
- **Phase 3 (Recurring Events):** Use dateutil or proven library; hard test DST boundaries
- **Phase 5 (Sync):** Fetch full series on each sync; prefer read-only recurring in v1

---

### Pitfall 3: Concurrent Edit Conflicts & Lost Updates

**What goes wrong:**
User A changes an event description in the webapp (9:01 am). User B edits the same event on their phone (9:02 am). Whichever sync runs second wins; the other's change is silently lost. No merge, no warning.

Worse: A adds "Bring passport" to a trip event. B changes the time. Your app syncs A's description to Google, then B's time—but Google sees it as edits to the same event and may apply both (correct by accident) or only one (silent conflict).

**Why it happens:**
- Two-user household model implies single calendar, but updates can arrive out-of-order
- Last-write-wins (LWW) is simple but loses data
- No concept of "version" or "edited_at" to detect conflicts
- Google Calendar API doesn't support ETags or conditional updates in v1

**Consequences:**
- Users lose edits without realizing it
- Inconsistency between app and Google Calendar
- Trust erosion ("Why did my change disappear?")
- Silent data loss is worse than failed request

**Prevention:**
- **Implement optimistic locking with edit timestamps:**
  - Store `last_edited_at` and `last_editor_user_id` with each event
  - When User A tries to save, check if `last_edited_at` hasn't changed since they loaded it
  - If changed, show conflict dialog: "B edited this while you were typing. Compare versions?" (not auto-merge)
- **Queue-based sync for v1:** Don't allow simultaneous edits to the same event
  - Lock event for editing by one user at a time (add UI indicator "B is editing this")
  - Serialize writes: if A saves, B's pending save fails with "event changed" and reloads
- **Separate conflicts for recurring events:** If A edits the series and B edits one instance, treat as non-conflicting
- **Log all conflicts:** Track where conflicts occur; use as input to future undo/history feature
- **Scope creep:** Avoid full collaborative editing in v1 (like Google Docs). Household calendar doesn't need simultaneous collaborative typing.

**Detection (warning signs):**
- Users report missing edits or changes
- Discrepancy between app event and Google Calendar event (same event_id, different fields)
- Database logs showing multiple saves to same event in < 1 second

**Phase mapping:**
- **Phase 2 (Core DB):** Add `last_edited_at`, `last_editor_user_id`
- **Phase 4 (Sync):** Implement conflict detection; lock editing during sync
- **Phase 7+ (UX):** Show "X is editing" indicator and conflict dialogs

---

### Pitfall 4: OCR Accuracy and Fallback Failure

**What goes wrong:**
User uploads a flyer image with an event: "Annual Company Picnic—June 15 at Central Park." OCR reads it as "Annual Campany Picinc—June 15 at Central Bark" (misread 'o'→'a', 'P'→'B'). Event title is now wrong. Worse: OCR completely fails on low-contrast text, but the app doesn't degrade gracefully—it either crashes or creates blank events.

Even working OCR confidence is unreliable: scanned text often has 75-85% confidence, leading to random character substitutions that break event parsing.

**Why it happens:**
- OCR tools (Tesseract, cloud APIs) aren't 100% accurate, especially on real-world images
- No fallback: app either shows OCR result or fails silently
- Confidence scores aren't displayed to users for validation
- Relying on OCR for dates is risky (date parsing is separate error source)

**Consequences:**
- Malformed events added to calendar (wrong title, date, or location)
- Users don't notice until they check the calendar later
- If auto-synced to Google Calendar, bad events are hard to find and delete
- Trust erodes: "I took a photo, why is the event wrong?"

**Prevention:**
- **Human-in-the-loop for v1:** Never auto-add OCR results directly
  - OCR extracts text; user reviews and edits before confirmation
  - Show OCR confidence per field; highlight low-confidence extractions in yellow/red
  - Example: "Title (92% confident): [text field]" with "Title seems unclear, re-read this part?" hint
- **Fallback extraction:** If OCR fails entirely, show raw image + text input form ("I can't read this image. Please type the event details")
- **Structured OCR:** Use form-based extraction (ask "Date?" "Title?" "Location?") instead of free-form text
- **Validate before sync:** Before pushing to Google Calendar, validate:
  - Date is in future (or user's intended range)
  - Title is not empty and > 2 characters
  - Location is optional but if present, not obviously garbage (e.g., "Bark" unlikely for park)
- **Confidence threshold:** Set minimum OCR confidence (e.g., 80%); below threshold, require manual review
- **Async processing:** Offload OCR to background job with user notification ("Processed your image, please review")

**Detection (warning signs):**
- Low OCR confidence reported in logs (< 75%)
- Users editing events immediately after OCR creation
- Events with obviously wrong titles/dates from OCR source

**Phase mapping:**
- **Phase 6 (Image Upload):** Implement OCR + human review flow (block auto-add)
- **Phase 8 (Refinement):** Improve OCR selection (better library) and add confidence scoring UI

---

### Pitfall 5: NLP Date Parsing Edge Cases

**What goes wrong:**
User types "next Tuesday" expecting an event a week from now. Your NLP parser interprets "next Tuesday" as tomorrow (if today is Monday) or 8 days away depending on the NLP library's definition. User types "March 15" without a year; parser assumes current year, but it's December, so the event is created for March 15, 1970 (or the far past).

Relative dates ("in 3 days," "next month") are especially brittle. Recurring patterns ("every other Thursday") are parsed incorrectly if the NLP library doesn't support open-ended recurrence.

**Why it happens:**
- NLP libraries (e.g., `dateutil.parser`, NLTK, commercial APIs) have different heuristics
- Ambiguous input: "March 15" could mean this year or next; "next Tuesday" varies by library definition
- User context isn't captured: "next Tuesday" means different things on Monday vs Thursday
- Timezone handling in NLP is rare; no library knows your user's timezone implicitly

**Consequences:**
- Events created with wrong dates, silently (user doesn't notice until calendar view)
- Recurring events with wrong frequency or end date
- User frustration: "I said 'next Tuesday' and it created it for next year!"

**Prevention:**
- **Limit NLP scope in v1:** Accept only explicit formats initially
  - Supported: "March 15, 2026," "15-Mar-2026," "Mar 15, 2026"
  - Supported: User selects "in X days" from dropdown (not free text)
  - Supported: "Repeats weekly on Tuesday" (Google Calendar UI pattern, not free text)
- **Relative date validation:** If NLP is used, validate relative dates against user's timezone + current date
  - "next Tuesday" → parse with dateutil, then validate it's > today
  - If ambiguous, ask user: "Did you mean March 15, 2026 or 2027?" (show future date highlighted)
- **Timezone context:** Pass user's timezone to NLP parser (dateutil supports this)
- **No year inferred:** If user says "March 15", always ask "This year or next?" before creating
- **Recurring recurrence validation:** Don't parse "every other Thursday" unless fully supported; show a form instead
  - Form: "Repeats: Weekly | Bi-weekly | Monthly | Yearly" + "On: [day selection]" + "Until: [date picker]"
- **Test suite:** Create explicit test cases:
  - "next Tuesday" on Monday (should be 1 day away, not 8)
  - "March 15" in December (should be next year, not this)
  - "in 3 weeks" (should be 21 days from now)

**Detection (warning signs):**
- Events created with dates far in past or future unexpectedly
- Users immediately editing event dates after NLP creation
- NLP parser errors in logs (parsing failures, ambiguous input)

**Phase mapping:**
- **Phase 4 (NLP Event Creation):** Use form-based inputs, not free-text NLP; validate before sync
- **Phase 8+ (Advanced):** Add optional NLP with user confirmation step

---

## Moderate Pitfalls

### Pitfall 6: Google Calendar API Quota Exhaustion

**What goes wrong:**
Your app makes one API call per user action (edit event, view month, sync). With 2 users, each opening the app multiple times per day, you hit Google Calendar API quota limits faster than expected. Free tier limits are ~1M requests/day for the entire project. You're throttled, users see slow sync.

Worse: No queue management, so sync requests pile up and timeout.

**Why it happens:**
- Apps don't batch API calls (e.g., get all events in one call instead of N calls)
- No caching: every page view queries Google Calendar (wasteful)
- Overly aggressive sync: app syncs on every event edit + periodic background sync + manual user sync
- Free tier quotas are per-project, not per-user; small mistake scales badly

**Consequences:**
- "Quota exceeded" errors; users see blank calendar or sync failures
- Unpredictable performance (throttled to 1-2 requests/sec after hitting limit)
- Requires backoff/retry logic that users don't understand

**Prevention:**
- **Batch API calls:** Fetch all events for a date range in one call, not one call per event
- **Local cache with TTL:** Store recent calendar state in DB; expire after 15-30 min
  - Only sync if user explicitly clicked "Refresh" or TTL expired
  - Full monthly sync once per day (background job, not on every page load)
- **Incremental sync:** Use Google Calendar's `syncToken` to fetch only changed events since last sync, not the whole calendar
- **Smart retry:** Implement exponential backoff (1s, 2s, 4s, 8s) when quota exhausted; don't retry immediately
- **Quota monitoring:** Track API calls per day; alert if approaching limit (e.g., 80% of 1M)
- **v1 constraint:** Sync to Google once per day (batch), not per edit
  - Accept eventual consistency: events sync in the next batch, not immediately

**Detection (warning signs):**
- Google API error logs showing `rateLimitExceeded` or `quotaExceeded`
- Calendar appears blank or stale (syncing stopped)
- App response times spike to seconds (quota throttled)

**Phase mapping:**
- **Phase 3 (Google Sync):** Implement caching + incremental sync + syncToken
- **Phase 5 (Daily Batch):** Background job for nightly Google Calendar export
- **Phase 9 (Monitoring):** Alert on quota approaching

---

### Pitfall 7: One-Way Sync Hidden Complexity

**What goes wrong:**
You plan "push events from app → Google Calendar only" (not two-way in v1). But users also edit events directly in Google Calendar on their phones, and expect those to show in the web app. Your app doesn't pull from Google, so the web app is stale. Users see old data and get confused.

Alternatively, your "one-way" sync design doesn't account for deletions: User deletes an event in Google Calendar on their phone, but the web app still shows it. Sync now becomes "broken" and either deletes from app or recreates a ghost event from app into Google.

**Why it happens:**
- "One-way" is stated as v1 design, but the real world is two-way (users expect both directions)
- "Push only" ignores the fact that users will edit on Google Calendar phone app
- Deletion handling is non-obvious: does "one-way" mean app→Google, but also remove from app if deleted in Google?

**Consequences:**
- Users see stale data in web app (events deleted on phone still show on web)
- Sync becomes "one-way" in design but actually two-way in practice, leading to complex edge cases
- Requires designing deletion sync separate from creation/update sync

**Prevention:**
- **Clearly define scope:** 
  - v1: "Users manage events in the web app only; phone users view via Google Calendar"
  - If two-way wanted: plan as separate phase
- **Read-only phone access:** Document that events should NOT be edited on phone; edits will be lost
- **Enforce at app layer:** Disable user edits on Google Calendar directly; all edits go through web app
  - Impractical for household use, so pick simpler scope
- **Deletion strategy:** Decide:
  - Option A: One-way deletion (app→Google only; user can't delete from phone)
  - Option B: Accept two-way deletion (hard to implement correctly)
  - v1 recommendation: Option A (or disable deletions in phone until v2)
- **Status quo:** Accept that v1 is "app-primary" and phone is "view-only via Google Calendar read-only"

**Detection (warning signs):**
- Users reporting deleted events reappearing
- Users editing on phone, changes missing from web app
- Sync conflicts between app and Google Calendar

**Phase mapping:**
- **Phase 2 (Requirements Fidelity):** Clarify scope; document that phone edits aren't synced back
- **Phase 5 (Sync):** Implement one-way only; clearly explain in UI/docs
- **Phase future (Two-way):** Plan as separate phase with explicit conflict resolution

---

### Pitfall 8: Over-Engineering v1 (Scope Creep)

**What goes wrong:**
You plan to build "full two-way sync with Google Calendar" in v1. You design for multi-tenant setups (in case you resell later). You build a complex event merging engine to handle conflicts. You plan to support shared calendars (not just two-person). By the time you're halfway through Phase 2, you've written 10K lines of code and still don't have a working calendar to show users.

Real outcome: Project stalls, users never see anything, features get cut at the last moment.

**Why it happens:**
- "Wouldn't it be nice if..." features sound easy before implementation
- Designer over-generalizes (one app for any household size, not just 2 users)
- No clear definition of "minimum," just "v1 should support..."

**Consequences:**
- Project takes 4x longer than estimated
- Code complexity makes testing harder
- Bugs are harder to isolate
- User feedback delayed indefinitely

**Prevention:**
- **Define MVP rigorously:** Two users, single calendar, manual + image + NLP input, export to Google (no import), recurring basic support
- **Explicitly defer hard problems to v2:**
  - Full two-way sync (v2)
  - Shared calendars with > 2 users (v2)
  - Conflict merging (v2, if needed)
  - Advanced recurrence (v2)
  - Undo/history (v2)
- **Ship earliest possible incomplete feature:** Get a working calendar UI and one event creation path (manual) in front of users by end of Phase 3
- **Layer, don't generalize:** Build for 2-user household, not parameterized for N users
- **Ruthless cutting:** If a feature isn't on MVP list, it ships in v2 (same day decision rule)

**Detection (warning signs):**
- Design documents describe 10+ features for v1
- Technical discussions about "flexibility" and "future-proofing"
- Phases scheduled beyond 6-8 weeks
- Debate over feature prioritization (sign of unclear MVP scope)

**Phase mapping:**
- **Phase 1 (Requirements):** Lock "two users only, manual input + Google export"
- **Phase 2-6 (Core):** Stick to locked scope; defer all "nice-to-haves" to v2 explicitly
- **Phase 7+ (Polish):** Do not add major features

---

## Minor / Domain-Specific Pitfalls

### Pitfall 9: Testing Calendar Apps is Deceptively Hard

**What goes wrong:**
You test with today's date (March 18, 2026). Tests pass. Then a month later, you realize your "show upcoming events for this month" view was only correct for March; it's broken in April because you hardcoded month logic. You never tested DST transitions, timezone changes, or leap year edge cases.

**Why it happens:**
- Date/time logic appears simple until you test edge cases
- Tests often run in current year and month; edge cases aren't covered
- CI/CD doesn't vary the system date, so timezone/DST tests are missed
- "Just check if event date > today" seems right but fails on month boundaries

**Prevention:**
- **Parametrize tests by date:** Run the same tests on:
  - March 18 (current)
  - March 1 (start of month)
  - March 31 (end of month)
  - Feb 29 (leap year)
  - Nov 5, 2025 (DST end)
  - Mar 9, 2025 (DST start)
  - Dec 31 → Jan 1 (year boundary)
- **Mock system date in tests:** Don't rely on actual date; set test clock explicitly
- **Test recurring events near boundaries:**
  - Event: "Every Tuesday at 2pm EST", run from Oct 1 to Nov 15 (crosses DST)
  - Assert times are correct post-DST
- **Test edge case months:** Feb (28-29 days), months with 30 vs 31 days

**Detection (warning signs):**
- Bug reports arriving monthly or seasonally (DST/month boundary related)
- "It worked in March but broke in April"
- Recurrence-related bugs clustered around DST transitions

**Phase mapping:**
- **Phase 3 (Recurring):** Write parametrized date tests with DST/month boundaries
- **Ongoing:** Add one boundary test for each bug fix

---

### Pitfall 10: Forgetting Timezone in Every UI Display

**What goes wrong:**
Event created "Sept 15 at 2pm". No timezone shown. User A from EST thinks it's 2pm eastern. User B from PST thinks it's 2pm pacific. They show up at events an hour apart.

**Why it happens:**
- Developers store times in UTC but forget to store/display timezone
- UI displays "2:00 PM" without timezone context
- Multi-user household with same timezone assumption breaks when one user travels

**Prevention:**
- **Store timezone with event:** Event record includes `timezone` field (e.g., "US/Eastern")
- **Display always with timezone:** UI shows "2:00 PM EST" or "2:00 PM (your time)" 
- **Allow per-event timezone:** Some events are "9am Pacific" (for call with west coast friend), others "9am Eastern" (local time)

**Detection (warning signs):**
- Users confused about event times, especially after travel or DST
- "What time is this event for me?" in support requests

**Phase mapping:**
- **Phase 3 (Core Events):** Include timezone in event model and UI display

---

## Phase-Specific Warning Matrix

| Phase Topic | Likely Pitfall | Primary Mitigation |
|---|---|---|
| OAuth Setup (Phase 2) | Refresh token exhaustion | Store one token per user, reuse it, use Production consent screen |
| Core DB Schema (Phase 2) | Concurrent edit conflicts | Add `last_edited_at`, `last_editor_user_id` |
| Google Calendar Sync (Phase 3) | Quota exhaustion | Cache + batch API calls + syncToken for incremental sync |
| Recurring Events (Phase 3) | Timezone & DST disasters | Store times in UTC, use dateutil, test DST boundaries |
| NLP Event Creation (Phase 4) | Date parsing edge cases | Use form inputs, not free-text NLP; validate before creating |
| Image Upload (Phase 6) | OCR accuracy failures | Human review before adding; show confidence scores |
| Sync Strategy (Phase 5) | One-way sync hidden complexity | Clearly define scope (app-primary, phone read-only) |
| Architecture (Phase 1) | Over-engineering v1 | Lock scope to 2 users, manual + image + NLP, export only, defer multi-user |
| Testing (Phases 3-7) | Calendar logic edge cases | Parametrize tests with DST, month boundaries, leap years |
| UI Display (Phases 3-5) | Timezone ambiguity | Always display timezone with times |

---

## Key Sources

- **Google OAuth 2.0 docs:** Refresh token limits, expiration, error handling (official)
- **RFC 5545 (iCalendar spec):** RRULE timezone and DST handling (authoritative)
- **dateutil Python library:** Proven recurrence rule + timezone support
- **Google Calendar API sync patterns:** Batch vs. incremental, syncToken strategy (official docs)
- **Common pitfalls from Slack/Stack Overflow discussions:** OCR accuracy, NLP date parsing edge cases, two-user sync (community)

---

*Last updated: March 18, 2026*
