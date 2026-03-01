#!/usr/bin/env python3
"""
Analyze all items categorized as "Tool" and suggest reclassifications.
Also identify suspicious/generic descriptions.
"""

import json
import re
from collections import Counter

# Load data
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Get all Tool entries
tools = [i for i in data if i.get('category') == 'Tool']
print(f"Total 'Tool' entries: {len(tools)}")
print("=" * 100)

# Available categories for reference
categories = sorted(set(i.get('category', '') for i in data))
print(f"\nAvailable categories: {categories}")
print("=" * 100)

# Generic/suspicious descriptions that indicate copy-paste errors
generic_descriptions = [
    "Low-level systems programming language",
    "Statistical computing and graphics language",
    "Systems programming language",
    "Capability-based language",
    "Array programming for finance",
    "Simple, fast compiled language",
    "Array programming language",
    "Fast, statically typed language by Google",
    "Formal specification language",
    "Array language for kdb+",
]

# Categorization rules based on name/URL/description keywords
category_rules = {
    'Hosting': ['hosting', 'domain', 'registrar', 'dns', 'cpanel', 'plesk', 'cloudflare'],
    'Cloud': ['aws', 'azure', 'gcp', 'cloud', 'digitalocean', 'linode', 'vultr'],
    'IDE/Editor': ['ide', 'editor', 'vim', 'emacs', 'sublime', 'notepad', 'vscode', 'intellij', 'eclipse'],
    'Version Control': ['git', 'svn', 'mercurial', 'version control', 'bitbucket', 'gitlab'],
    'Database': ['database', 'sql', 'mysql', 'postgres', 'mongodb', 'redis', 'nosql', 'db'],
    'DevOps': ['devops', 'jenkins', 'ansible', 'puppet', 'chef', 'terraform', 'ci/cd', 'cicd'],
    'Monitoring': ['monitoring', 'logging', 'metrics', 'apm', 'observability', 'grafana', 'prometheus'],
    'Security': ['security', 'firewall', 'antivirus', 'encryption', 'vpn', 'ssl', 'auth'],
    'Testing': ['test', 'selenium', 'cypress', 'jest', 'mocha', 'qa', 'quality'],
    'Documentation': ['documentation', 'docs', 'wiki', 'readme', 'markdown'],
    'Collaboration': ['collaboration', 'slack', 'teams', 'chat', 'communication', 'project management'],
    'CMS': ['cms', 'wordpress', 'drupal', 'joomla', 'content management'],
    'Email': ['email', 'mail', 'smtp', 'imap'],
    'CDN': ['cdn', 'content delivery'],
    'Container': ['docker', 'container', 'kubernetes', 'k8s', 'podman'],
    'Build Tool': ['build', 'make', 'gradle', 'maven', 'webpack', 'bundler'],
    'Package Manager': ['package manager', 'npm', 'pip', 'cargo', 'gem'],
    'Programming Language': ['programming language', 'compiler', 'interpreter'],
    'Library': ['library', 'framework', 'sdk'],
    'CLI': ['cli', 'command line', 'terminal', 'shell'],
    'API': ['api', 'rest', 'graphql', 'endpoint'],
    'Mobile': ['mobile', 'android', 'ios', 'flutter', 'react native'],
    'Frontend': ['frontend', 'css', 'html', 'javascript', 'react', 'vue', 'angular', 'ui'],
    'Backend': ['backend', 'server', 'node', 'express', 'django', 'flask'],
    'Analytics': ['analytics', 'tracking', 'metrics', 'dashboard'],
    'Storage': ['storage', 's3', 'blob', 'file storage'],
    'Search': ['search', 'elasticsearch', 'solr', 'algolia'],
    'Message Queue': ['queue', 'kafka', 'rabbitmq', 'pubsub', 'messaging'],
    'Serverless': ['serverless', 'lambda', 'functions'],
}

# Analyze each tool
suggestions = []
bad_descriptions = []

for tool in tools:
    name = tool.get('name', '').lower()
    url = tool.get('url', '').lower()
    desc = tool.get('description', '')
    
    # Check for generic/bad description
    if desc in generic_descriptions:
        bad_descriptions.append(tool)
    
    # Try to suggest a better category
    suggested_cat = None
    for cat, keywords in category_rules.items():
        for kw in keywords:
            if kw in name or kw in url or kw in desc.lower():
                suggested_cat = cat
                break
        if suggested_cat:
            break
    
    if suggested_cat:
        suggestions.append({
            'name': tool['name'],
            'url': tool.get('url', ''),
            'current_desc': desc,
            'suggested_category': suggested_cat,
            'has_bad_desc': desc in generic_descriptions
        })

# Output results
print(f"\n\n{'='*100}")
print("ITEMS WITH BAD/GENERIC DESCRIPTIONS:")
print(f"{'='*100}")
for item in bad_descriptions[:50]:
    print(f"  {item['name']}: \"{item.get('description', '')}\"")
if len(bad_descriptions) > 50:
    print(f"  ... and {len(bad_descriptions) - 50} more")

print(f"\n\n{'='*100}")
print("SUGGESTED RECLASSIFICATIONS:")
print(f"{'='*100}")
for s in suggestions:
    bad_flag = " [BAD DESC]" if s['has_bad_desc'] else ""
    print(f"  {s['name']} -> {s['suggested_category']}{bad_flag}")
    print(f"    URL: {s['url']}")
    print(f"    Desc: {s['current_desc']}")
    print()

print(f"\n{'='*100}")
print("SUMMARY:")
print(f"  Total 'Tool' items: {len(tools)}")
print(f"  Items with bad descriptions: {len(bad_descriptions)}")
print(f"  Items with suggested reclassification: {len(suggestions)}")
print(f"{'='*100}")

# Output JSON for processing
import json
output = {
    'tools_count': len(tools),
    'bad_descriptions': [{'name': t['name'], 'desc': t.get('description', '')} for t in bad_descriptions],
    'suggestions': suggestions,
    'all_tools': [{'name': t['name'], 'url': t.get('url', ''), 'desc': t.get('description', '')} for t in tools]
}

with open('tool_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("\nDetailed analysis saved to tool_analysis.json")
