#!/usr/bin/env python3
import json
import sys
from urllib.parse import urlparse

def load_data(path='data.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_safe_url(u):
    try:
        p = urlparse(u)
        if p.scheme in ('http','https',''):
            return True
    except Exception:
        pass
    return False

def main():
    issues = 0
    data = load_data()
    for i,item in enumerate(data):
        name = item.get('name','')
        desc = item.get('description','') or ''
        if '<' in name or '<' in desc:
            print(f'XSS-like character in item #{i}: {name}')
            issues += 1
        url = item.get('url','')
        if url and not is_safe_url(url):
            print(f'Unsafe URL scheme in item #{i}: {url}')
            issues += 1
    if issues:
        print(f'Found {issues} issues')
        sys.exit(2)
    print('Security checks passed')

if __name__ == "__main__":
    main()
