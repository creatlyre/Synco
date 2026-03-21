---
phase: 22
slug: historical-year-import
status: approved
shadcn_initialized: false
preset: none
created: 2026-03-21
---

# Phase 22 — UI Design Contract

> Visual and interaction contract for the Historical Year Import page. Verified against existing CalendarPlanner design system.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none (vanilla Tailwind + custom design tokens) |
| Preset | CalendarPlanner glassmorphism system |
| Component library | none (custom glass components) |
| Icon library | inline SVG (stroke-based, 18-24px) |
| Font | Plus Jakarta Sans (display), DM Sans (body), JetBrains Mono (mono/data) |

---

## Spacing Scale

Declared values (project design tokens from `input.css`):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px (--space-xs) | Icon gaps, inline padding |
| sm | 8px (--space-sm) | Compact element spacing, gap between preview rows |
| md | 16px (--space-md) | Default element spacing, card padding |
| lg | 24px (--space-lg) | Section padding, gap between import cards |
| xl | 32px (--space-xl) | Layout gaps |
| 2xl | 48px (--space-2xl) | Major section breaks |

Exceptions: none — follow existing budget page spacing exactly.

---

## Typography

| Role | Size | Weight | Line Height | Font |
|------|------|--------|-------------|------|
| Page title | 1.75rem (text-page-title) | 700 | 1.2 | Plus Jakarta Sans |
| Section title | 1.125rem (text-section-title) | 600 | 1.3 | Plus Jakarta Sans |
| Card title | 0.9375rem (text-card-title) | 600 | 1.4 | Plus Jakarta Sans |
| Body | 0.875rem (text-body / text-sm) | 400 | 1.6 | DM Sans |
| Caption/description | 0.75rem (text-caption / text-xs) | 400 | 1.5 | DM Sans |
| Textarea content | 0.875rem | 400 | 1.5 | JetBrains Mono (font-mono) |
| Preview table data | 0.75rem | 400 | 1.5 | JetBrains Mono (font-mono) |

---

## Color

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | Body gradient (#0f0c29 → #1e1553 → #0d1b4b) | Page background |
| Secondary (30%) | Glass panels (rgba(255,255,255,0.07)) | Cards, sidebar, textareas |
| Accent (10%) | Indigo gradient (--color-primary → purple) | Save buttons, active sidebar item |
| Success | --color-success (#22c55e) | Success toast after import |
| Danger | --color-danger (#ef4444) | Error toast on failure |
| Warning | --color-warning (#f59e0b) | Validation warnings in preview |

Accent reserved for: Save Hours/Expenses buttons, active sidebar nav-active indicator, year picker hover state.

---

## Page Layout

### Structure

```
┌─────────────────────────────────────────────────────────┐
│ [Nav bar - existing base.html]                          │
├──────────┬──────────────────────────────────────────────┤
│ Sidebar  │  Main content                                │
│ glass    │                                              │
│ rounded  │  ┌─ Year Picker ─────────────────────────┐  │
│ -2xl p-4 │  │  ← 2024 →                             │  │
│          │  └────────────────────────────────────────┘  │
│ Settings │                                              │
│ Income   │  ┌─ Income Hours Card ────────────────────┐  │
│ Expenses │  │  Title + description                    │  │
│ Overview │  │  ┌─────────────────────────────────┐   │  │
│ ■Import  │  │  │ textarea (mono, 200px min-h)    │   │  │
│ ← Back   │  │  └─────────────────────────────────┘   │  │
│          │  │  [Preview] [Save Hours]                 │  │
│          │  │  ┌─ Preview table (if shown) ───────┐  │  │
│          │  │  │ Month | R1 | R2 | R3              │  │  │
│          │  │  │ 1     | 96 | 144| 0               │  │  │
│          │  │  └──────────────────────────────────┘  │  │
│          │  └────────────────────────────────────────┘  │
│          │                                              │
│          │  ┌─ One-time Expenses Card ───────────────┐  │
│          │  │  [Same pattern as above]                │  │
│          │  └────────────────────────────────────────┘  │
│          │                                              │
│          │  ┌─ Recurring Expenses Card ──────────────┐  │
│          │  │  [Same pattern as above]                │  │
│          │  └────────────────────────────────────────┘  │
├──────────┴──────────────────────────────────────────────┤
```

### Sidebar

Identical to existing budget pages. 5 links:
- Settings → `/budget/settings`
- Income → `/budget/income`
- Expenses → `/budget/expenses`
- Overview → `/budget/overview`
- **Import** → `/budget/import` (active state: `nav-active`)
- ← Back → `/` (glass-btn-secondary, mt-4 on lg)

Active item: `nav-active` class (not `<a>`, uses `<div>` with `aria-current="page"`).
Inactive items: `hover:bg-white/5 transition-colors`.
All items: `px-4 py-3 text-sm font-medium rounded-xl min-h-[44px] flex items-center`.

### Year Picker

Reuse exact pattern from `budget_overview.html`:
```html
<div class="flex items-center justify-center gap-4 mb-6">
  <button id="year-prev" class="glass-btn-secondary rounded-xl px-4 py-2.5 text-sm font-medium min-h-[44px] min-w-[44px]">←</button>
  <span id="year-display" class="text-xl font-bold"></span>
  <button id="year-next" class="glass-btn-secondary rounded-xl px-4 py-2.5 text-sm font-medium min-h-[44px] min-w-[44px]">→</button>
</div>
```

Default year: `new Date().getFullYear() - 1` (most imports are for the previous year).
Year range: 2020 to current year (no future years — this is historical import).

---

## Import Cards

Three identical-structure glass cards stacked vertically with `gap-6` (--space-lg).

### Card Structure

```html
<div class="glass rounded-2xl p-6">
  <!-- Title -->
  <h3 class="text-section-title mb-2">{card title}</h3>
  <!-- Description -->
  <p class="text-xs opacity-60 mb-4">{format description}</p>
  
  <!-- Textarea -->
  <textarea class="glass-input font-mono text-sm rounded-xl w-full min-h-[200px] mb-4"
            placeholder="{example data}" spellcheck="false"></textarea>
  
  <!-- Action buttons -->
  <div class="flex gap-3 mb-4">
    <button class="glass-btn-secondary rounded-xl px-4 py-2.5 text-sm font-medium min-h-[44px]">
      {Preview btn text}
    </button>
    <button class="glass-btn-primary rounded-xl px-4 py-2.5 text-sm font-medium min-h-[44px]">
      {Save btn text}
    </button>
  </div>
  
  <!-- Preview table (hidden by default) -->
  <div id="{preview-id}" class="hidden">
    <div class="table-responsive">
      <table class="w-full text-xs font-mono">
        <thead>
          <tr class="text-xs opacity-70 border-b border-white/10">
            <th>...</th>
          </tr>
        </thead>
        <tbody id="{tbody-id}"></tbody>
      </table>
    </div>
  </div>
  
  <!-- Status message -->
  <div id="{status-id}" class="hidden rounded-xl px-4 py-3 text-sm font-medium" role="status"></div>
</div>
```

### Card 1: Income Hours

| Element | Spec |
|---------|------|
| Title | `{{ t('budget.import_hours_title') }}` |
| Description | `{{ t('budget.import_hours_desc') }}` |
| Textarea placeholder | `1\t0\t0\t0\n2\t0\t0\t0\n...\n12\t160\t144\t124` (tab-literal in placeholder) |
| Preview columns | Month, Rate 1 Hours, Rate 2 Hours, Rate 3 Hours |
| Preview cell styling | Numbers right-aligned (`text-right`), null/empty shown as `—` in opacity-40 |
| Save button | `{{ t('budget.import_save_hours') }}` |

### Card 2: One-time Expenses

| Element | Spec |
|---------|------|
| Title | `{{ t('budget.import_onetime_title') }}` |
| Description | `{{ t('budget.import_onetime_desc') }}` |
| Textarea placeholder | `Laptop\t3500\t3\nVacation\t2000\t7` |
| Preview columns | Name, Amount, Month |
| Preview cell styling | Amount right-aligned, formatted with 2 decimals + currency |
| Save button | `{{ t('budget.import_save_expenses') }}` |

### Card 3: Recurring Expenses

| Element | Spec |
|---------|------|
| Title | `{{ t('budget.import_recurring_title') }}` |
| Description | `{{ t('budget.import_recurring_desc') }}` |
| Textarea placeholder | `Rent\t2500\nInternet\t100` |
| Preview columns | Name, Amount |
| Preview cell styling | Amount right-aligned, formatted with 2 decimals + currency |
| Save button | `{{ t('budget.import_save_expenses') }}` |

---

## Textarea Styling

```css
/* Uses existing glass-input from design system + overrides */
textarea.glass-input {
  font-family: var(--font-mono);  /* JetBrains Mono */
  font-size: 0.875rem;
  line-height: 1.5;
  min-height: 200px;
  resize: vertical;
  white-space: pre;               /* preserve tab formatting */
  overflow-x: auto;               /* horizontal scroll for wide data */
}
```

Textarea inherits `glass-input` class: dark mode `rgba(255,255,255,0.07)` bg, light mode `rgba(255,255,255,0.88)` bg. Focus ring: `rgba(139,92,246,0.65)` border + `rgba(139,92,246,0.18)` glow.

Placeholder text: `opacity-35` (dark), `opacity-40` (light) — monospace, showing exact TSV format.

---

## Preview Table

| Property | Value |
|----------|-------|
| Font | JetBrains Mono, 0.75rem |
| Header | `text-xs opacity-70 border-b border-white/10 py-2 px-2` |
| Cell padding | `py-1.5 px-2` |
| Numeric cells | `text-right` |
| Null/empty values | `—` displayed in `opacity-40` |
| Row hover | none (data preview, not interactive) |
| Max rows | show all rows (max 12 for hours, variable for expenses) |
| Validation errors | Row with invalid data: `bg-red-500/10` background, `text-red-400` text |

---

## Interaction States

### Buttons

| State | Primary (Save) | Secondary (Preview) |
|-------|-----------------|---------------------|
| Default | `glass-btn-primary` gradient | `glass-btn-secondary` |
| Hover | `filter: brightness(1.15)` | `bg-white/5` underlay |
| Active | `transform: scale(0.98)` | `transform: scale(0.98)` |
| Disabled | `opacity-50 cursor-not-allowed` | `opacity-50 cursor-not-allowed` |
| Loading | Text replaced with "..." + `animate-pulse` | N/A |

Save button is disabled until Preview has been clicked and data is valid.

### Toast / Status Messages

Reuse existing pattern from budget_income.html / budget_expenses.html:

```javascript
function showToast(msg, isError = false) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = isError
    ? 'rounded-xl px-4 py-3 mb-4 text-sm font-medium toast-error'
    : 'rounded-xl px-4 py-3 mb-4 text-sm font-medium toast-success';
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 4000);
}
```

Success toast: green background (`toast-success`), shows count: "Successfully imported 12 items".
Error toast: red background (`toast-error`), shows error message.

Toast placement: top of main content area (same as income/expenses pages).

---

## Copywriting Contract

| Element | EN Copy | PL Copy |
|---------|---------|---------|
| Page title | "Import Historical Data" | "Import danych historycznych" |
| Hours section title | "Income Hours" | "Godziny pracy" |
| Hours description | "Paste TSV: Month \| Rate 1 Hours \| Rate 2 Hours \| Rate 3 Hours" | "Wklej TSV: Miesiąc \| Godziny stawka 1 \| Godziny stawka 2 \| Godziny stawka 3" |
| One-time title | "One-time Expenses" | "Wydatki jednorazowe" |
| One-time description | "Paste TSV: Name \| Amount \| Month" | "Wklej TSV: Nazwa \| Kwota \| Miesiąc" |
| Recurring title | "Recurring Monthly Expenses" | "Wydatki stałe miesięczne" |
| Recurring description | "Paste TSV: Name \| Amount" | "Wklej TSV: Nazwa \| Kwota" |
| Preview button | "Preview" | "Podgląd" |
| Save hours button | "Save Hours" | "Zapisz godziny" |
| Save expenses button | "Save Expenses" | "Zapisz wydatki" |
| Success message | "Successfully imported {count} items" | "Pomyślnie zaimportowano {count} pozycji" |
| Error message | "Import failed" | "Import nie powiódł się" |
| No data message | "No data to import. Paste data into the textarea first." | "Brak danych do importu. Najpierw wklej dane w pole tekstowe." |
| View overview link | "View in Overview →" | "Zobacz w Przeglądzie →" |

---

## Empty States

| Scenario | Behavior |
|----------|----------|
| No data pasted, Preview clicked | Textarea border flashes red briefly (`border-red-400` for 1s via CSS transition), show toast: "No data to import" |
| No data pasted, Save clicked | Same as above — Save requires Preview first anyway |
| Invalid TSV format | Preview table shows with invalid rows highlighted in `bg-red-500/10`, Save button remains disabled |
| All rows valid | Preview table shown, Save button becomes enabled |

---

## Responsive Behavior

| Breakpoint | Layout Change |
|------------|---------------|
| < lg (mobile) | Sidebar becomes horizontal scroll row at top. Cards stack vertically, full width. Year picker centered. |
| >= lg (desktop) | Sidebar fixed-width (w-48) left column. Cards in right column. Year picker above cards. |

Textareas: always `w-full`. On mobile, horizontal scroll for wide TSV content via `overflow-x: auto` on the textarea.

---

## Accessibility

| Element | Requirement |
|---------|-------------|
| Textarea labels | Each textarea has a visible `<label>` or `aria-label` |
| Preview tables | `role="table"` implicit, `<th scope="col">` on headers |
| Toast messages | `role="status"` + `aria-live="polite"` |
| Buttons | All min-h-[44px] touch targets |
| Year picker buttons | `aria-label="Previous year"` / `aria-label="Next year"` |
| Focus order | Year picker → Hours textarea → Hours buttons → One-time textarea → One-time buttons → Recurring textarea → Recurring buttons |
| Color contrast | All text meets WCAG 2.1 AA (existing design system compliant) |

---

## Light Mode

All glass/input/button components already support light mode via `html.light-mode` class in `input.css`. No additional light mode overrides needed for this page — the existing design tokens handle:
- Glass panels: `rgba(255,255,255,0.82)` bg with indigo border
- Inputs: `rgba(255,255,255,0.88)` bg with indigo border
- Buttons: solid indigo gradient
- Text: `#1e3a8a` body text

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS — All strings defined EN+PL, CTAs verb+noun, empty states with solution path
- [x] Dimension 2 Visuals: PASS — Layout wireframe, card structure, interaction states, preview table spec
- [x] Dimension 3 Color: PASS — 60/30/10 from existing design system, accent limited to save buttons
- [x] Dimension 4 Typography: PASS — All roles mapped with exact values, mono for data entry/display
- [x] Dimension 5 Spacing: PASS — Uses existing --space-* tokens, gap/padding values specified
- [x] Dimension 6 Registry Safety: PASS — No third-party components, all existing glass system

**Approval:** approved 2026-03-21
