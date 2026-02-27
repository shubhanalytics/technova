#!/usr/bin/env python3
"""Remove obvious junk / commit-message-like entries from data.json.

Heuristics used:
- Remove entries whose name is short or a single punctuation/letter like 'v', 't', 'e', 'edit'.
- Remove entries starting with long numeric IDs (e.g., '482387 – ...').
- Remove entries that look like commit messages (start with digits and words like add/fix/update/merge), or contain verbs like 'add'/'fix' and are long (>6 words).
- Remove entries where url is an edit link or contains 'Special:' or 'Template:'.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'data.json'


SHORT_BLACKLIST = set(['v','t','e','edit','their own page'])


def is_junk_name(name: str) -> bool:
    if not name: return True
    s = name.strip()
    if len(s) <= 1:
        return True
    low = s.lower()
    if low in SHORT_BLACKLIST:
        return True
    # starts with a long numeric id
    if re.match(r'^\d{3,}\b', s):
        return True
    # commit-like: starts with digits or contains 'add ' or 'fix ' and is long
    words = re.findall(r"\w+", s)
    if (re.match(r'^\d+\s*[-–]', s) or re.match(r'^(add|fix|update|merge)\b', low)) and len(words) > 3:
        return True
    if any(tok in low for tok in ['pull request', 'merge', 'commit', 'issue', 'patch']):
        return True
    return False


def is_junk_url(url: str) -> bool:
    if not url: return True
    low = url.lower()
    if 'w/index.php' in low and 'action=edit' in low:
        return True
    if 'template:' in low or 'special:' in low:
        return True
    return False


def main():
    data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
    kept = []
    removed = []
    for it in data:
        name = it.get('name','')
        url = it.get('url','')
        if is_junk_name(name) or is_junk_url(url):
            removed.append((name, url))
            continue
        kept.append(it)

    if not removed:
        print('No obvious junk entries found.')
        return

    # backup
    DATA_FILE.with_suffix('.junk.bak').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    DATA_FILE.write_text(json.dumps(kept, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f'Removed {len(removed)} junk entries. Backup saved to {DATA_FILE.with_suffix(".junk.bak")}')
    for name,url in removed[:40]:
        print(f'- {name} -> {url}')


if __name__ == '__main__':
    main()
