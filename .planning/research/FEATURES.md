# Feature Landscape: Shared Household Calendar

**Project:** CalendarPlanner  
**Researched:** March 18, 2026  
**Research Sources:** Cozi (market leader), Google Calendar, Apple Family Sharing, industry patterns  

## Table Stakes

Features users expect in a shared household calendar. Missing any of these = product feels incomplete for household use.

### Event Management

| Feature | Why Expected | Complexity | Dependencies |
|---------|--------------|------------|--------------|
| **Create events** | Core functionality; no calendar without event creation | Low | — |
| **Edit existing events** | Users make mistakes, schedules change | Low | Create events |
| **Delete events** | Remove moved/cancelled events | Low | Create events |
| **One-time events** | Appointments, doctor visits, one-off plans | Low | Create events |
| **Recurring events** | Weekly practices, monthly bills, daily commutes | Medium | Create events; supporting UI for frequency/end date |
| **Event title/name** | Identify what the event is | Low | Create events |
| **Event start/end time** | Know when commitment occurs | Low | Create events |
| **Event description/notes** | Add context: address, confirmation number, attendee notes | Low | Create events |

### Sharing & Collaboration

| Feature | Why Expected | Complexity | Dependencies |
|---------|--------------|------------|--------------|
| **Share calendar with specific person** | Core necessity for household: both partners need access | Medium | User authentication, authorization model |
| **Two user access** | Both household members can view and edit same calendar | Medium | Multi-user session management, conflict resolution |
| **Edit permissions** | Both users can add/modify events (not just read-only) | Medium | Permission system, data consistency |
| **Real-time sync** | Changes show immediately on partner's device | Medium | WebSocket or polling, conflict handling |
| **See who made changes** | "Sarah added dentist appointment" vs mystery update | Low | Event audit trail, user attribution |

### Calendar Views

| Feature | Why Expected | Complexity | Dependencies |
|---------|--------------|------------|--------------|
| **Day view** | See single day's schedule in detail | Low | Event layout, time display |
| **Week view** | Plan weekly at a glance | Medium | Multi-day layout, collision detection |
| **Month view** | Plan monthly, see entire month overview | Medium | Calendar grid layout, event indicators |
| **Upcoming events list** | Check next N days without switching views | Low | Event sorting by date |
| **Today indicator** | Always know what today is | Low | System date, UI highlighting |

### Notifications & Reminders

| Feature | Why Expected | Complexity | Dependencies |
|---------|--------------|------------|--------------|
| **In-app notifications** | Alert when event is added to calendar | Low | Event listener, notification UI |
| **Push notifications** | Reminders on phone even when app closed | Medium | OS notification API (browser/mobile) |
| **Reminder time selection** | "Alert 15 min before", "1 day before", "on day" | Low | UI for time picker |
| **Multiple reminders per event** | "Email yesterday, notify 30 min before" | Medium | Reminder queue, multi-channel support |
| **Email digest** | Daily/weekly summary sent to email (like Cozi) | Medium | Email service integration, scheduler |

### Google Calendar Sync/Export

| Feature | Why Expected | Complexity | Dependencies |
|---------|--------------|------------|--------------|
| **Export to Google Calendar** | Both users read events on phone via Google app | Medium | OAuth2 flow, Google Calendar API |
| **Push event creation** | When event added to CalendarPlanner, appears in Google Calendar | Medium | API write access, sync queue |
| **Calendar selection** | Users choose which Google Calendar receives events | Low | OAuth2 permissions, calendar listing |

### Mobile Access

| Feature | Why Expected | Complexity | Dependencies |
|---------|--------------|------------|--------------|
| **Mobile web view** | Calendar works on phone browser | Low | Responsive design, touch UX |
| **Event view on mobile** | Can see event details from phone | Low | Mobile layout |
| **Create event on mobile** | Add events from phone (quick add via Google Calendar sync) | Low | Mobile form UX |

---

## Differentiators

Features that set CalendarPlanner apart. Not expected, but valuable. Creates competitive moat.

### Natural Language Event Creation

| Feature | Value Proposition | Complexity | Phase Dependency |
|---------|-------------------|------------|------------------|
| **Text request** | "Mom's dentist appointment Tuesday 2pm" → auto-creates event | High | NLP pipeline, entity extraction |
| **Fuzzy date parsing** | "next Friday", "in 2 weeks", "Christmas" understood | High | NLP date parser, calendar math |
| **Participant detection** | "Sarah's soccer game" tags Sarah as attendee | High | NLP + user context |
| **Duration inference** | "Lunch with Sarah" → 1 hour by default | Medium | Domain training data |

**Why valuable:** Competitors require manual form-filling. Text input 10x faster for household use.

### Image/Document OCR for Events

| Feature | Value Proposition | Complexity | Phase Dependency |
|---------|-------------------|------------|------------------|
| **Flyer/poster OCR** | Take photo of event poster → extract date/time/name | High | OCR engine, event extraction model |
| **Screenshot calendar OCR** | Snap photo of another calendar → auto-populate events | High | Layout recognition, scheduling inference |
| **Invitation extraction** | Upload email screenshot → parse event details | High | Email parsing, date/time extraction |

**Why valuable:** Household gets calendar invites in email, texts, flyers — all convertible to shared calendar without manual entry.

### Household-Specific Features

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Color coding by person** | Visual identification of whose event (Sarah=red, Tom=blue) | Low | UI + event model |
| **Quick add shortcuts** | "Sarah practice", "Doctor appointment" with pre-set details | Low | Preset event templates |
| **Event search** | Find "dentist" across all events | Low | Full-text search |
| **Conflict highlighting** | Alert when both users have events at same time | Medium | Overlap detection, collision UI |

### Export Flexibility

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Export to iCal/ICS file** | Download calendar for portability | Low | Standard format support |
| **Export month as PDF** | Print calendar for fridge | Low | PDF generation |
| **Sync to Outlook Calendar** | OneNote integration for users in Microsoft ecosystem | Medium | Outlook API (OAuth) |

---

## Anti-Features

Features to **deliberately NOT build in v1**. Why to skip them.

| Anti-Feature | Why Avoid | Phase to Revisit | What to Build Instead |
|--------------|-----------|------------------|----------------------|
| **Multi-calendar support** (e.g., "Work" + "Personal") | Household calendar is unified by design — separation introduces complexity with no household benefit | v2 | Single shared calendar; color-code by person |
| **Team/multi-family calendars** (3+ users) | Household = 2 people. Multi-family introduces permission complexity, conflict resolution, admin roles. Defer. | v2+ | Stays designed for pairs |
| **Full two-way Google Calendar sync** | Bi-directional sync creates update conflicts, complexity. One-way push (CalendarPlanner → Google) sufficient. | v2 | Push-only with import option |
| **Advanced access controls** (view-only, edit-only roles) | Household: both users have same permissions. Roles add surface area with minimal v1 benefit. | v2 | Simple "shared with you" = full access |
| **Calendar invitations/RSVP system** | Household doesn't RSVP to each other. Adds event-tracking complexity. | Later | Manual RSVP status as event field |
| **Delegated calendar shares** ("Share my calendar with Sarah's mom") | Scope creep. v1 is two people. | v2+ | Start with direct pairs only |
| **Complex permission hierarchies** (owner/editor/viewer) | Household doesn't need permission tiers. Both users = equal editors. | v2+ | Binary: either you have access or you don't |
| **Recurring event customization** (e.g., "every other Tuesday, except holidays") | Advanced rules rare in household use. Simple weekly/monthly/yearly covers ~95%. | v2 | Week/month/year patterns; custom dates as separate events |
| **Timezone support** | Both household members usually in same timezone initially. Add only when needed. | v2 | Assume local timezone; may add later |
| **Integration with homekit/smart home** | Tempting but scope creep: "Turn on lights when Sarah arrives" ≠ calendar problem. | Much later | Calendar only; IoT is separate product |
| **Recurring task lists** (todos differ from events) | Blurs calendar purpose. Cozi's feature bloat. v1 focuses on events. | v2 | Keep event-focused; defer to separate todo app |
| **Meal planning / recipe matching** | Cozi's secondary business. Household calendar ≠ meal planner. | v2+ | Events only; meal planning is separate |
| **Shopping list integration** | Same as above: feature creep. | v2+ | Calendar only |

---

## Feature Dependencies

**Critical path for MVP:**

```
Create Events
  ↓
Sharing (OAuth, two-user model)
  ↓
Calendar Views (Month/Week/Day)
  ↓
Google Calendar Export
  ↓
Notifications/Reminders
```

**Differentiators (parallel to MVP):**
```
Natural Language Input → Requires trained NLP model
Image OCR → Requires vision ML model
Color coding → Requires UI update to event display
```

**Not blocking**, can be added post-MVP:
- Email digests
- Outlook sync
- Conflict highlighting
- Event search
- PDF export

---

## MVP Feature Set (Minimum Viable)

**To ship and validate:**

1. ✓ Create/edit/delete events (one-time + recurring)
2. ✓ Two-user shared calendar  
3. ✓ Month/week view
4. ✓ Real-time sync between users
5. ✓ Push events to Google Calendar
6. ✓ In-app notifications
7. ✓ Mobile-responsive design
8. ✓ User attribution (see who added event)

**Acceptable to defer:**
- Natural language input (post-MVP differentiator)
- Image OCR (post-MVP differentiator)
- Email digest reminders (post-MVP)
- Outlook sync (post-MVP)

---

## Complexity Estimates

| Category | Estimated Effort | Critical Path |
|----------|------------------|----------------|
| Event CRUD | 1-2 weeks | YES |
| Sharing + OAuth setup | 2-3 weeks | YES |
| Calendar views (month/week/day) | 2-3 weeks | YES |
| Notifications | 1-2 weeks | YES |
| Google Calendar sync | 2-3 weeks | YES |
| Real-time sync (WebSocket) | 2 weeks | YES |
| Natural language input | 3-4 weeks | NO (post-MVP) |
| Image OCR | 4-6 weeks | NO (post-MVP) |
| Email digests | 1-2 weeks | NO (post-MVP) |

---

## Confidence Assessment

| Domain | Confidence | Notes |
|--------|------------|-------|
| Table stakes | **HIGH** | Verified across Cozi, Google Calendar, Apple products |
| Differentiators | **MEDIUM** | NLP/OCR are emerging; limited public data on household use cases |
| Anti-features | **MEDIUM-HIGH** | Based on project scope (2-user) + complexity tradeoffs; may revisit post-v1 |
| Complexity estimates | **MEDIUM** | Depends on implementation choices (framework, NLP service) |

---

## Sources

- **Cozi** (cozi.com): Market-leading family calendar; reverse-engineered feature set  
- **Google Calendar**: Public API documentation; feature parity analysis  
- **Apple Calendar / Family Sharing**: Public documentation  
- **Industry patterns**: Common household calendar use cases based on competitor analysis  

**Data sources:**
- Cozi feature overview: https://www.cozi.com/feature-overview/  
- Cozi calendar details: https://www.cozi.com/calendar/  
- Google Calendar creation & sharing: https://support.google.com/calendar/  

