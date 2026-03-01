#!/usr/bin/env python3
"""Fix entries with generic descriptions and bad URLs."""

import json

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fixes for generic descriptions
description_fixes = {
    # CMS
    "Adobe Business Catalyst": {
        "description": "All-in-one hosted solution for web designers",
        "url": "https://www.adobe.com/"
    },
    "Alchemy CMS": {
        "description": "Open source Rails content management system"
    },
    "Ametys CMS": {
        "description": "Java-based open source content management system"
    },
    "Composr CMS": {
        "description": "Powerful open source website CMS and social platform"
    },
    "Magento": {
        "description": "Open source e-commerce platform",
        "url": "https://business.adobe.com/products/magento/magento-commerce.html"
    },
    "Squarespace": {
        "description": "Website builder and hosting platform"
    },
    "Webflow": {
        "description": "Visual web design and development platform"
    },
    
    # Hosting
    "Altitude3.Net": {
        "description": "Web hosting provider",
        "url": "https://altitude3.net"
    },
    "Bluehost": {
        "description": "Web hosting and WordPress hosting provider",
        "url": "https://www.bluehost.com"
    },
    "DreamHost": {
        "description": "Web hosting and cloud services provider",
        "url": "https://www.dreamhost.com"
    },
    
    # IDE/Editor
    "Adobe Dreamweaver": {
        "description": "Web design and development IDE from Adobe"
    },
    "Adobe Flash Builder": {
        "description": "IDE for developing mobile and web apps using Flex/ActionScript"
    },
    "AonixADT": {
        "description": "Ada development toolkit for Eclipse IDE",
        "url": "https://www.adacore.com/"
    },
    "Aptana Studio": {
        "description": "Open source web development IDE based on Eclipse"
    },
    "Arachnophilia": {
        "description": "Free HTML and programming editor for Windows"
    },
    "Dolphin Smalltalk": {
        "description": "Smalltalk development environment for Windows"
    },
    "Zed": {
        "description": "High-performance code editor from the creators of Atom"
    },
    
    # Analytics
    "Analytics": {
        "description": "Data analytics and business intelligence tools",
        "url": "https://analytics.google.com/",
        "name": "Google Analytics"
    },
    
    # Mobile
    "Android app development": {
        "description": "Native app development for Android platform",
        "url": "https://developer.android.com/"
    },
    
    # Documentation
    "Document management system": {
        "description": "Systems for organizing and managing digital documents",
        "url": "https://en.wikipedia.org/wiki/Document_management_system"
    },
    "KOffice": {
        "description": "KDE office suite (deprecated, now Calligra)",
        "url": "https://calligra.org/"
    },
    "Web document": {
        "description": "Web-based document creation and sharing",
        "url": "https://docs.google.com/"
    },
    
    # Hosting - DNS entries
    "DNS Belgium": {
        "description": "Registry for .be domain names",
        "url": "https://www.dnsbelgium.be/"
    },
    "Top-level domain": {
        "description": "Internet domain name classification",
        "url": "https://www.icann.org/resources/pages/tlds-2012-02-25-en"
    }
}

# Entries to remove (concepts, not actual tools/products)
entries_to_remove = [
    # Concept entries that shouldn't be product listings
    "Click tracking",  # DOI link, concept not product
    "SAML",  # Wikipedia link, protocol not product
    "CRM",  # Wikipedia link, concept not product
    "Collaborative software",  # DOI link, concept
    "Code completion",  # DOI link, concept
    "Developer",  # DOI link, role not product
    "Kanban (development)",  # Wikidata link, methodology not product
    "Open source",  # Dictionary link, concept
    "Permissive",  # Dictionary link, concept
    "commercial",  # DOI link, concept
    "doi",  # Meta entry about DOI
    "Design Systems",  # Wikipedia concept
    "GUI-baseddesign",  # Wikiversity, typo in name, concept
    "CPL",  # DOI link, historical language
    "Categories",  # MediaWiki, meta entry
    "CorVision",  # Wiktionary, wrong URL
    "Darwin",  # DOI bioinformatics link, wrong context
    "Definitions",  # Wiktionary, concept
    "Hermes",  # DOI link
    "Klerer-May System",  # DOI link, historical
    "LYaPAS",  # Russian wiki, obscure
    "ML",  # DOI link (the language ML, not machine learning)
    "PDP-11s",  # Wiktionary link, hardware concept
    "Other platforms",  # Wikidata meta
    "content management frameworks",  # Wikidata, concept
    "Personalization management system (PMS)",  # DOI, concept
    "Website governance",  # LinkedIn group, concept
    "Invoicing",  # Wiktionary, concept
]

# Track changes
fixed_count = 0
removed_count = 0
new_data = []

for item in data:
    name = item.get('name', '')
    
    # Check if should be removed
    if name in entries_to_remove:
        print(f"  Removing: {name}")
        removed_count += 1
        continue
    
    # Check if needs description/URL fix
    if name in description_fixes:
        fixes = description_fixes[name]
        changes = []
        
        if 'description' in fixes:
            old_desc = item.get('description', '')[:50]
            item['description'] = fixes['description']
            changes.append(f"desc: '{old_desc}...' -> '{fixes['description']}'")
        
        if 'url' in fixes:
            old_url = item.get('url', '')[:40]
            item['url'] = fixes['url']
            changes.append(f"url: '{old_url}' -> '{fixes['url']}'")
        
        if 'name' in fixes:
            old_name = item.get('name', '')
            item['name'] = fixes['name']
            changes.append(f"name: '{old_name}' -> '{fixes['name']}'")
        
        if changes:
            print(f"  Fixed {name}: {'; '.join(changes)}")
            fixed_count += 1
    
    new_data.append(item)

print(f"\n✅ Fixed {fixed_count} entries")
print(f"✅ Removed {removed_count} concept/invalid entries")
print(f"📊 Total entries: {len(data)} -> {len(new_data)}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print("\n✅ Saved to data.json")
