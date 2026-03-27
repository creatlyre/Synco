"""
Shopping item categorization coverage test.

Generates 10 curated lists of 100 realistic Polish shopping items,
runs them through the same keyword matching logic as the shopping service,
and saves categorization results as JSON.

Usage:
    python scripts/test_shopping_categorization.py
"""
from __future__ import annotations

import json
import os
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KEYWORDS_PATH = PROJECT_ROOT / "app" / "shopping" / "keywords.json"
RESULTS_DIR = PROJECT_ROOT / "scripts" / "categorization_results"


# ── Replicate exact matching logic from app/shopping/service.py ──────────


def _normalize(text: str) -> str:
    text = text.lower().replace("ł", "l")
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _load_keywords() -> dict[str, list[str]]:
    with open(KEYWORDS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {
        k: [_normalize(kw) for kw in v]
        for k, v in data.items()
        if not k.startswith("_")
    }


def categorize(item_name: str, section_keywords: dict[str, list[str]]) -> str | None:
    norm = _normalize(item_name)
    for section_name, keywords in section_keywords.items():
        for norm_kw in keywords:
            if norm_kw in norm:
                return section_name
            if len(norm) >= 3 and norm in norm_kw:
                return section_name
    return None


# ── 10 curated lists of 100 realistic Polish shopping items ─────────────

LISTS: list[list[str]] = [
    # List 1: Typical weekly family shop
    [
        "mleko", "chleb", "masło", "jajka", "ser żółty", "szynka", "pomidory",
        "ogórki", "ziemniaki", "cebula", "marchewka", "jabłka", "banany",
        "jogurt naturalny", "kefir", "śmietana", "makaron", "ryż", "kasza",
        "mąka", "cukier", "olej", "ocet", "sól", "pieprz", "herbata",
        "kawa", "sok pomarańczowy", "woda mineralna", "chleb tostowy",
        "bułki", "rogaliki", "kiełbasa", "parówki", "boczek", "kurczak",
        "pierś z kurczaka", "mięso mielone", "schab", "żeberka",
        "dorsz", "łosoś", "tuńczyk w puszce", "krewetki", "makrela",
        "serek wiejski", "twaróg", "jajka", "mozzarella", "feta",
        "pomidory", "papryka", "sałata", "szpinak", "brokuły",
        "kalafior", "cukinia", "pieczarki", "czosnek", "imbir",
        "ketchup", "musztarda", "majonez", "sos sojowy", "pesto",
        "dżem", "miód", "nutella", "masło orzechowe", "płatki śniadaniowe",
        "musli", "granola", "owsianka", "budyń", "galaretka",
        "chipsy", "popcorn", "żelki", "czekolada", "baton",
        "piwo", "wino", "wódka", "sok jabłkowy", "woda gazowana",
        "papier toaletowy", "ręcznik papierowy", "mydło", "szampon",
        "pasta do zębów", "proszek do prania", "płyn do naczyń",
        "worki na śmieci", "folia aluminiowa", "gąbka do naczyń",
        "dezodorant", "krem do rąk", "balsam do ciała", "szczoteczka do zębów",
        "pierogi", "pizza mrożona", "frytki mrożone", "nuggetsy", "lody",
    ],
    # List 2: Baking & cooking focused
    [
        "mąka pszenna", "mąka tortowa", "cukier puder", "cukier wanilinowy",
        "drożdże", "proszek do pieczenia", "żelatyna", "kakao", "czekolada gorzka",
        "czekolada mleczna", "orzechy włoskie", "migdały", "pistacje",
        "rodzynki", "wiórki kokosowe", "sezam", "słonecznik", "marcepan",
        "lukier", "posypka", "polewa czekoladowa", "masa makowa", "biszkopty",
        "jajka", "masło", "śmietana", "mleko", "serek mascarpone",
        "twaróg", "ricotta", "cukier", "wanilia", "aromat", "esencja",
        "ser", "jogurt grecki", "budyń waniliowy", "kisiel",
        "herbatniki", "wafelki", "krakersy", "tort", "ciasto",
        "sernik", "szarlotka", "babka", "makowiec", "pączki",
        "drożdżówka", "rogal", "bułka", "chleb", "bagietka",
        "croissant", "graham", "wafle ryżowe", "ciasteczka",
        "kwasek cytrynowy", "soda oczyszczona", "olej", "oliwa",
        "miód", "dżem truskawkowy", "marmolada", "powid", "syrop klonowy",
        "płatki owsiane", "kasza manna", "ryż", "makaron",
        "koncentrat pomidorowy", "passata", "pelati", "bulion",
        "kostka rosołowa", "zupa instant", "makaron instant",
        "kuskus", "soczewica", "ciecierzyca", "fasola",
        "groszek", "kukurydza", "ogórki konserwowe", "kapusta kiszona",
        "ocet", "sos", "ketchup", "musztarda", "majonez",
        "sól", "pieprz", "cynamon", "curry", "papryka mielona",
        "oregano", "bazylia", "tymianek", "rozmaryn", "kminek",
        "liść laurowy", "ziele angielskie", "majeranek", "piernik", "chalka",
    ],
    # List 3: Health-conscious / organic
    [
        "awokado", "szpinak", "jarmuż", "rukola", "sałata rzymska",
        "pomidory koktajlowe", "ogórek", "papryka czerwona", "brokuły",
        "kalafior", "bataty", "seler naciowy", "marchewka", "burak",
        "imbir", "kurkuma", "czosnek", "cebula czerwona",
        "jabłka", "gruszki", "banany", "kiwi", "mango",
        "maliny", "jagody", "borówki", "truskawki", "ananas",
        "jogurt naturalny", "kefir", "mleko owsiane", "mleko migdałowe",
        "tofu", "hummus", "tortilla", "chleb żytni", "bułka grahamka",
        "płatki owsiane", "granola", "musli", "kasza jaglana", "kasza gryczana",
        "ryż brązowy", "makaron pełnoziarnisty", "soczewica", "ciecierzyca",
        "fasola", "oliwki", "kapary", "oliwa z oliwek",
        "tahini", "masło orzechowe", "orzechy włoskie", "migdały",
        "pestki dyni", "słonecznik", "siemię lniane", "sezam",
        "herbata zielona", "herbata miętowa", "yerba mate",
        "woda kokosowa", "smoothie", "sok marchwiowy", "woda mineralna",
        "kombucha", "mleko sojowe", "serek naturalny",
        "jajka", "łosoś", "dorsz", "kurczak", "indyk",
        "pierś z indyka", "szynka z indyka", "schab", "wołowina",
        "szparag", "karczoch", "daktyle", "figi", "morele suszone",
        "żurawina", "rodzynki", "bakalie", "czekolada gorzka",
        "miód", "syrop daktylowy", "masło", "śmietana", "ser kozi",
        "mozzarella", "parmezan", "ricotta", "mascarpone",
        "chleb", "woda", "cytryna", "limonka", "grejpfrut",
        "mandarynki", "pomarańcze", "arbuz", "melon", "nektarynki",
    ],
    # List 4: Family with kids
    [
        "mleko", "jogurt owocowy", "serek homogenizowany", "kefir",
        "jajka", "masło", "chleb", "bułki", "rogaliki",
        "ser żółty", "szynka", "parówki", "kiełbasa", "pasztet",
        "kurczak", "mięso mielone", "pierś z kurczaka",
        "ziemniaki", "marchewka", "pomidory", "ogórki", "sałata",
        "jabłka", "banany", "truskawki", "maliny", "gruszki",
        "mandarynki", "winogrona", "brzoskwinie", "arbuz",
        "makaron", "ryż", "kasza", "płatki śniadaniowe", "musli",
        "mleko czekoladowe", "kakao", "herbata", "sok jabłkowy",
        "woda", "lemoniada", "kompot", "nektar",
        "pierogi", "naleśniki", "pizza mrożona", "nuggetsy", "frytki",
        "krokiety", "pyzy", "knedle", "lody", "budyń",
        "dżem", "nutella", "miód", "cukier", "mąka",
        "ciasteczka", "żelki", "lizaki", "baton", "czekolada",
        "wafelki", "chipsy", "popcorn", "guma do żucia",
        "ketchup", "majonez", "sos", "sól", "pieprz",
        "olej", "ocet", "musztarda", "koncentrat pomidorowy",
        "pampers", "chusteczki", "krem pod pieluszkę", "gryzak",
        "kaszka", "słoiczek", "deserek", "mleko modyfikowane",
        "papier toaletowy", "ręcznik papierowy", "mydło",
        "szampon", "pasta do zębów", "szczoteczka", "dezodorant",
        "proszek do prania", "płyn do naczyń", "worki na śmieci",
        "gąbka", "zmywak", "ściereczka", "serwetki",
        "baterie", "żarówka", "folia spożywcza", "woreczki",
    ],
    # List 5: Party / entertaining
    [
        "piwo", "wino czerwone", "wino białe", "prosecco", "szampan",
        "wódka", "gin", "rum", "whisky", "tequila",
        "aperol", "vermut", "cydr", "likier", "nalewka",
        "piwo bezalkoholowe", "radler", "drink", "miód pitny",
        "cola", "fanta", "sprite", "schweppes", "tonic",
        "ice tea", "woda gazowana", "woda niegazowana", "sok pomarańczowy",
        "lemoniada", "red bull", "energetyk",
        "chipsy", "orzeszki solone", "prażynki", "paluszki solone",
        "krakersy", "oliwki", "hummus", "salami", "szynka parmeńska",
        "ser brie", "ser camembert", "mozzarella", "feta", "parmezan",
        "tortilla", "nachosy", "sos salsa", "guacamole",
        "ogórki konserwowe", "papryka marynowana",
        "baguette", "chleb", "bułki", "croissant",
        "pomidory koktajlowe", "ogórek", "rzodkiewki", "sałata",
        "cytryny", "limonki", "mięta", "pomarańcze",
        "łosoś wędzony", "krewetki", "tuńczyk", "śledzie",
        "kiełbasa", "kabanosy", "boczek", "kurczak", "żeberka",
        "grillowane warzywa", "szaszłyki", "ketchup", "musztarda",
        "majonez", "sos sojowy", "tabasco", "wasabi",
        "ciasto", "tort", "sernik", "tiramisu", "panna cotta",
        "lody", "czekolada", "żelki", "baton", "ciasteczka",
        "serwetki", "kubeczki", "talerzyki", "sztućce jednorazowe",
        "świeczki", "zapałki", "folia aluminiowa", "woreczki",
        "papier toaletowy", "ręcznik papierowy", "mydło",
    ],
    # List 6: Quick weekday meals
    [
        "pierogi ruskie", "naleśniki", "pizza mrożona", "krokiety mrożone",
        "zupa instant", "makaron instant", "zupka chińska", "lane kluski",
        "ryż", "makaron", "kuskus", "kasza bulgur",
        "sałatka gotowa", "danie gotowe", "kanapka", "wrap",
        "kurczak", "schab", "kotlety mielone", "kiełbasa",
        "dorsz", "mintaj", "filet rybny", "paluszki rybne",
        "jajka", "ser", "szynka", "parówki",
        "mleko", "jogurt", "kefir", "masło",
        "chleb", "bułki", "tortilla", "bagietka",
        "pomidory", "ogórek", "sałata", "papryka",
        "cebula", "czosnek", "ziemniaki", "marchewka",
        "pieczarki", "fasola w puszce", "kukurydza",
        "koncentrat pomidorowy", "passata", "pesto", "ketchup",
        "śmietana", "serek kanapkowy", "hummus", "majonez",
        "olej", "oliwa", "masło", "sól", "pieprz",
        "herbata", "kawa", "sok", "woda",
        "jabłka", "banany", "mandarynki", "gruszki",
        "chipsy", "baton", "czekolada", "ciasteczka",
        "papier toaletowy", "mydło", "szampon", "dezodorant",
        "proszek do prania", "płyn do naczyń", "ściereczka",
        "worki na śmieci", "gąbka", "folia spożywcza",
        "piwo", "wino", "woda gazowana", "cola",
        "nuggetsy", "frytki", "pyzy", "mrożonki",
        "bulion", "kostka rosołowa", "przyprawy", "oregano",
        "cukier", "mąka", "budyń", "galaretka",
    ],
    # List 7: Baby household
    [
        "pampers", "pieluchy", "chusteczki nawilżane", "krem pod pieluszkę",
        "oliwka dla dzieci", "kąpiel dla dzieci", "gryzak", "śliniak",
        "kaszka", "słoiczek", "deserek dla dzieci", "herbatka dla dzieci",
        "mleko modyfikowane", "mleko następne", "woda dla niemowląt",
        "mleko", "jogurt", "kefir", "serek homogenizowany",
        "masło", "jajka", "chleb", "bułki",
        "ser żółty", "szynka", "parówki", "kurczak",
        "pierś z kurczaka", "mięso mielone", "indyk", "schab",
        "ziemniaki", "marchewka", "brokuły", "kalafior",
        "dynia", "cukinia", "szpinak", "pomidory",
        "jabłka", "banany", "gruszki", "truskawki",
        "maliny", "jagody", "morele", "brzoskwinie",
        "makaron", "ryż", "kasza jaglana", "płatki owsiane",
        "musli", "granola", "budyń", "kisiel",
        "dżem", "miód", "nutella", "czekolada",
        "ciasteczka", "wafelki", "żelki", "lizaki",
        "herbata", "kawa", "sok jabłkowy", "woda",
        "papier toaletowy", "ręcznik papierowy", "mydło",
        "szampon", "żel pod prysznic", "pasta do zębów",
        "dezodorant", "krem do rąk", "balsam",
        "proszek do prania", "płyn do płukania", "płyn do naczyń",
        "tabletki do zmywarki", "worki na śmieci", "serwetki",
        "pierogi", "naleśniki", "pizza", "frytki",
        "lody", "piwo", "wino", "woda gazowana",
        "baterie", "żarówka", "plaster", "bandaż",
        "folia aluminiowa", "woreczki", "gąbka", "zmywak",
        "chips", "popcorn", "baton", "sok pomarańczowy",
        "mąka", "cukier", "sól", "pieprz", "olej",
    ],
    # List 8: Fish & seafood lover
    [
        "łosoś", "dorsz", "tuńczyk", "makrela", "pstrąg",
        "sandacz", "halibut", "morszczuk", "tilapia", "mintaj",
        "krewetki", "małże", "owoce morza", "sardynki", "szproty",
        "śledzie", "matjas", "anchois", "kawior", "ikra",
        "surimi", "paluszki rybne", "filet rybny", "ryba wędzona",
        "łosoś wędzony", "śledzik", "karp",
        "cytryny", "limonki", "koper", "natka pietruszki",
        "czosnek", "imbir", "cebula", "szalotka",
        "pomidory", "ogórek", "sałata", "rukola",
        "szpinak", "szparagi", "papryka", "awokado",
        "oliwa", "olej", "ocet", "sos sojowy",
        "wasabi", "tabasco", "pesto", "majonez",
        "masło", "śmietana", "ser", "jajka",
        "chleb", "bagietka", "bułki", "tortilla",
        "ryż", "makaron", "kuskus", "ziemniaki",
        "mleko", "jogurt", "kefir", "woda",
        "wino białe", "piwo", "prosecco", "woda gazowana",
        "herbata", "kawa", "sok", "lemoniada",
        "sól", "pieprz", "curry", "kurkuma",
        "bazylia", "oregano", "tymianek", "rozmaryn",
        "kapary", "oliwki", "ogórki konserwowe",
        "chipsy", "czekolada", "ciasteczka", "baton",
        "papier toaletowy", "mydło", "szampon",
        "płyn do naczyń", "gąbka", "worki na śmieci",
        "folia aluminiowa", "folia spożywcza",
        "koncentrat pomidorowy", "passata", "ketchup", "musztarda",
        "dżem", "miód", "masło orzechowe", "nutella",
    ],
    # List 9: Pet owner + household
    [
        "karma dla kota", "karma dla psa", "żwirek", "przysmak dla psa",
        "papier toaletowy", "ręcznik papierowy", "mydło", "szampon",
        "żel pod prysznic", "pasta do zębów", "dezodorant", "balsam",
        "krem do rąk", "krem do twarzy", "odżywka", "peeling",
        "proszek do prania", "płyn do prania", "kapsułki do prania",
        "płyn do naczyń", "tabletki do zmywarki", "płyn do płukania",
        "spray do szyb", "płyn do podłóg", "odplamiacz", "odkamieniacz",
        "odświeżacz", "kostka do wc", "żel do wc", "wybielacz",
        "worki na śmieci", "gąbka", "zmywak", "ściereczka",
        "rękawice gumowe", "folia aluminiowa", "folia spożywcza", "woreczki",
        "serwetki", "zapałki", "świeczki", "baterie", "żarówka",
        "plaster", "bandaż", "aspiryna",
        "mleko", "chleb", "masło", "jajka",
        "ser żółty", "szynka", "kurczak", "mięso mielone",
        "ziemniaki", "marchewka", "cebula", "pomidory",
        "jabłka", "banany", "pomarańcze", "mandarynki",
        "makaron", "ryż", "kasza", "płatki owsiane",
        "herbata", "kawa", "sok", "woda",
        "piwo", "wino", "cola", "woda gazowana",
        "chipsy", "czekolada", "ciasteczka", "żelki",
        "dżem", "miód", "ketchup", "musztarda",
        "sól", "pieprz", "olej", "oliwa",
        "jogurt", "kefir", "śmietana", "twaróg",
        "pierogi", "pizza", "lody", "nuggetsy",
        "rajstopy", "skarpetki", "reklamówki",
        "lakier do włosów", "żel do włosów", "pianka do włosów",
        "maszynka do golenia", "żyletki", "waciki", "płatki kosmetyczne",
    ],
    # List 10: Seasonal / BBQ + mixed
    [
        "kiełbasa grillowa", "karkówka", "żeberka", "skrzydełka",
        "szaszłyki", "boczek", "kurczak", "steak",
        "sałatka", "pomidory", "ogórek", "papryka",
        "cebula", "czosnek", "kukurydza", "ziemniaki",
        "chleb", "bułki", "bagietka", "tortilla",
        "ketchup", "musztarda", "majonez", "sos barbecue",
        "piwo", "piwo bezalkoholowe", "radler", "wino",
        "wódka", "gin", "cydr", "lemoniada",
        "cola", "fanta", "sprite", "woda gazowana",
        "sok pomarańczowy", "ice tea", "red bull",
        "chipsy", "orzeszki", "prażynki", "nachosy",
        "oliwki", "hummus", "salami", "ser brie",
        "mozzarella", "feta", "camembert", "gouda",
        "arbuz", "melon", "truskawki", "wiśnie",
        "czereśnie", "maliny", "jagody", "brzoskwinie",
        "lody", "czekolada", "żelki", "ciasteczka",
        "tort", "sernik", "tiramisu", "panna cotta",
        "mleko", "jogurt", "kefir", "masło",
        "jajka", "śmietana", "ser", "szynka",
        "makaron", "ryż", "herbata", "kawa",
        "cukier", "sól", "pieprz", "olej",
        "papier toaletowy", "szampon", "mydło", "dezodorant",
        "worki na śmieci", "serwetki", "talerzyki jednorazowe",
        "folia aluminiowa", "zapałki", "świeczki",
        "dżem", "miód", "nutella", "masło orzechowe",
        "mąka", "drożdże", "rogal", "pączek",
        "karma dla kota", "żwirek", "baterie", "żarówka",
    ],
]


def run_test() -> dict:
    section_keywords = _load_keywords()
    results_dir = RESULTS_DIR
    results_dir.mkdir(parents=True, exist_ok=True)

    all_uncategorized: list[dict] = []
    per_list_summaries: list[dict] = []

    for i, item_list in enumerate(LISTS, 1):
        items_result: list[dict] = []
        categorized_count = 0
        uncategorized_count = 0

        for item_name in item_list:
            section = categorize(item_name, section_keywords)
            items_result.append({
                "name": item_name,
                "normalized": _normalize(item_name),
                "section_matched": section,
            })
            if section:
                categorized_count += 1
            else:
                uncategorized_count += 1
                all_uncategorized.append({
                    "list": i,
                    "name": item_name,
                    "normalized": _normalize(item_name),
                })

        total = len(item_list)
        rate = round(categorized_count / total * 100, 1) if total else 0

        list_result = {
            "list_number": i,
            "total": total,
            "categorized": categorized_count,
            "uncategorized_count": uncategorized_count,
            "rate": rate,
            "items": items_result,
        }

        list_file = results_dir / f"list_{i:02d}.json"
        with open(list_file, "w", encoding="utf-8") as f:
            json.dump(list_result, f, ensure_ascii=False, indent=2)

        per_list_summaries.append({
            "list": i,
            "total": total,
            "categorized": categorized_count,
            "uncategorized": uncategorized_count,
            "rate": rate,
        })

    total_items = sum(s["total"] for s in per_list_summaries)
    total_categorized = sum(s["categorized"] for s in per_list_summaries)
    total_uncategorized = sum(s["uncategorized"] for s in per_list_summaries)
    overall_rate = round(total_categorized / total_items * 100, 1) if total_items else 0

    summary = {
        "total_items": total_items,
        "total_categorized": total_categorized,
        "total_uncategorized": total_uncategorized,
        "overall_rate": overall_rate,
        "per_list_rates": per_list_summaries,
        "all_uncategorized_items": all_uncategorized,
    }

    summary_file = results_dir / "summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # Print results
    print("=" * 60)
    print("SHOPPING ITEM CATEGORIZATION TEST RESULTS")
    print("=" * 60)
    print(f"{'List':>6} | {'Total':>5} | {'Categorized':>11} | {'Uncat.':>6} | {'Rate':>6}")
    print("-" * 60)
    for s in per_list_summaries:
        print(f"  {s['list']:>4} | {s['total']:>5} | {s['categorized']:>11} | {s['uncategorized']:>6} | {s['rate']:>5}%")
    print("-" * 60)
    print(f" TOTAL | {total_items:>5} | {total_categorized:>11} | {total_uncategorized:>6} | {overall_rate:>5}%")
    print("=" * 60)

    if all_uncategorized:
        print(f"\nUncategorized items ({len(all_uncategorized)}):")
        for item in all_uncategorized:
            print(f"  List {item['list']:>2}: {item['name']!r} (normalized: {item['normalized']!r})")

    print(f"\nResults saved to: {results_dir}")
    return summary


if __name__ == "__main__":
    run_test()
