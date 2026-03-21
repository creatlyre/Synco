---
status: complete
phase: 22-historical-year-import
source: [22-01-SUMMARY.md]
started: 2026-03-21T12:00:00Z
updated: 2026-03-21T18:00:00Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: done
name: All tests passed
expected: n/a
awaiting: none

## Tests

### 1. Import page reachable from sidebar
expected: Navigate to any budget page (e.g. /budget/overview). The sidebar shows "📥 Import" link. Clicking it navigates to /budget/import. The page loads with title, year picker (default 2025), and three TSV paste sections.
result: pass

### 2. Income hours TSV paste and preview
expected: On /budget/import, paste tab-separated hours data into the Income Hours textarea (e.g. "1\t160\t144\t120" on separate lines for each month). Click "Preview" — a table appears below showing the parsed months and hour values. Empty cells show as "-".
result: pass

### 3. Save income hours for a past year
expected: With hours data pasted and year picker set to a past year (e.g. 2024), click "Save Hours". A success toast appears showing the count of imported items. Navigate to /budget/overview?year=2024 — the imported hours should be reflected in the monthly income calculations.
result: pass

### 4. One-time expenses TSV import
expected: On /budget/import, paste tab-separated expense data into the One-time Expenses textarea (e.g. "Laptop\t3500\t3" for a 3500 expense in March). Click "Preview" to see parsed table. Click "Save Expenses" — success toast appears. Navigate to /budget/overview for that year — March shows a 3500 one-time expense.
result: pass

### 5. Recurring expenses TSV import
expected: On /budget/import, paste tab-separated recurring data into the Recurring Expenses textarea (e.g. "Rent\t2500"). Click "Preview" to see parsed table. Click "Save Expenses" — success toast appears. Navigate to /budget/overview for that year — recurring expenses show the imported amount each month.
result: pass

### 6. Imported data appears in YoY comparison
expected: After importing data for two different years (e.g. 2024 and 2025), navigate to /budget/overview?year=2025. The Year-over-Year Comparison card should show data for both years with a non-zero delta, confirming imported historical data feeds into the comparison.
result: pass

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0

## Gaps

[none]
