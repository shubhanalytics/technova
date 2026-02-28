#!/usr/bin/env python3
"""
enrich_companies.py

Fetch company pages from Wikipedia categories and attempt to extract founding year and website.
This script is aggressive by default but supports a --limit per category to avoid overloading.

Usage:
  python scripts/enrich_companies.py --limit 100

Notes:
 - Uses the public MediaWiki API (no credentials).
 - Adds non-duplicated entries to data.json with fields: name, url, year, description, category.
 - Results are written to `data.enriched.json` to avoid overwriting original data.json.
"""

import argparse
import json
import re
import time
from urllib.parse import urlencode
from urllib.request import urlopen, Request

WIKI_API = 'https://en.wikipedia.org/w/api.php'


def wiki_api(params):
    params['format'] = 'json'
    url = WIKI_API + '?' + urlencode(params)
    req = Request(url, headers={'User-Agent': 'technova-enricher/1.0 (https://github.com)'})
    with urlopen(req, timeout=30) as r:
        return json.load(r)


def get_category_members(category, limit=200):
    members = []
    cmcontinue = None
    while True:
        params = {'action': 'query', 'list': 'categorymembers', 'cmtitle': f'Category:{category}', 'cmlimit': min(limit,500)}
        if cmcontinue:
            params['cmcontinue'] = cmcontinue
        data = wiki_api(params)
        chunk = data.get('query', {}).get('categorymembers', [])
        members.extend(chunk)
        if 'continue' in data and len(members) < limit:
            cmcontinue = data['continue'].get('cmcontinue')
            if not cmcontinue:
                break
        else:
            break
        if len(members) >= limit:
            break
    return members[:limit]


def get_page_extract(title):
    data = wiki_api({'action': 'query', 'prop': 'extracts', 'exintro': 1, 'explaintext': 1, 'titles': title})
    pages = data.get('query', {}).get('pages', {})
    for p in pages.values():
        return p.get('extract', '')
    return ''


def get_page_wikitext(title):
    data = wiki_api({'action': 'query', 'prop': 'revisions', 'rvslots': 'main', 'rvprop': 'content', 'titles': title})
    pages = data.get('query', {}).get('pages', {})
    for p in pages.values():
        revs = p.get('revisions', [])
        if revs:
            return revs[0].get('slots', {}).get('main', {}).get('*', '')
    return ''


def extract_year_and_website(wikitext):
    # look for common infobox fields: founded=founded, founded=, foundation=, established=
    year = None
    website = None
    # try simple regex on wikitext
    m = re.search(r'\|\s*(?:founded|founded_date|founded_year|founded_in|foundedyear|founded_at)\s*=\s*([^\n\r\|]+)', wikitext, re.I)
    if not m:
        m = re.search(r'\|\s*(?:foundation|established|founded)\s*=\s*([^\n\r\|]+)', wikitext, re.I)
    if m:
        s = re.sub(r'<.*?>', '', m.group(1)).strip()
        # find a 4-digit year
        y = re.search(r'(19|20)\d{2}', s)
        if y:
            year = y.group(0)

    m2 = re.search(r'\|\s*(?:website|url|homepage)\s*=\s*\[?\s*(https?://[^\s\]\|]+)', wikitext, re.I)
    if m2:
        website = m2.group(1).strip()

    return year, website


def normalize_name(n):
    return re.sub(r'\s+', ' ', n or '').strip()


def load_data(path='data.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data, path='data.enriched.json'):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main(limit_per_category=200):
    print('Loading existing data.json...')
    try:
        base = load_data()
    except Exception:
        base = []

    existing_names = set((normalize_name(i.get('name', '')).lower() for i in base))
    existing_urls = set((i.get('url') for i in base if i.get('url')))

    categories = [
        'Artificial intelligence companies',
        'Software companies',
        'Internet companies',
        'Technology companies',
        'Startups'
    ]

    added = 0
    for cat in categories:
        print(f'Fetching members of category: {cat} (limit {limit_per_category})')
        members = get_category_members(cat, limit=limit_per_category)
        for m in members:
            title = m.get('title')
            name = normalize_name(title)
            key = name.lower()
            if key in existing_names:
                continue
            # fetch page extract and wikitext
            try:
                extract = get_page_extract(title)
                wikitext = get_page_wikitext(title)
            except Exception as e:
                print('  skip', title, '(', e, ')')
                time.sleep(0.5)
                continue

            year, website = extract_year_and_website(wikitext)
            if website and website in existing_urls:
                continue

            item = {
                'name': name,
                'description': (extract or '')[:400].strip(),
                'category': 'Company',
            }
            if year:
                item['year'] = year
            if website:
                item['url'] = website
            base.append(item)
            existing_names.add(key)
            if website:
                existing_urls.add(website)
            added += 1
            if added % 10 == 0:
                print(f'  added {added} so far...')
            time.sleep(0.5)

    print(f'Finished. Added {added} new entries. Writing to data.enriched.json')
    save_data(base)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--limit', type=int, default=100, help='Per-category limit of pages to fetch (default 100)')
    args = p.parse_args()
    main(limit_per_category=args.limit)
