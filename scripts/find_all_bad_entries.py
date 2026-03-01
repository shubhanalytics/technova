#!/usr/bin/env python3
"""
Find ALL items across all categories with incorrect URLs or mismatched descriptions.
"""

import json
import re

data = json.load(open('data.json', encoding='utf-8'))

# Bad/generic descriptions that indicate data quality issues
BAD_DESCRIPTIONS = [
    'Systems programming language',
    'Low-level systems programming language',
    'Statistical computing and graphics language',
    'Capability-based language',
    'Array programming for finance',
    'Simple, fast compiled language',
    'Array programming language',
    'Fast, statically typed language by Google',
    'Formal specification language',
    'Array language for kdb+',
    'Functional shell language',
    'Pure object-oriented language',
    'Stream editor for text transformation',
    'Functional programming family',
    'Cloud-native integration language',
]

# Categories where these descriptions make NO sense
CATEGORIES_BAD_WITH_GENERIC_DESC = [
    'IDE/Editor', 'CMS', 'Collaboration', 'Hosting', 'Cloud', 
    'Analytics', 'Design', 'Documentation', 'API', 'Business',
    'Monitoring', 'Testing', 'Security', 'Storage', 'CDN',
    'Container', 'DevOps', 'Message Queue', 'Search', 'Email',
    'Hardware', 'VR/AR', 'Game Engine', 'IoT', 'Low-Code',
    'Serverless', 'Feature Flags', 'Authentication', 'Payment',
]

# Suspicious URL patterns
BAD_URL_PATTERNS = [
    r'marketplace\.', r'wikidata\.org', r'wikipedia\.org',
    r'archive\.org', r'/wiki/', r'wiktionary\.org',
    r'stackoverflow\.com', r'github\.com/topics',
    r'linuxsoft\.cz', r'groups\.io', r'sourceforge\.net/p/',
    r'amazon\.com/(?!aws)', r'ebay\.com', r'aliexpress\.com',
    r'linkedin\.com/groups', r'facebook\.com/groups',
    r'youtube\.com(?!/channel|/c/|/@)', r'slideshare\.net',
    r'doi\.org', r'doi\.ieeecomputersociety', r'd-nb\.info',
]

print("Scanning all entries for problems...")
print("=" * 100)

issues = []

for item in data:
    name = item.get('name', '')
    url = item.get('url', '')
    desc = item.get('description', '')
    cat = item.get('category', '')
    
    problems = []
    
    # Check 1: Bad description in wrong category
    if cat in CATEGORIES_BAD_WITH_GENERIC_DESC:
        for bad_desc in BAD_DESCRIPTIONS:
            if bad_desc in desc and not desc.startswith('[Needs review]'):
                problems.append(f"Generic desc '{bad_desc[:30]}...' in {cat}")
                break
    
    # Check 2: Suspicious URL patterns
    for pattern in BAD_URL_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            problems.append(f"Suspicious URL pattern: {pattern}")
            break
    
    # Check 3: Empty or very short URL
    if not url or len(url) < 10:
        problems.append("Empty or invalid URL")
    
    # Check 4: Name suggests something different from category
    name_lower = name.lower()
    if cat == 'IDE/Editor':
        # These shouldn't be in IDE/Editor
        if any(x in name_lower for x in ['domain', 'registry', 'hosting', 'cms', 'wiki', 'project management']):
            problems.append(f"Name '{name}' doesn't fit IDE/Editor category")
    elif cat == 'Hosting':
        # These shouldn't be in Hosting
        if any(x in name_lower for x in ['editor', 'ide', 'compiler', 'language']):
            problems.append(f"Name '{name}' doesn't fit Hosting category")
    
    if problems:
        issues.append({
            'name': name,
            'url': url,
            'desc': desc,
            'category': cat,
            'problems': problems
        })

# Sort by category for easier review
issues.sort(key=lambda x: (x['category'], x['name']))

print(f"\nTotal issues found: {len(issues)}")
print("=" * 100)

# Group by category
from collections import defaultdict
by_category = defaultdict(list)
for issue in issues:
    by_category[issue['category']].append(issue)

for cat in sorted(by_category.keys()):
    items = by_category[cat]
    print(f"\n### {cat} ({len(items)} issues) ###")
    for item in items[:10]:  # Show first 10 per category
        print(f"\n  {item['name']}")
        print(f"    URL: {item['url'][:60]}{'...' if len(item['url']) > 60 else ''}")
        print(f"    Desc: {item['desc'][:50]}{'...' if len(item['desc']) > 50 else ''}")
        for p in item['problems']:
            print(f"    ⚠️  {p}")
    if len(items) > 10:
        print(f"\n  ... and {len(items) - 10} more in {cat}")

# Save full report
with open('bad_entries_report.json', 'w', encoding='utf-8') as f:
    json.dump(issues, f, indent=2, ensure_ascii=False)

print(f"\n\nFull report saved to bad_entries_report.json")
