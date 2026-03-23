import re, json, glob

en = json.load(open("app/locales/en.json", encoding="utf-8"))
pl = json.load(open("app/locales/pl.json", encoding="utf-8"))

keys = set()
for tpl in glob.glob("app/templates/**/*.html", recursive=True):
    with open(tpl, encoding="utf-8") as f:
        content = f.read()
    keys.update(re.findall(r"t\('([^']+)'\)", content))

missing_en = [k for k in sorted(keys) if k not in en]
missing_pl = [k for k in sorted(keys) if k not in pl]

print(f"Keys in templates: {len(keys)}")
print(f"EN missing ({len(missing_en)}):", missing_en if missing_en else "NONE")
print(f"PL missing ({len(missing_pl)}):", missing_pl if missing_pl else "NONE")

en_only = sorted(set(en) - set(pl))
pl_only = sorted(set(pl) - set(en))
print(f"In EN not PL ({len(en_only)}):", en_only if en_only else "NONE")
print(f"In PL not EN ({len(pl_only)}):", pl_only if pl_only else "NONE")
