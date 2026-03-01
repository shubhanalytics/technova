#!/usr/bin/env python3
"""
Analyze remaining Tool items and reclassify them.
"""

import json
import re

# Load data
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Get remaining Tool items
tools = [i for i in data if i.get('category') == 'Tool']
print(f"Total remaining Tool items: {len(tools)}")
print("=" * 100)

# Print all remaining tools
for t in sorted(tools, key=lambda x: x['name']):
    print(f"{t['name']} | {t.get('url', '')[:50]} | {t.get('description', '')[:50]}")
