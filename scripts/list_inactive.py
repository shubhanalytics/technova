#!/usr/bin/env python3
"""List all inactive entries for review."""

import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

inactive = [item for item in data if item.get('status') == 'inactive']
print(f'Total inactive entries: {len(inactive)}')
print('\nAll inactive entries:')
for item in sorted(inactive, key=lambda x: x.get('name', '')):
    url = item.get('url', '')[:60]
    print(f"  [{item.get('category', '')}] {item.get('name', '')} - {url}")
