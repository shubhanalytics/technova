#!/usr/bin/env python3
"""Validate and correct item categories in data.json using existing category seeds.

Heuristic:
- Build name->category map from items with non-empty category.
- For each item, if its normalized name appears predominantly in a different category, correct it.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'data.json'


def normalize(s: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]", "", (s or "").lower())


def main():
    data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
    name_to_categories = {}
    for it in data:
        name = normalize(it.get('name',''))
        cat = (it.get('category') or '').strip() or None
        if not name: continue
        if name not in name_to_categories: name_to_categories[name] = {}
        if cat:
            name_to_categories[name][cat] = name_to_categories[name].get(cat,0) + 1

    changed = 0
    corrections = []
    for it in data:
        name_raw = it.get('name','')
        name = normalize(name_raw)
        if not name: continue
        current = (it.get('category') or '').strip() or None
        counts = name_to_categories.get(name, {})
        if not counts: continue
        # pick highest-count category
        best_cat = max(counts.items(), key=lambda x: x[1])[0]
        if current != best_cat:
            # apply correction
            it['category'] = best_cat
            changed += 1
            corrections.append((name_raw, current, best_cat))

    if changed:
        # backup
        DATA_FILE.with_suffix('.validate.bak').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f'Validation complete. Corrected {changed} items.')
    for c in corrections[:40]:
        print(f"{c[0]}: {c[1]} -> {c[2]}")


if __name__ == '__main__':
    main()
