# Phase 48: Version & Consistency Sync - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Sync version numbers and brand strings across README, pyproject.toml, service worker, manifest, and Stripe checkout. Ensure consistency across all files that reference the app version or brand name.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — sync/cleanup phase. Items:
- README.md shows v3.0, pyproject.toml shows 4.0.0, CHANGELOG only goes to 2026-03-19 — update to v5.1
- SW cache `dobryplan-v1` should be `dobryplan-v5.1` to bust old caches
- manifest.json description "Smart household calendar & budget planner" — should match i18n `app.meta_desc`
- Stripe checkout has no `payment_method_types` or `statement_descriptor` — consider adding statement descriptor "DOBRYPLAN" (max 22 chars) or leave for Stripe dashboard
- Add v4.0, v5.0, v5.1 entries to README version history table

</decisions>

<code_context>
## Existing Code Insights

### Version References
- `pyproject.toml` line 3: `version = "4.0.0"` (should be 5.1.0)
- `README.md` line 13: `Version: v3.0 (shipped 2026-03-23)` (outdated)
- `README.md` line 270–276: Version history table (stops at v3.0)
- `sw.js` line 2: `CACHE_NAME = 'dobryplan-v1'` (never updated)
- `manifest.json` line 4: `"description": "Smart household calendar & budget planner"` (hardcoded English)

### Stripe Checkout (app/billing/service.py lines 69-79)
```python
session = stripe.checkout.Session.create(
    mode=mode,
    customer=stripe_customer_id,
    line_items=[{"price": price_id, "quantity": 1}],
    success_url=success_url,
    cancel_url=cancel_url,
    metadata={"user_id": user_id, "plan": plan},
)
```
- No `payment_method_types` (defaults to card — fine)
- No `statement_descriptor` — would show raw Stripe descriptor

### README Version History (lines 270-276)
| Version | Date | Highlights |
| v3.0 | 2026-03-23 | Dashboard, notifications, categories, shopping |
| v2.1 | 2026-03-22 | Event privacy, reminders, multi-year budget |
| v2.0 | 2026-03-20 | Budget tracker |
| v1.1 | 2026-03-20 | Polish localization |
| v1.0 | 2026-03-19 | Calendar CRUD, recurrence, Google sync |

Missing: v4.0 (Monetization), v5.0 (Growth & Conversion), v5.1 (E2E & Brand)

</code_context>

<specifics>
## Specific Ideas

None — sync/cleanup phase.

</specifics>

<deferred>
## Deferred Ideas

None.
</deferred>
