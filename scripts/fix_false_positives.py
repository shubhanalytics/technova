#!/usr/bin/env python3
"""
Fix false positives - active products incorrectly marked as inactive.
These sites block bots but are definitely active.
"""

import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Known active products that were false positives (their sites block bots)
active_products = {
    # AI/ML - All major AI products are active
    "DALL-E": "AI image generation by OpenAI",
    "OpenAI": "Leading AI research company",
    "OpenAI API": "API for GPT models and AI services",
    "Meta AI": "AI research and products by Meta",
    "Midjourney": "AI image generation platform",
    "Whisper": "AI speech recognition by OpenAI",
    "OpenCV": "Open source computer vision library",
    
    # Major tech companies/startups
    "Canva": "Online design and visual communication platform",
    "Coinbase": "Cryptocurrency exchange platform",
    "DoorDash": "Food delivery platform",
    "Meesho": "Social commerce platform",
    "Nykaa": "Beauty and fashion e-commerce platform",
    
    # Hosting & Domain registrars
    "GoDaddy": "Domain registrar and web hosting",
    "Bluehost": "Web hosting provider",
    "Namecheap": "Domain registrar and hosting",
    "NameSilo": "Domain registrar",
    "Network Solutions": "Domain registrar and web services",
    "Register.com": "Domain registration service",
    "Web.com": "Web hosting and domain services",
    "CIRA": "Canadian Internet Registration Authority",
    "Linode": "Cloud hosting by Akamai",
    
    # Databases
    "MySQL": "Popular open-source relational database",
    "Couchbase": "NoSQL document database",
    "FaunaDB": "Serverless database (now Fauna)",
    "RethinkDB": "Real-time database for web apps",
    "Percona Server": "Enhanced MySQL-compatible database",
    
    # Development tools & IDEs
    "CodePen": "Online code editor and social development environment",
    "MATLAB": "Numerical computing environment by MathWorks",
    "Simulink": "Simulation and model-based design by MathWorks",
    "NPM": "Node.js package manager",
    "JVM": "Java Virtual Machine runtime",
    "Wine": "Windows compatibility layer for Unix",
    
    # CMS
    "Drupal": "Open source content management framework",
    "Umbraco": ".NET CMS platform",
    "OpenCart": "Open source e-commerce platform",
    "XWiki": "Wiki and collaboration platform",
    "Backdrop CMS": "Free CMS fork of Drupal 7",
    "DNN": "DotNetNuke - .NET CMS platform",
    "Nucleus CMS": "PHP-MySQL blog platform",
    
    # Business/Analytics
    "Tableau": "Business intelligence and analytics platform",
    "NetSuite": "Cloud ERP and business management software",
    "SAP Business ByDesign": "Cloud ERP for mid-size companies",
    "SAP BusinessObjects": "Business intelligence suite",
    "AppDynamics": "Application performance monitoring (Splunk)",
    "Workfront": "Work management platform by Adobe",
    
    # Game engines
    "Unreal Engine": "Game engine by Epic Games",
    "Phaser": "HTML5 game framework",
    
    # Email/Marketing
    "ConvertKit": "Email marketing for creators",
    "Ko-fi": "Creator monetization platform",
    "Loops": "Email platform for SaaS",
    "React Email": "React components for email",
    
    # Libraries/Frameworks
    "Naive UI": "Vue 3 component library",
    "Nivo": "React data visualization components",
    "nopCommerce": "Open source e-commerce platform",
    "AnyChart": "JavaScript charting library",
    
    # Standards (these are specs, not products - always active)
    "CSS": "Cascading Style Sheets - web styling standard",
    "HTML5": "HTML5 markup language standard",
    "XML": "Extensible Markup Language standard",
    "XSLT": "XML stylesheet transformation language",
    "XQuery": "XML query language",
    "RDF": "Resource Description Framework standard",
    "OWL": "Web Ontology Language standard",
    
    # Message Queues
    "Redis Pub/Sub": "Redis publish/subscribe messaging",
    "Upstash Kafka": "Serverless Kafka service",
    
    # Other active products
    "Height": "Project management tool",
    "Goalscape": "Visual goal management software",
    "SuperAgent": "HTTP request library for Node.js",
    "exa": "Modern replacement for ls command",
    
    # Programming languages that are active
    "UnrealScript": "Scripting language for Unreal Engine",
    "MuPAD": "Computer algebra system (now part of MATLAB)",
    "Stateflow": "State machine and flow chart tool by MathWorks",
}

# Track changes
fixed_count = 0

for item in data:
    name = item.get('name', '')
    
    if name in active_products:
        if item.get('status') == 'inactive':
            item['status'] = 'active'
            
            # Fix description - remove [Inactive...] prefix
            desc = item.get('description', '')
            if desc.startswith('['):
                # Find the closing bracket and remove the prefix
                bracket_end = desc.find(']')
                if bracket_end != -1:
                    desc = desc[bracket_end + 1:].strip()
            
            # Use our clean description if original is empty or was just the prefix
            if not desc or len(desc) < 5:
                desc = active_products[name]
            
            item['description'] = desc
            print(f"  ✅ Fixed: {name}")
            fixed_count += 1

# Count final stats
active_count = sum(1 for item in data if item.get('status') == 'active')
inactive_count = sum(1 for item in data if item.get('status') == 'inactive')

print(f"\n{'='*60}")
print(f"✅ Fixed {fixed_count} false positives")
print(f"📊 Active: {active_count}, Inactive: {inactive_count}")
print(f"📊 Total: {len(data)} entries")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ Saved to data.json")
