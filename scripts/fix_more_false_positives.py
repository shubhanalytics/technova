#!/usr/bin/env python3
"""Fix remaining false positives that are actually active."""

import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# More active products to fix
active_products = {
    # Active products with sites that block bots
    "Uniface": "Low-code enterprise application platform",
    "SKILL": "Scripting language for Cadence EDA tools",
    "Zesty.io": "Headless CMS platform",
    "Onepager pro": "Project timeline and roadmap software",
    "Sellerdeck": "E-commerce platform for UK businesses",
    "NetPoint": "Project scheduling software",
    "Codelobster": "Free PHP, JavaScript, HTML, CSS IDE",
    "JOE": "Joe's Own Editor - terminal text editor",
    "Kile": "LaTeX editor for KDE",
    "LXDE": "Lightweight X11 Desktop Environment",
    "Seed7": "Extensible programming language",
    "Unicon": "High-level goal-directed programming language",
    "Agilent VEE": "Visual programming for test automation (Keysight)",
    "Teamcenter": "Product lifecycle management by Siemens",
    "CodeWarrior": "IDE for embedded systems by NXP",
    "VisualWorks": "Smalltalk development environment by Cincom",
}

# Items to mark as truly inactive/historical with better descriptions
historical_items = {
    "Rome": "Discontinued JavaScript toolchain (merged into Biome)",
    "Symbian": "Discontinued mobile OS (Nokia, ended 2012)",
    "Maemo": "Discontinued Linux mobile OS (Nokia)",
    "DR DOS 3.31": "Historical DOS operating system (1988)",
    "System Software 6": "Historical Mac OS version (1988)",
    "Tru64 UNIX": "Discontinued HP/DEC UNIX (support ended 2012)",
    "VisiCalc": "First spreadsheet program (1979, historical)",
    "Lotus Symphony": "Discontinued office suite (IBM, ended 2014)",
    "Borland Kylix": "Discontinued Linux IDE (ended 2005)",
    "Aptana Studio": "Discontinued web IDE (last release 2015)",
    "PHPEclipse": "Discontinued PHP Eclipse plugin",
    "EDLIN": "MS-DOS line editor (legacy, included for reference)",
}

fixed_count = 0

for item in data:
    name = item.get('name', '')
    
    # Fix false positives - mark as active
    if name in active_products:
        if item.get('status') == 'inactive':
            item['status'] = 'active'
            desc = item.get('description', '')
            if desc.startswith('['):
                bracket_end = desc.find(']')
                if bracket_end != -1:
                    desc = desc[bracket_end + 1:].strip()
            if not desc or len(desc) < 5:
                desc = active_products[name]
            item['description'] = desc
            print(f"  ✅ Fixed active: {name}")
            fixed_count += 1
    
    # Update descriptions for truly historical items
    elif name in historical_items:
        current_desc = item.get('description', '')
        if not current_desc.startswith('[Historical'):
            item['description'] = f"[Historical] {historical_items[name]}"
            print(f"  📜 Updated historical: {name}")

# Count final stats
active_count = sum(1 for item in data if item.get('status') == 'active')
inactive_count = sum(1 for item in data if item.get('status') == 'inactive')

print(f"\n{'='*60}")
print(f"✅ Fixed {fixed_count} more false positives")
print(f"📊 Active: {active_count}, Inactive: {inactive_count}")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Saved to data.json")
