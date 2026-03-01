import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_JSON = ROOT / 'data.json'
DATA_MIN = ROOT / 'data.min.json'

KEYWORDS = ['ai/ml', 'ai', 'ml', 'tools', 'software', 'application', 'tool']

def looks_like_software(domains):
    if not domains:
        return False
    for d in domains:
        dd = d.lower()
        for k in KEYWORDS:
            if k in dd:
                return True
    return False

def reclassify(items):
    changed = 0
    for it in items:
        cat = it.get('category')
        if cat != 'Programming Language':
            continue
        domains = it.get('domains') or []
        if looks_like_software(domains):
            it['category'] = 'Software'
            changed += 1
    return changed

def main():
    if not DATA_JSON.exists():
        print('data.json not found')
        return
    items = json.loads(DATA_JSON.read_text(encoding='utf-8'))
    if not isinstance(items, list):
        print('unexpected data.json format')
        return
    changed = reclassify(items)
    if changed:
        DATA_JSON.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding='utf-8')
        # update minified version as well
        try:
            DATA_MIN.write_text(json.dumps(items, separators=(',', ':'), ensure_ascii=False), encoding='utf-8')
        except Exception:
            pass
        print(f'Reclassified {changed} items to Software')
    else:
        print('No items reclassified')

if __name__ == '__main__':
    main()
