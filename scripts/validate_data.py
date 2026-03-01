#!/usr/bin/env python3
"""Final validation script for Technova data"""

import json
from collections import Counter

def main():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 50)
    print("TECHNOVA DATA VALIDATION")
    print("=" * 50)
    
    # Stats
    print(f"\nTotal items: {len(data)}")
    cats = Counter(i.get('category') for i in data)
    print(f"Total categories: {len(cats)}")
    
    # Check duplicates
    names = [i.get('name', '').lower() for i in data]
    dupes = [name for name, count in Counter(names).items() if count > 1 and name]
    if dupes:
        print(f"\n⚠️  Duplicates found: {len(dupes)}")
        for d in dupes[:10]:
            print(f"   - {d}")
    else:
        print("\n✅ No duplicates")
    
    # Check missing fields
    missing_url = [i.get('name') for i in data if not i.get('url')]
    missing_cat = [i.get('name') for i in data if not i.get('category')]
    missing_desc = [i.get('name') for i in data if not i.get('description')]
    
    if missing_url:
        print(f"\n⚠️  Missing URL: {len(missing_url)}")
        for m in missing_url[:5]:
            print(f"   - {m}")
    else:
        print("✅ All items have URLs")
    
    if missing_cat:
        print(f"\n⚠️  Missing category: {len(missing_cat)}")
    else:
        print("✅ All items have categories")
    
    if missing_desc:
        print(f"\n⚠️  Missing description: {len(missing_desc)}")
        for m in missing_desc[:5]:
            print(f"   - {m}")
    else:
        print("✅ All items have descriptions")
    
    # Check for empty names
    empty_names = [i for i in data if not i.get('name') or i.get('name').strip() == '']
    if empty_names:
        print(f"\n⚠️  Empty names: {len(empty_names)}")
    else:
        print("✅ All items have names")
    
    # Check popular count
    popular = [i for i in data if i.get('popular')]
    print(f"\n📊 Popular items: {len(popular)}")
    
    # Category distribution (top 15)
    print("\n📁 Top 15 Categories:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1])[:15]:
        print(f"   {cat}: {count}")
    
    print("\n" + "=" * 50)
    print("VALIDATION COMPLETE")
    print("=" * 50)

if __name__ == '__main__':
    main()
