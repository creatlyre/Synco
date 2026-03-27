---
phase: quick-260327-jif
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - app/shopping/keywords.json
  - scripts/test_shopping_categorization.py
autonomous: true
requirements: [QUICK-JIF]

must_haves:
  truths:
    - "keywords.json covers bread/bakery, frozen foods, ready meals, pet food, snacks, and household items"
    - "10 curated lists of 100 Polish shopping items exercise all 10 Biedronka sections"
    - "Categorization script reuses exact matching logic from service.py (_normalize + substring + reverse match)"
    - "Overall categorization rate is ≥ 95%"
    - "All uncategorized items are explicitly listed for review"
    - "Results are saved as JSON files"
  artifacts:
    - path: "app/shopping/keywords.json"
      provides: "Comprehensive Biedronka shopping keyword mapping"
      contains: "chleb"
    - path: "scripts/test_shopping_categorization.py"
      provides: "Standalone categorization test with 10×100 item lists"
      min_lines: 200
    - path: "scripts/categorization_results/"
      provides: "JSON result files from test runs"
  key_links:
    - from: "scripts/test_shopping_categorization.py"
      to: "app/shopping/keywords.json"
      via: "Loads and normalizes keywords identically to service.py"
      pattern: "_normalize|SECTION_KEYWORDS|keywords.json"
    - from: "scripts/test_shopping_categorization.py"
      to: "scripts/categorization_results/"
      via: "Writes per-list and summary JSON"
      pattern: "json.dump|categorization_results"
---

<objective>
Expand keywords.json to achieve comprehensive Biedronka shopping item coverage, validate with 10 curated lists of 100 realistic Polish items, and iterate until ≥ 95% categorization rate.

Purpose: Shopping list items typed by Polish users should land in the correct Biedronka store section, not "Uncategorized". Current coverage has critical gaps (bread, frozen, ready meals, pets, snacks).
Output: Updated keywords.json, categorization test script, JSON result files proving ≥ 95% rate.
</objective>

<execution_context>
@~/.copilot/get-shit-done/workflows/execute-plan.md
@~/.copilot/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/quick/260327-jif-full-coverage-shopping-item-categorizati/260327-jif-CONTEXT.md
@.planning/quick/260327-jif-full-coverage-shopping-item-categorizati/260327-jif-RESEARCH.md
@app/shopping/keywords.json
@app/shopping/service.py

<interfaces>
<!-- Categorization engine from service.py — replicate this logic exactly in the test script -->

```python
def _normalize(text: str) -> str:
    """Lowercase, strip diacritics (including Polish ł→l), collapse whitespace."""
    text = text.lower().replace("ł", "l")
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

# Matching logic (from _categorize_item):
# 1. For each section in JSON order (first match wins):
#    a. norm_kw in norm  (keyword substring in item)
#    b. len(norm) >= 3 and norm in norm_kw  (reverse: item substring in keyword)
# 2. Return section name on first match, None if no match
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Expand keywords.json with all missing keywords from research</name>
  <files>app/shopping/keywords.json</files>
  <action>
Add ALL missing keywords identified in RESEARCH.md to keywords.json. Maintain the existing JSON structure and _meta field. Use Polish diacritics forms for readability (the engine normalizes at load time).

**Pieczenie / Bakalie — add bread/bakery items:**
chleb, bułka, bułki, rogal, rogalik, bagietka, croissant, drożdżówka, pączek, pączki, tort, ciasto, sernik, szarlotka, babka, makowiec, chleb tostow, graham, wafle ryżow, ciastka, ciasteczk, herbatnik, soda oczyszczon, kwasek cytryn, cukier wanili, aromat, esencja

**Nabiał i Lodówki — add ready meals + frozen:**
pierogi, naleśnik, pizza, krokiet, pyzy, knedle, sałatka gotow, danie gotow, kanapk, wrap, mrożonk, parmezan, cheddar, serek wiejsk, serek homogeniz, serek topion, serek kanapkow, nuggets, frytki, panna cotta, tiramisu

**Puszki, Sosy, Przetwory — add pantry + snacks:**
bulion, kostka rosołow, zupa instant, zupka, baton, batonik, wafle, żelki, lizak, guma do żucia, popcorn, prażynk, sos sojow, pesto, tahini, tabasco, wasabi, kisiel, galaretka, lane kluski, makaron instant

**Chemia / Higiena — add household + pet food:**
karma, żwirek, przysmak dla, tabletki do zmywark, płyn do płukan, kapsułki do prani, odplamiacz, spray do szyb, płyn do podłóg, kostka do wc, żel do wc, odkamieniacz, żarówka, rękawice gumow, żel do włos, lakier do włos, pianka do włos, plaster, opatrunek, bandaż, rajstopy, skarpet, aspiryna

**Napoje — additions:**
smoothie, koktajl, woda smakow, syrop do wody, herbata mrożon, yerba, mate, kawa rozpuszczal, napój izotonicz, woda kokosow

**Alkohol — additions:**
piwo bezalkoholow, radler, wino musując, nalewka, miód pitny, drink

**Lada Tradycyjna / Mięso — additions:**
smalec, słonina, bekon, hamburger, baleron, metka, krakowska, żywiecka, podwawelska, kiszka, kaszanka, flaki, ozorki, stek, kości rosołow

**Ryby — additions:**
morszczuk, anchois, filet rybny, matjas, śledzik, ryba wędzon, kawior, ikra

**Warzywa i Owoce — additions:**
daktyl, figa, granat, liczi, marakuja, papaja, szparag, karczoch, kalarepa, oliwki, oliwka, kapary

**Dział Dziecięcy — additions:**
krem pod pieluszk, oliwka dla dziec, kąpiel dziec, gryzak, śliniaczek, herbatka dla dziec

Ensure valid JSON after editing. Do NOT break existing keywords — only ADD new entries to each section's array.
  </action>
  <verify>
    <automated>python -c "import json; d=json.load(open('app/shopping/keywords.json','r',encoding='utf-8')); assert '_meta' in d; assert 'chleb' in d['Pieczenie / Bakalie']; assert 'karma' in d['Chemia / Higiena']; assert 'pierogi' in d['Nabiał i Lodówki']; assert 'bulion' in d['Puszki, Sosy, Przetwory']; print(f'OK: {sum(len(v) for k,v in d.items() if k!=\"_meta\")} keywords')"</automated>
  </verify>
  <done>keywords.json has comprehensive coverage for all common Biedronka items including bread, frozen, ready meals, pet food, snacks, household. Total keyword count > 600.</done>
</task>

<task type="auto">
  <name>Task 2: Create categorization test script with 10 × 100 curated item lists</name>
  <files>scripts/test_shopping_categorization.py</files>
  <action>
Create a standalone Python script (no pytest, no DB required) at scripts/test_shopping_categorization.py that:

1. **Replicates the exact matching logic from service.py:**
   - Import `_normalize` pattern: `text.lower().replace("ł", "l")` → `unicodedata.normalize("NFKD", text)` → strip combining chars
   - Load keywords.json from `app/shopping/keywords.json` (relative to project root)
   - Match logic: for each section in JSON order, check `norm_kw in norm` then `len(norm) >= 3 and norm in norm_kw`. First match wins.

2. **Define 10 curated lists of 100 realistic Polish shopping items each:**
   - Items are generic human-style: "mleko", "chleb", "masło" — NOT brand-specific
   - Each list covers a realistic shopping trip mix across all 10 sections
   - Lists should have variety — not all identical distributions
   - Include tricky items: short words (mak, sos, rum), diacritics (bułka, żeberka), compound items (masło orzechowe, woda gazowana)
   - Total: exactly 1000 items

3. **Run categorization and report:**
   - For each list: count categorized vs uncategorized, compute rate
   - Overall: total categorized / 1000 × 100 = rate%
   - Print per-list summary table and overall rate to stdout
   - List ALL uncategorized items with their list number

4. **Save results as JSON:**
   - Create `scripts/categorization_results/` directory
   - Per-list: `list_01.json` through `list_10.json` with `{list_number, total, categorized, uncategorized_count, rate, items: [{name, section_matched, normalized}]}`
   - Summary: `summary.json` with `{total_items, total_categorized, total_uncategorized, overall_rate, per_list_rates: [...], all_uncategorized_items: [...]}`

Run with: `python scripts/test_shopping_categorization.py` from project root.
  </action>
  <verify>
    <automated>python scripts/test_shopping_categorization.py</automated>
  </verify>
  <done>Script runs without errors, produces 10 list JSON files + summary.json in scripts/categorization_results/, prints categorization rates to stdout.</done>
</task>

<task type="auto">
  <name>Task 3: Iterate keywords until ≥ 95% categorization rate</name>
  <files>app/shopping/keywords.json, scripts/test_shopping_categorization.py</files>
  <action>
Run the categorization script from Task 2. Examine the uncategorized items list.

If overall rate < 95%:
1. Read the uncategorized items from output / summary.json
2. Add missing keywords to app/shopping/keywords.json for each uncategorized item — place in the most appropriate section
3. Re-run the script
4. Repeat until overall rate ≥ 95% AND no single list is below 90%

If items are genuinely ambiguous or extremely niche (e.g., foreign foods, brand-only names), accept them as uncategorized rather than adding overly broad keywords that could cause false positives.

After achieving target rate, ensure final results are saved to scripts/categorization_results/.
  </action>
  <verify>
    <automated>python -c "import json; s=json.load(open('scripts/categorization_results/summary.json')); assert s['overall_rate']>=95, f'Rate {s[\"overall_rate\"]}%'; print(f'PASS: {s[\"overall_rate\"]}% ({s[\"total_categorized\"]}/{s[\"total_items\"]})')"</automated>
  </verify>
  <done>Final summary.json shows overall categorization rate ≥ 95%, no list below 90%. All result JSON files saved.</done>
</task>

</tasks>

<verification>
1. keywords.json is valid JSON with _meta field and all 10 sections
2. Script runs cleanly: `python scripts/test_shopping_categorization.py`
3. `scripts/categorization_results/summary.json` exists and shows rate ≥ 95%
4. 10 per-list JSON files exist in `scripts/categorization_results/`
5. All uncategorized items are documented in summary.json
</verification>

<success_criteria>
- keywords.json expanded with 150+ new keywords covering bread, frozen, ready meals, pets, snacks, household
- Categorization test script with 10 × 100 curated Polish shopping items runs against actual engine logic
- Overall categorization rate ≥ 95% (at least 950/1000 items categorized)
- No single list below 90% rate
- All results saved as JSON in scripts/categorization_results/
</success_criteria>

<output>
After completion, create `.planning/quick/260327-jif-full-coverage-shopping-item-categorizati/260327-jif-SUMMARY.md`
</output>
