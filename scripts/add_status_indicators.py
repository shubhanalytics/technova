#!/usr/bin/env python3
"""
Add status indicators to data.json entries based on URL check results.
- status: "active" | "inactive" 
- For inactive entries, update descriptions to indicate historical status.
"""

import json

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('url_check_report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

# Build lookup of broken/ssl items
broken_items = set()
for item in report.get('broken', []):
    broken_items.add(item['name'])
for item in report.get('ssl_error', []):
    broken_items.add(item['name'])

# Historical/inactive message prefixes based on category
category_messages = {
    "Programming Language": "Historical programming language",
    "IDE/Editor": "Legacy development environment",
    "CMS": "Legacy content management system",
    "Database": "Legacy database system",
    "Framework": "Legacy framework",
    "Library": "Legacy library",
    "Operating System": "Legacy operating system",
    "Hardware": "Historical hardware platform",
    "Collaboration": "Discontinued collaboration tool",
    "default": "Inactive/historical project"
}

def get_inactive_message(category):
    return category_messages.get(category, category_messages["default"])

# Process each item
active_count = 0
inactive_count = 0

for item in data:
    name = item.get('name', '')
    category = item.get('category', '')
    desc = item.get('description', '')
    
    if name in broken_items:
        item['status'] = 'inactive'
        inactive_count += 1
        
        # Update description if it doesn't already have the inactive marker
        if not desc.startswith('[Inactive]') and not desc.startswith('[Historical]'):
            prefix = get_inactive_message(category)
            if desc:
                # Keep original description but add prefix
                item['description'] = f"[{prefix}] {desc}"
            else:
                item['description'] = f"[{prefix}]"
    else:
        item['status'] = 'active'
        active_count += 1

print(f"✅ Marked {active_count} entries as active (green dot)")
print(f"🔴 Marked {inactive_count} entries as inactive (red dot)")
print(f"📊 Total: {len(data)} entries")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ Saved status indicators to data.json")
