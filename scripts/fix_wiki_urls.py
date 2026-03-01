#!/usr/bin/env python3
"""Fix entries with wiki URLs."""

import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fixes for wiki URL entries
wiki_fixes = {
    "Machine code": {
        "description": "Low-level CPU instructions",
        "url": "https://en.wikipedia.org/wiki/Machine_code"  # Keep Wikipedia as it's a concept
    },
    "FPGA": {
        "description": "Field-programmable gate arrays for custom hardware logic",
        "url": "https://www.xilinx.com/"  # Major FPGA vendor
    },
    "DENIC": {
        "description": "German .de domain name registry",
        "url": "https://www.denic.de/"
    },
    "free": {
        "remove": True  # Concept, not a product
    },
    "IBM Lotus Symphony": {
        "description": "Free office suite by IBM (discontinued)",
        "url": "https://www.ibm.com/"  # Product discontinued
    },
    "KCells": {
        "description": "KDE spreadsheet application (now Calligra Sheets)",
        "url": "https://calligra.org/sheets/"
    },
    "Midnight Commander": {
        "description": "Visual file manager for Unix-like systems",
        "url": "https://midnight-commander.org/"
    },
    "proprietary": {
        "remove": True  # Concept, not a product
    },
    "Resolver One": {
        "description": "Python-based spreadsheet (discontinued)",
        "url": "https://www.resolversystems.com/"  # Company site
    },
    "C": {
        "description": "Low-level systems programming language",
        "url": "https://www.iso.org/standard/74528.html"  # ISO C standard
    }
}

fixed_count = 0
removed_count = 0
new_data = []

for item in data:
    name = item.get('name', '')
    
    if name in wiki_fixes:
        fixes = wiki_fixes[name]
        
        if fixes.get('remove'):
            print(f"  Removing concept: {name}")
            removed_count += 1
            continue
        
        changes = []
        if 'description' in fixes:
            item['description'] = fixes['description']
            changes.append("desc")
        if 'url' in fixes:
            item['url'] = fixes['url']
            changes.append("url")
        
        if changes:
            print(f"  Fixed {name}: {', '.join(changes)}")
            fixed_count += 1
    
    new_data.append(item)

print(f"\n✅ Fixed {fixed_count} entries")
print(f"✅ Removed {removed_count} concept entries")
print(f"📊 Total entries: {len(data)} -> {len(new_data)}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print("\n✅ Saved to data.json")
