# Phase 43 Plan 01 Summary

**Status:** Complete
**Commit:** 7144a95

## What was done
- Added comparison table section to landing page — Dobry Plan vs Google Cal+Sheets vs Notion
- Added founder story section with blockquote and personal narrative
- Added GitHub badge/link with SVG icon
- Added ~30 new locale keys in both en.json and pl.json for comparison rows, founder copy, and GitHub CTA
- Table uses semantic HTML (`<table>`, `<th>`, `<thead>`, `<tbody>`, `scope="col"`)

## Files modified
- `app/locales/en.json` — 25+ new keys (compare_*, founder_*, github_*)
- `app/locales/pl.json` — 25+ new keys
- `app/templates/landing.html` — new comparison and founder sections

## Verification
- 581 tests passing, 0 regressions
