#!/usr/bin/env python3
"""
Data Quality Check - Verify URLs, descriptions, and remove bad entries
"""
import json
import re
from urllib.parse import urlparse

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("DATA QUALITY CHECK")
print("=" * 60)

# Track issues
bad_urls = []
missing_desc = []
duplicates = []
bad_entries = []

# Check for duplicates by name
seen_names = {}
for i, item in enumerate(data):
    name = (item.get('name') or '').strip().lower()
    if name in seen_names:
        duplicates.append({
            'name': item.get('name'),
            'index': i,
            'first_index': seen_names[name]
        })
    else:
        seen_names[name] = i

# Check each item
for item in data:
    name = item.get('name', '').strip()
    url = item.get('url', '').strip()
    desc = item.get('description', '').strip()
    
    # Check URL validity
    if url:
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ('http', 'https'):
                bad_urls.append({'name': name, 'url': url, 'reason': 'Invalid scheme'})
            elif not parsed.netloc:
                bad_urls.append({'name': name, 'url': url, 'reason': 'No domain'})
        except:
            bad_urls.append({'name': name, 'url': url, 'reason': 'Parse error'})
    else:
        bad_urls.append({'name': name, 'url': '', 'reason': 'Missing URL'})
    
    # Check description
    if not desc or len(desc) < 10:
        missing_desc.append({'name': name, 'desc': desc})
    
    # Check for entries that are just URLs or garbage
    if name.startswith('http') or len(name) < 2:
        bad_entries.append({'name': name, 'reason': 'Invalid name'})

print(f"\nTotal items: {len(data)}")

# Report findings
print(f"\n1. BAD URLs: {len(bad_urls)}")
if bad_urls[:10]:
    for item in bad_urls[:10]:
        print(f"   - {item['name'][:40]}: {item['reason']}")
    if len(bad_urls) > 10:
        print(f"   ... and {len(bad_urls) - 10} more")

print(f"\n2. MISSING/SHORT DESCRIPTIONS: {len(missing_desc)}")
if missing_desc[:10]:
    for item in missing_desc[:10]:
        print(f"   - {item['name'][:50]}")
    if len(missing_desc) > 10:
        print(f"   ... and {len(missing_desc) - 10} more")

print(f"\n3. DUPLICATE ENTRIES: {len(duplicates)}")
for item in duplicates[:10]:
    print(f"   - {item['name']}")

print(f"\n4. BAD ENTRIES (invalid names): {len(bad_entries)}")
for item in bad_entries:
    print(f"   - '{item['name']}': {item['reason']}")

# Remove bad entries
print("\n" + "=" * 60)
print("CLEANING DATA")
print("=" * 60)

original_count = len(data)

# Remove entries with invalid names
data = [item for item in data if not (item.get('name', '').startswith('http') or len(item.get('name', '').strip()) < 2)]

# Remove exact duplicates (keep first occurrence)
seen = set()
unique_data = []
for item in data:
    name_lower = (item.get('name') or '').strip().lower()
    if name_lower not in seen:
        seen.add(name_lower)
        unique_data.append(item)

data = unique_data

print(f"Removed {original_count - len(data)} bad/duplicate entries")
print(f"Final count: {len(data)} items")

# Summary by category
print("\nItems by category:")
cats = {}
for item in data:
    cat = item.get('category', 'Unknown')
    cats[cat] = cats.get(cat, 0) + 1

for cat, count in sorted(cats.items()):
    print(f"  {cat}: {count}")

# Save cleaned data
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✓ Saved cleaned data.json")

# Summary stats
items_with_desc = sum(1 for i in data if i.get('description') and len(i['description']) >= 10)
items_with_url = sum(1 for i in data if i.get('url') and i['url'].startswith('http'))
print(f"\nQuality stats:")
print(f"  Items with good description: {items_with_desc}/{len(data)} ({100*items_with_desc//len(data)}%)")
print(f"  Items with valid URL: {items_with_url}/{len(data)} ({100*items_with_url//len(data)}%)")
