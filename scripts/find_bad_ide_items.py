#!/usr/bin/env python3
"""
Find items in IDE/Editor category with incorrect descriptions or URLs.
"""

import json

data = json.load(open('data.json', encoding='utf-8'))

# Bad descriptions that shouldn't be in IDE/Editor
bad_descs = [
    'Systems programming language',
    'Low-level systems programming language',
    'Statistical computing and graphics language',
    'Capability-based language',
    'Array programming',
    'Formal specification language',
    'Simple, fast compiled language',
    'Array language for kdb+',
    'Functional shell language',
    'Pure object-oriented language',
]

# Get IDE/Editor items with suspicious descriptions or URLs
ide_items = [i for i in data if i.get('category') == 'IDE/Editor']
print(f'Total IDE/Editor items: {len(ide_items)}')
print()

suspicious = []
for item in ide_items:
    desc = item.get('description', '')
    url = item.get('url', '')
    name = item.get('name', '')
    
    # Check for bad descriptions
    is_bad_desc = any(bad in desc for bad in bad_descs)
    
    # Check for suspicious URLs (marketplace, documentation sites, wikipedia, etc.)
    is_bad_url = any(x in url.lower() for x in [
        'marketplace', 'wikidata', 'wikipedia', 'archive', 
        'wiki/', 'wiktionary', 'stackoverflow', 'github.com/topics',
        '/docs/', 'linuxsoft', 'groups.io', 'sourceforge.net/p/',
    ])
    
    if is_bad_desc or is_bad_url:
        suspicious.append({
            'name': name,
            'url': url,
            'desc': desc,
            'bad_desc': is_bad_desc,
            'bad_url': is_bad_url
        })

print(f'Suspicious IDE/Editor items: {len(suspicious)}')
print('=' * 100)
for s in suspicious:
    flags = []
    if s['bad_desc']: flags.append('BAD DESC')
    if s['bad_url']: flags.append('BAD URL')
    print(f"{s['name']} [{', '.join(flags)}]")
    print(f"  URL: {s['url']}")
    print(f"  Desc: {s['desc']}")
    print()
