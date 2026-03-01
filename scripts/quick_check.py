#!/usr/bin/env python3
"""Quick data check"""
import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check software
sw = [i for i in data if i.get('category') == 'Software']
print(f"Software ({len(sw)}):")
for i in sorted(sw, key=lambda x: x.get('name', '')):
    pop = "★" if i.get('popular') else " "
    print(f"  {pop} {i.get('name')}")

# Check for missing major languages
pl = [i for i in data if i.get('category') == 'Programming Language']
names = set(i.get('name', '') for i in pl)

major_langs = ['C', 'C++', 'C#', 'Python', 'JavaScript', 'Java', 'TypeScript', 'Go', 'Rust', 'Swift', 'Kotlin']
print(f"\nChecking major languages:")
for lang in major_langs:
    status = "✓" if lang in names else "✗ MISSING"
    print(f"  {lang}: {status}")

# Check popular tools
tools = [i for i in data if i.get('category') == 'Tool']
pop_tools = [i for i in tools if i.get('popular')]
print(f"\nPopular Tools ({len(pop_tools)}):")
for i in sorted(pop_tools, key=lambda x: x.get('name', '')):
    print(f"  {i.get('name')}")
