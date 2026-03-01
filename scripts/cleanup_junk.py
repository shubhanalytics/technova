#!/usr/bin/env python3
"""Clean up remaining junk entries."""

import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Junk entry names (case-insensitive)
junk_names = ['the original', 'external links', 'see also', 'references', 'notes', 
              'further reading', 'sources', 'bibliography', 'links', 'footnotes']

# Wiki URL patterns that shouldn't be product pages
wiki_patterns = ['en.wikipedia.org', 'wikidata.org', 'wiktionary.org', 'wikiversity.org',
                 'wikia.com', 'fandom.com']

to_remove = []
new_data = []

for item in data:
    name = item.get('name', '').strip()
    url = item.get('url', '')
    
    # Check for junk names
    if name.lower() in junk_names:
        print(f"  Removing junk: {name}")
        to_remove.append(name)
        continue
    
    # Check for wiki URLs (these need review but keep them for now)
    if any(p in url for p in wiki_patterns):
        print(f"  Wiki URL (keeping for review): {name} -> {url[:60]}")
    
    new_data.append(item)

print(f"\n✅ Removed {len(to_remove)} junk entries")
print(f"📊 Total entries: {len(data)} -> {len(new_data)}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print("\n✅ Saved to data.json")
