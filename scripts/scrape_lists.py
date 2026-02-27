#!/usr/bin/env python3
"""Simple scraper to extract link text + href from given pages
and append unique entries to data.json with a supplied category.

Usage:
  Call `main(urls, category)` from a Python runner, or run as script:
    python -m scripts.scrape_lists https://example.com/list "Tool"
"""
import sys
from pathlib import Path
import json
import re

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'data.json'

def fetch_links(url):
    print(f'Fetching {url}')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) technova-bot/1.0'}
    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    # restrict to main content if Wikipedia-like
    main = soup.find(id='bodyContent') or soup.find('main') or soup
    links = []
    for a in main.find_all('a'):
        href = a.get('href')
        text = (a.get_text() or '').strip()
        if not href or not text:
            continue
        # normalize href to absolute
        if href.startswith('//'):
            href = 'https:' + href
        if href.startswith('/'): 
            # build absolute from base
            from urllib.parse import urljoin
            href = urljoin(url, href)
        if not href.startswith('http'):
            continue
        # skip internal anchors, mailto, etc
        if href.startswith('mailto:') or href.startswith('javascript:'):
            continue
        # basic filter: text not too long and contains letters
        if len(text) > 200 or not re.search('[A-Za-z0-9]', text):
            continue
        links.append({'name': text, 'url': href})
    # dedupe by url keeping first
    seen = set(); out = []
    for l in links:
        if l['url'] in seen: continue
        seen.add(l['url']); out.append(l)
    return out

def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding='utf-8'))
    return []

def save_data(items):
    DATA_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding='utf-8')

def append_items(new_items, category=None, sector=None, country=None):
    data = load_data()
    existing_urls = {i.get('url') for i in data}
    added = 0
    for it in new_items:
        if it['url'] in existing_urls:
            continue
        item = {
            'name': it['name'],
            'url': it['url'],
            'category': category or 'Uncategorized',
            'sector': sector or '',
            'country': country or '',
            'description': ''
        }
        data.append(item); existing_urls.add(it['url']); added += 1
    save_data(data)
    return added

def main(urls, category='Uncategorized', sector=None, country=None):
    all_links = []
    for u in urls:
        try:
            links = fetch_links(u)
            all_links.extend(links)
        except Exception as e:
            print(f'Error fetching {u}: {e}')
    print(f'Found {len(all_links)} candidate links; appending unique ones...')
    n = append_items(all_links, category=category, sector=sector, country=country)
    print(f'Added {n} new items to {DATA_FILE}')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python -m scripts.scrape_lists <url1> [<url2> ...] <Category>')
        sys.exit(2)
    *urls, category = sys.argv[1:]
    main(urls, category=category)
