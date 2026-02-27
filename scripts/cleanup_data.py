#!/usr/bin/env python3
"""Cleanup and deduplicate data.json.

Rules:
- Normalize names and urls for duplicate detection.
- Prefer non-wikipedia URLs when merging duplicates.
- Merge missing fields (description, sector, country) when possible.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlparse, urlunparse

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'data.json'


def normalize_name(name: str) -> str:
    if not name:
        return ''
    s = name.strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^0-9a-zA-Z ]+", "", s)
    return s.lower()


def normalize_url(url: str) -> str:
    if not url:
        return ''
    try:
        p = urlparse(url)
        scheme = p.scheme or 'https'
        netloc = p.netloc.lower()
        path = p.path.rstrip('/')
        # drop query and fragment for normalization
        return urlunparse((scheme, netloc, path, '', '', ''))
    except Exception:
        return url.strip().lower()


def is_wikipedia(url: str) -> bool:
    return url and 'wikipedia.org' in url.lower()


def merge_entries(a: dict, b: dict) -> dict:
    # merge b into a (prefer non-empty fields, prefer non-wiki url)
    out = a.copy()
    # prefer url: if a is wiki and b is non-wiki prefer b
    a_url = a.get('url','')
    b_url = b.get('url','')
    if is_wikipedia(a_url) and b_url and not is_wikipedia(b_url):
        out['url'] = b_url
    # choose longer description
    if (not out.get('description')) and b.get('description'):
        out['description'] = b.get('description')
    if (not out.get('sector')) and b.get('sector'):
        out['sector'] = b.get('sector')
    if (not out.get('country')) and b.get('country'):
        out['country'] = b.get('country')
    # keep the nicer-cased name (prefer longer)
    if len(b.get('name','')) > len(out.get('name','')):
        out['name'] = b['name']
    return out


def main():
    if not DATA_FILE.exists():
        print('data.json not found')
        return
    data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
    print(f'Loaded {len(data)} items')

    # backup
    bak = DATA_FILE.with_suffix('.bak2')
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Backup written to {bak}')

    by_name = {}
    by_url = {}

    for it in data:
        name = it.get('name','')
        url = it.get('url','')
        nname = normalize_name(name)
        nurl = normalize_url(url)

        if nurl and nurl in by_url:
            # merge into existing by url
            by_url[nurl] = merge_entries(by_url[nurl], it)
            continue

        if nname and nname in by_name:
            # merge with existing name entry
            by_name[nname] = merge_entries(by_name[nname], it)
            # also ensure url mapping
            if nurl:
                by_url[nurl] = by_name[nname]
            continue

        # new entry
        entry = {
            'name': it.get('name','').strip(),
            'url': it.get('url','').strip(),
            'category': it.get('category','').strip(),
            'sector': it.get('sector','').strip(),
            'country': it.get('country','').strip(),
            'description': it.get('description','').strip(),
        }
        if nname:
            by_name[nname] = entry
        if nurl:
            by_url[nurl] = entry

    # produce merged list (prefer alphabetical by name)
    merged = list({v['name']: v for v in list(by_name.values()) + list(by_url.values())}.values())
    merged.sort(key=lambda x: (x.get('category','') or '', x.get('name','').lower()))

    print(f'Reduced to {len(merged)} unique items')

    DATA_FILE.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Wrote cleaned data.json')


if __name__ == '__main__':
    main()
