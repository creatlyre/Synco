# Quick Task: Expense Categorization Coverage — Research

**Researched:** 2026-03-27
**Domain:** Multilingual keyword matching (PL + EN) for expense auto-categorization
**Confidence:** HIGH

## Summary

The current `category_keywords.json` contains ~850 keywords across 20 preset categories. Coverage is excellent for most categories (Groceries, Home, Health, Entertainment, Transport, Garden) but critically thin for **Loan** (3 keywords), and notably thin for **Travel** (~25) and **Rent** (~25). Several categories also miss common generic expense terms that Polish households would frequently type.

The substring matching algorithm (`norm_kw in w` and `w in norm_kw` for `len(w)>=3`) creates **false-positive risks from short keywords** (e.g., `"tea"` matches `"theater"`, `"gaz"` matches `"magazyn"`) and **first-match-wins ordering issues** (e.g., `"szampon"` matches Pets before Personal Care due to reverse-substring on multi-word Pets keyword `"szampon dla psow"`).

**Primary recommendation:** Add ~120 missing keywords across thin categories, fix ordering/collision issues, then validate with 1,000 generated test expenses targeting ≥93% hit rate.

## User Constraints (from CONTEXT.md)

### Locked Decisions
- PL and EN only
- 10 lists × 100 items = 1,000 total test expense names
- Target ≥93% categorization rate
- Output: JSON file for tracking categorization results (one-time validation artifact)
- Gaps below 93% trigger keyword additions to `category_keywords.json`

### Specifics
- 20 preset categories, keyword map in `category_keywords.json`
- Matching: case-insensitive substring with diacritic normalization
- First-match-wins ordering
- "Other" category = empty keywords (fallback)

## Keyword Gap Analysis by Category

### CRITICAL — Needs Major Additions

| Category | Current Count | Gap Assessment |
|----------|:------------:|----------------|
| **Loan** | 3 | Only PL: `pozyczka`, `pozyczki`, `splata pozyczki`. Zero EN keywords. Missing: `rata`, `raty`, `splata`, `dlug`, `chwilowka`, `windykacja`, `komornik`, `refinansowanie`, `loan`, `installment`, `repayment`, `debt`, `financing`, `credit payment`, `monthly payment`, `interest` |
| **Travel** | ~25 | Missing airlines: `ryanair`, `wizzair`, `wizz air`, `easyjet`, `lot`. Missing generic: `wycieczka`, `kemping`, `camping`, `namiot`, `przewodnik`, `turystyka`, `kurorz`, `all inclusive`, `kolonia`, `kolonie`, `oboz`, `wczasy`, `agroturystyka`. Missing EN: `cruise`, `excursion`, `resort`, `tour`, `souvenir`, `itinerary` |
| **Rent** | ~25 | Missing PL housing-specific: `fundusz remontowy`, `podatek od nieruchomosci`, `oplata za mieszkanie`, `zarzadca`, `administrator budynku`, `wspolnota mieszkaniowa`, `przelew za mieszkanie`. Missing EN: `mortgage payment` (conflict with Savings), `property tax`, `homeowners`, `HOA`, `maintenance fee` |

### MODERATE — Needs 5-15 Additions

| Category | Current Count | Missing Common Terms |
|----------|:------------:|---------------------|
| **Personal Care** | ~55 | `manicure`, `pedicure`, `paznokcie`, `depilacja`, `wax`, `spa`, `masaz`, `massage`, `salon`, `nail polish`, `makeup`, `skincare` |
| **Health** | ~70 | Pharmacy chains: `gemini`, `doz`, `dbam o zdrowie`, `apteka melissa`. Generic: `stomatologia`, `protetyka`, `korona`, `implant`, `orteza`, `kule` |
| **Children** | ~65 | Generic: `dziecko`, `butelka`, `smoczek`, `fotelik samochodowy`, `mleko modyfikowane`, `formula`, `baby formula`, `child`, `kids`, `toddler`. Stores: `kiddystory`, `51015`, `coccodrillo` |
| **Education** | ~45 | `szkola jezykowa`, `kurs online`, `lekcje muzyki`, `lekcje plywania`, `korepetytor`, `e-learning`, `online course`, `tutorial`. Platforms: `chatgpt`, `github copilot` (dev tools?) |
| **Clothing** | ~65 | Stores: `deichmann`, `ccc`, `halfprice`, `tkmaxx`, `tk maxx`, `nike`, `adidas`, `new balance`, `puma`, `zalando`, `about you`, `modivo` |
| **Electronics** | ~50 | `smartfon`, `smartphone`, `telefon` (ordering risk vs Utilities), `telewizor`, `tv`, `television`, `apple`, `samsung`, `xiaomi`, `huawei` |
| **Savings & Finance** | ~50 | `inwestycja`, `investment`, `fundusz`, `fund`, `lokata`, `deposit`, `obligacje`, `bonds`, `akcje`, `stocks`, `prowizja`, `commission`, `broker`, `makler`, `dywidenda`, `dividend` |

### GOOD — Minor Gaps Only

| Category | Current Count | Notes |
|----------|:------------:|-------|
| **Groceries** | ~110 | Very thorough. Could add: `piekarnia`, `bakery`, `masarnia`, `butcher`, `delikatesy`, `warzywniak`, `owocowy`, `bio`, `eko`, `organic` |
| **Transport** | ~65 | Good. Could add: `e-toll`, `viatoll`, `jakdojade`, `koleo`, `e-podroznik`, `car sharing`, `panek`, `traficar` |
| **Utilities** | ~55 | Good. Could add: `swiatłowod`, `fiber`, `5g`, `lte`, `telewizja`, `tv` (risk: Entertainment), `smieci gmina` |
| **Entertainment** | ~70 | Thorough. Could add: `spotify family`, `escape room` (already there!), `laser tag`, `paintball`, `karaoke`, `bilard`, `dart` |
| **Home** | ~90 | Excellent. Could add: `remont`, `renovation`, `malowanie`, `tapeta`, `wallpaper` |
| **Garden** | ~55 | Excellent coverage |
| **Pets** | ~30 | Could add: `royal canin`, `purina`, `brit`, `whiskas`, `pedigree`, `akwarium`, `aquarium`, `terrarium` |
| **Events** | ~40 | Could add: `zaproszenie`, `invitation`, `dekoracje`, `decoration`, `balony`, `balloon` |
| **Shopping** | ~22 | Store-only by design. Could add: `zakupy online`, `zamowienie`, `paczka`, `przesylka`, `kurier`, `inpost`, `paczkomat`, `dhl`, `dpd`, `ups` |

## Matching Algorithm Observations

### How It Works

```python
norm = _normalize(name)       # lowercase, strip diacritics (ł→l, NFKD)
words = norm.split()          # split expense name into words
for cat_name, keywords in CATEGORY_KEYWORDS.items():   # iterate categories in JSON order
    for norm_kw in keywords:                            # iterate pre-normalized keywords
        for w in words:
            if norm_kw in w:                            # keyword is substring of word
                return match
            if len(w) >= 3 and w in norm_kw:            # word is substring of keyword
                return match
```

### Gotcha 1: Short Keywords → False Positives

| Keyword | Category | Would Falsely Match |
|---------|----------|---------------------|
| `"tea"` | Groceries | `"theater"`, `"steak"` (both contain "tea" substring) |
| `"gaz"` | Utilities | `"magazyn"`, `"gazetka"` |
| `"bus"` | Transport | `"business"`, `"abus"` |
| `"ham"` | Groceries | `"shampoo"` — actually no ("ham" not in "shampoo"), safe |
| `"rice"` | Groceries | `"price"` |
| `"ice cream"` | Groceries | Safe (multi-word, tested per-word) |
| `"oil"` | Groceries | `"toilet"`, `"foil"`, `"boiler"` |

**Mitigation for test data:** Avoid using these short-keyword collisions as "uncategorizable" items — they'll match unexpectedly. Instead, note them as expected false positives.

### Gotcha 2: Reverse-Substring Steals

When `len(w) >= 3 and w in norm_kw`: a single word from the expense can match inside a multi-word keyword. This means:

| Expense | Word | Matched Keyword | Category (wrong) | Expected Category |
|---------|------|-----------------|-------------------|-------------------|
| `"szampon"` | `szampon` | `"szampon dla psow"` (Pets) | Pets | Personal Care |
| `"szczepienie"` | `szczepienie` | `"szczepienie psa"` (Pets) | Pets | Health |
| `"krem"` | `krem` | `"krem natalia"` (Personal Care) | Personal Care | OK (correct) |

**Fix:** Move single-word variants (`"szampon"`, `"szczepienie"`) to the correct category as standalone keywords so they match first via exact substring. Or reorder categories so Health/Personal Care precede Pets.

### Gotcha 3: Ordering Determines Priority

JSON object key order in Python 3.7+ is insertion order. Current order:
1. Pets → 2. Loan → 3. Garden → 4. Electronics → 5. Children → 6. Personal Care → 7. Clothing → 8. Events → 9. Savings & Finance → 10. Travel → 11. Groceries → 12. Rent → 13. Utilities → 14. Transport → 15. Health → 16. Education → 17. Entertainment → 18. Home → 19. Shopping → 20. Other

**Key conflict: Groceries (#11) before Entertainment (#17)**
- `"tea"` in Groceries catches `"theater"` before Entertainment sees `"theater"`.
- `"coffee"` in Groceries catches `"coffee shop"` before Entertainment's `"cafe"` — but this is arguably correct.

**Key conflict: Pets (#1) before Personal Care (#6) / Health (#15)**
- Multi-word Pets keywords steal single-word matches via reverse-substring (see Gotcha 2).

**Recommendation:** Either:
1. Add explicit single-word keywords to the correct category (they'll match via `norm_kw in w` before the reverse match fires), OR
2. Add min-length guards for short keywords that cause false positives

Option 1 is simpler and requires only keyword additions, no code changes.

## Common Polish Expense Vocabulary (Missing)

### Food & Daily
- `obiad` (lunch/dinner), `sniadanie` (breakfast), `kolacja` (supper)
- `paczka` (package — but could be Shopping/delivery)
- `woda` (already in Utilities — conflict if someone means bottled water!)
- `napoje` (drinks), `alkohol` (alcohol), `wino` (already: `wina`)

### Bills & Subscriptions
- `faktura` (invoice), `rachunek` (bill — already in Utilities), `oplata` (fee)
- `subskrypcja` (already in Entertainment), `prenumerata` (already in Education)

### Transport
- `bilet miesięczny` → `bilet miesieczny` (monthly pass)
- `mandat` (traffic ticket), `holowanie` (towing), `laweta` (tow truck)

### Health
- `recepta` (already present), `wizyta kontrolna` (checkup), `zabieg dentystyczny`
- Common drug names: `apap`, `ibuprom`, `paracetamol`, `nurofen`, `rutinoscorbin`

### Children
- `szkolna wplata` (school payment), `wycieczka szkolna` (school trip)
- `babyshower`, `baby shower`, `wyprawka` (layette)

## Common English Expense Vocabulary (Missing)

### Generic terms by category
- **Groceries:** `deli`, `bakery`, `butcher`, `produce`, `pantry`
- **Health:** `copay`, `deductible`, `lab test`, `blood work`, `checkup`
- **Transport:** `gas station`, `car insurance`, `AAA`, `roadside assistance`
- **Rent:** `property tax`, `HOA`, `maintenance`, `strata fee`
- **Loan:** `loan`, `installment`, `repayment`, `debt`, `financing`, `APR`
- **Travel:** `cruise`, `resort`, `tour`, `souvenir`, `Airbnb` (already present lowercase)
- **Savings:** `investment`, `stocks`, `bonds`, `401k`, `IRA`, `brokerage`

## Test Data Generation Strategy

### Category Distribution (per 100-item list)
Target: proportional to real household spending frequency.

| Category | Items per list | Rationale |
|----------|:-----------:|-----------|
| Groceries | 20 | Most frequent expense type |
| Home | 10 | Cleaning, repairs, furniture |
| Utilities | 8 | Monthly bills |
| Transport | 8 | Fuel, tickets, parking |
| Health | 6 | Pharmacy, doctor visits |
| Entertainment | 6 | Dining, streaming, cinema |
| Children | 5 | Toys, kindergarten, clothes |
| Clothing | 5 | Seasonal purchases |
| Personal Care | 4 | Hygiene, cosmetics |
| Education | 3 | Courses, books |
| Savings & Finance | 3 | Insurance, tax |
| Events | 3 | Gifts, celebrations |
| Pets | 2 | Food, vet |
| Garden | 2 | Seasonal |
| Electronics | 2 | Gadgets |
| Rent | 2 | Fixed monthly |
| Loan | 1 | Fixed monthly |
| Travel | 1 | Occasional |
| Shopping | 2 | Online orders (store names) |
| **Uncategorizable** | **7** | To test the ~7% miss target |
| **Total** | **100** | |

### Item Name Patterns

Each test item should follow realistic patterns:
1. **Store name only:** `"Biedronka"`, `"Rossmann"`, `"Allegro"`
2. **Generic description:** `"obiad"`, `"taxi do pracy"`, `"lunch"`
3. **Store + item:** `"Lidl zakupy"`, `"Apteka leki"`
4. **Brand/product name:** `"Netflix"`, `"Spotify"`, `"PKP bilet"`
5. **Informal/short:** `"mleko"`, `"chleb"`, `"paliwo"`
6. **Compound:** `"zakupy spozywcze biedronka"`, `"wizyta u dentysty"`

### Language Mix
- ~60% PL names (primary user language)
- ~30% EN names (subscriptions, brands, generic)
- ~10% mixed/brand-only (universal: `"Uber"`, `"Netflix"`, `"IKEA"`)

### Uncategorizable Items (~7 per list)
These should be genuinely ambiguous or niche expenses:
- `"prowizja bankowa"` (unless added to Savings)
- `"napiwek"` / `"tip"` (no category)
- `"darowizna"` / `"donation"` (no category)
- `"mandat"` / `"fine"` (no category unless added to Transport)
- `"kara umowna"` (contractual penalty)
- `"przelew"` / `"transfer"` (too generic)
- `"zwrot"` / `"refund"` (too generic)
- `"inne"` / `"miscellaneous"`
- `"skladka"` (could be insurance or club membership)
- `"tandeta"` (junk — no match)
- Person names: `"dla Marka"`, `"Ola"` (no match)

### Implementation Approach
1. Write a Python script that:
   - Generates 10 lists of 100 expense names from curated pools per category
   - Randomizes order within each list
   - Runs each name through `_normalize()` + `_detect_category()` logic
   - Logs: expense_name → detected_category → expected_category → match (✓/✗)
   - Computes per-list and aggregate hit rate
2. Output: JSON with all 1,000 results + summary stats
3. If hit rate < 93%: add keywords to fix gaps, re-run

## Known Collision Pairs to Watch

| Collision | Category A → Keyword | Category B → Keyword | Resolution |
|-----------|---------------------|---------------------|------------|
| `"szampon"` | Pets → `"szampon dla psow"` | Personal Care → `"szampon"` | Add standalone `"szampon"` to Personal Care, ensure Personal Care has `norm_kw in w` match before Pets reverse match fires. **Actually won't work** — Pets comes first. Must reorder or add `"szampon"` to Pets check exclusion. Simplest: remove `"szampon dla psow"` from Pets, keep `"karma psy"`, `"karma kot"` style keywords. |
| `"tea"` → `"theater"` | Groceries → `"tea"` | Entertainment → `"theater"` | Not a structural issue — `"theater"` should have its own full keyword in Entertainment. Entertainment already has `"theater"` keyword, but Groceries matches first via `"tea"` substring. **Fix:** Won't happen for `"teatr"` (Polish). Only EN edge case. |
| `"gaz"` → `"magazyn"` | Utilities → `"gaz"` | Any category with `"magazyn"` | Edge case — `"magazyn"` is unlikely as expense name. Acceptable risk. |
| `"woda"` | Utilities → `"woda"` | Groceries (bottled water) | `"woda mineralna"` or `"woda butelkowana"` would match Utilities. Consider adding `"woda mineralna"` to Groceries (before Utilities in order). But Groceries is currently AFTER Utilities in order. **Structural limitation.** |

## Recommendations for Planner

1. **Add ~120 keywords** to thin categories (Loan: +15, Travel: +15, Rent: +10, others: +5-10 each)
2. **Fix "szampon" collision:** Remove multi-word `"szampon dla..."` from Pets (keep `"karma psy"`, `"karma kot"` etc.) — or add `"szampon"` as explicit keyword to Personal Care AND ensure it matches via `norm_kw in w` before Pets reverse-match. Since Pets comes first, the only fix is to NOT have `"szampon"` matchable in Pets.
3. **Generate test data** in a Python script using the distribution table above
4. **Run categorization** using the exact same `_normalize()` + matching logic
5. **Iterate** on keyword additions until ≥93% hit rate achieved
6. **Do NOT change algorithm** — keyword additions only (per task scope)

## Sources

- **PRIMARY (HIGH):** Direct analysis of `app/budget/category_keywords.json` (current file)
- **PRIMARY (HIGH):** Direct analysis of `app/budget/expense_service.py` (`_detect_category`, `_normalize`)
- **PRIMARY (HIGH):** Direct analysis of `app/budget/expense_repository.py` (`_PRESET_CATEGORIES`)
- **DOMAIN (HIGH):** Polish household expense vocabulary from native-language awareness

## Metadata

**Confidence breakdown:**
- Keyword gap analysis: HIGH — direct file analysis, native PL knowledge
- Algorithm gotchas: HIGH — code-level verification of matching logic
- Test data strategy: HIGH — straightforward generation approach
- False positive risks: HIGH — verified through substring logic tracing

**Research date:** 2026-03-27
**Valid until:** No expiry — static analysis of existing codebase
