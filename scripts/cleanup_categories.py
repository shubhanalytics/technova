#!/usr/bin/env python3
"""Comprehensive category cleanup script for Technova data.json"""

import json
from collections import Counter

def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    data = load_data()
    original_count = len(data)
    changes = []
    
    # ===========================================
    # 1. MERGE ML/AI → AI/ML
    # ===========================================
    for item in data:
        if item.get('category') == 'ML/AI':
            item['category'] = 'AI/ML'
            changes.append(f"Merged ML/AI→AI/ML: {item['name']}")
    
    # ===========================================
    # 2. MERGE Data Visualization → Data Science
    # ===========================================
    for item in data:
        if item.get('category') == 'Data Visualization':
            item['category'] = 'Data Science'
            changes.append(f"Merged DataViz→DataScience: {item['name']}")
    
    # ===========================================
    # 3. REMOVE LICENSES (not tools)
    # ===========================================
    licenses_to_remove = [
        'AGPL', 'BSD license', 'GNU Affero GPL', 'GNU GPL', 'GNU LGPL',
        'GPL', 'MIT License', 'Apache License', 'ISC License', 'MPL',
        'AFL Ver. 3', 'AFNIC'  # Also not a tool
    ]
    data = [item for item in data if item.get('name') not in licenses_to_remove]
    removed_count = original_count - len(data)
    if removed_count > 0:
        changes.append(f"Removed {removed_count} license entries")
    
    # ===========================================
    # 4. FIX "Technology" CATEGORY
    # ===========================================
    tech_reclassify = {
        # Hardware
        'ARM Architecture': 'Hardware',
        'FPGA': 'Hardware',
        'Raspberry Pi': 'Hardware',
        'RISC-V': 'Hardware',
        # Game/3D
        'Unity': 'Game Engine',
        'Unreal Engine': 'Game Engine',
        # IoT/Embedded
        'MQTT': 'IoT',
        'ROS': 'IoT',
        'Arduino': 'Hardware',
        # VR/AR
        'OpenXR': 'VR/AR',
        'WebXR': 'VR/AR',
        # Business Tools
        'CRM': 'Business',
        'Miro': 'Collaboration',
        'Design Systems': 'Design',
        # Energy (remove - not dev tools)
        'Battery Storage': None,
        'Smart Grid': None,
        'Solar PV': None,
    }
    
    items_to_remove = []
    for item in data:
        name = item.get('name')
        if name in tech_reclassify:
            new_cat = tech_reclassify[name]
            if new_cat is None:
                items_to_remove.append(name)
                changes.append(f"Removing non-dev item: {name}")
            else:
                old_cat = item.get('category')
                item['category'] = new_cat
                changes.append(f"Reclassified {name}: {old_cat}→{new_cat}")
    
    data = [item for item in data if item.get('name') not in items_to_remove]
    
    # ===========================================
    # 5. CLEAN "Tool" CATEGORY - Reclassify
    # ===========================================
    tool_reclassify = {
        # Operating Systems
        'AmigaOS': 'Operating System',
        'ChromeOS': 'Operating System',
        'Classic Mac OS': 'Operating System',
        'AIX': 'Operating System',
        'DR DOS 3.31': 'Operating System',
        'FreeBSD': 'Operating System',
        'OpenBSD': 'Operating System',
        'NetBSD': 'Operating System',
        'Solaris': 'Operating System',
        'HP-UX': 'Operating System',
        'IRIX': 'Operating System',
        'QNX': 'Operating System',
        'ReactOS': 'Operating System',
        'Haiku': 'Operating System',
        'Plan 9': 'Operating System',
        'Minix': 'Operating System',
        
        # Companies (remove - not tools)
        'Adobe': None,
        'Adobe Systems': None,
        'Apache Foundation': None,
        'Google': None,
        'Microsoft': None,
        'Oracle': None,
        'IBM': None,
        'Guido van Rossum': None,  # Person, not a tool
        
        # Adobe Products → Design/Tool
        'Adobe Animate': 'Design',
        'Adobe Dreamweaver': 'IDE/Editor',
        'Adobe Flash Builder': 'IDE/Editor',
        'Adobe Business Catalyst': 'CMS',
        
        # Game Engines
        'Unreal Engine': 'Game Engine',
        
        # Hosting (already exists but may be misclassified)
        'Bluehost': 'Hosting',
        'DreamHost': 'Hosting',
        'GlowHost': 'Hosting',
        'Altitude3.Net': 'Hosting',
        
        # IDEs/Editors
        'Aptana Studio': 'IDE/Editor',
        'Arachnophilia': 'IDE/Editor',
        'AonixADT': 'IDE/Editor',
        
        # Hardware
        'Arduino': 'Hardware',
        'Apple II': 'Hardware',
        
        # Version Control
        'Apache Subversion': 'Version Control',
        'Fossil-scm': 'Version Control',
        
        # CMS
        'Alchemy CMS': 'CMS',
        'Ametys CMS': 'CMS',
        'Composr CMS': 'CMS',
        'Alfresco': 'CMS',
        
        # Mobile
        'Android': 'Mobile',
        'Android app development': 'Mobile',
        
        # Runtime
        '.NET': 'Runtime',
        
        # Analytics
        'Analytics': 'Analytics',
        'AnyChart': 'Data Science',
    }
    
    for item in data:
        name = item.get('name')
        if item.get('category') == 'Tool' and name in tool_reclassify:
            new_cat = tool_reclassify[name]
            if new_cat is None:
                items_to_remove.append(name)
                changes.append(f"Removing company/person: {name}")
            else:
                item['category'] = new_cat
                changes.append(f"Reclassified Tool→{new_cat}: {name}")
    
    data = [item for item in data if item.get('name') not in items_to_remove]
    
    # ===========================================
    # 6. FIX Backend/Framework overlap
    # Backend frameworks should stay in Backend
    # Frontend frameworks should be in Framework
    # ===========================================
    frontend_frameworks = ['React', 'Vue.js', 'Angular', 'Svelte', 'Next.js', 'Nuxt']
    backend_frameworks = ['Django', 'Flask', 'Laravel', 'Ruby on Rails', 'Spring']
    
    for item in data:
        name = item.get('name')
        if name in frontend_frameworks:
            item['category'] = 'Frontend'
            changes.append(f"Reclassified to Frontend: {name}")
        elif name in backend_frameworks and item.get('category') == 'Framework':
            item['category'] = 'Backend'
            changes.append(f"Reclassified Framework→Backend: {name}")
    
    # ===========================================
    # 7. Remove duplicates by name (keep first)
    # ===========================================
    seen = set()
    unique_data = []
    for item in data:
        name = item.get('name', '').lower()
        if name and name not in seen:
            seen.add(name)
            unique_data.append(item)
        elif name:
            changes.append(f"Removed duplicate: {item.get('name')}")
    data = unique_data
    
    # ===========================================
    # 8. Fix empty/missing categories
    # ===========================================
    for item in data:
        if not item.get('category'):
            item['category'] = 'Tool'
            changes.append(f"Added missing category for: {item.get('name')}")
    
    # Save
    save_data(data)
    
    # Report
    print("=" * 50)
    print("CATEGORY CLEANUP COMPLETE")
    print("=" * 50)
    print(f"Original items: {original_count}")
    print(f"Final items: {len(data)}")
    print(f"Removed: {original_count - len(data)}")
    print(f"Changes made: {len(changes)}")
    print()
    
    # Show category distribution
    cats = Counter(item.get('category') for item in data)
    print("Category distribution:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    print()
    print("Recent changes (last 30):")
    for change in changes[-30:]:
        print(f"  {change}")

if __name__ == '__main__':
    main()
