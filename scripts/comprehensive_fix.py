#!/usr/bin/env python3
"""
Comprehensive data cleanup and fixes
"""
import json
import re

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ============================================
# Fix Software -> Programming Language
# These are languages incorrectly labeled as Software
# ============================================
SOFTWARE_TO_LANGUAGE = {
    'APL', 'Assembly language', 'Bosque', 'Ch', 'Charm', 'Dog', 'Hop', 'IDL',
    'Io', 'Magik', 'Max', 'MaxScript', 'Nim', 'Orc', 'Tea', 'es',
    'GDScript (Godot)', 'LotusScript', 'Maya (MEL)', 'MuPAD', 'OmniMark',
    'Project Verona', 'Wolfram Language', 'XC', 'Maple', 'SAS', 'Stata',
    'CLIPS', 'EASYTRIEVE PLUS', 'Easy PL/I', 'C/AL', 'ACC', 'Action!', 
    'IBM Basic assembly language', 'AIMMS', 'Agilent VEE', 'LabVIEW',
    'Simulink', 'Stateflow', 'PeopleCode', 'Powerhouse', 'Net.Data', 'SPL',
    'DATATRIEVE', 'X++ (X plus plus/Microsoft Dynamics AX)',
    'Accent (Rational Synergy)'  # Actually this is a version control, skip it
}

# Items that really are software platforms, keep them
KEEP_AS_SOFTWARE = {
    'Apex (Salesforce.com, Inc)',  # Salesforce platform
    'Delphi Community',  # IDE
    'Unreal Engine',  # Game engine
    'App Inventor for Android\'s visual block language (MIT App Inventor)',  # Visual platform
}

# ============================================
# Add missing major languages
# ============================================
MISSING_LANGUAGES = [
    {
        'name': 'C',
        'description': 'General-purpose procedural programming language supporting structured programming',
        'url': 'https://en.wikipedia.org/wiki/C_(programming_language)',
        'category': 'Programming Language',
        'popular': True,
        'year': 1972
    },
    {
        'name': 'C++',
        'description': 'General-purpose programming language with object-oriented, generic, and functional features',
        'url': 'https://isocpp.org/',
        'category': 'Programming Language',
        'popular': True,
        'year': 1985
    },
    {
        'name': 'C#',
        'description': 'Modern object-oriented programming language developed by Microsoft for .NET',
        'url': 'https://docs.microsoft.com/en-us/dotnet/csharp/',
        'category': 'Programming Language',
        'popular': True,
        'year': 2000
    }
]

# ============================================
# Fix bad Tool entries (URLs, licenses, etc)
# ============================================
BAD_TOOL_PATTERNS = [
    r'^https?://',  # URLs shouldn't be names
    r'Apache.*License',
    r'^Apache\s+\d',  # Apache 2.0 etc (licenses)
]

# ============================================
# Truly popular items per category
# ============================================
POPULAR_LANGUAGES = {
    'c', 'c++', 'c#', 'python', 'javascript', 'typescript', 'java', 'go', 'rust',
    'swift', 'kotlin', 'php', 'ruby', 'scala', 'perl', 'lua', 'r', 'matlab',
    'sql', 'html', 'css', 'shell', 'bash', 'powershell', 'dart', 'elixir',
    'erlang', 'haskell', 'clojure', 'julia', 'objective-c', 'f#', 'groovy',
    'visual basic', 'vb.net', 'fortran', 'cobol', 'lisp', 'scheme', 'prolog',
    'ada', 'assembly', 'assembly language'
}

POPULAR_TOOLS = {
    'git', 'docker', 'kubernetes', 'npm', 'webpack', 'vite', 'eslint', 'prettier',
    'jest', 'mocha', 'pytest', 'jenkins', 'nginx', 'apache', 'postgresql', 'mysql',
    'mongodb', 'redis', 'elasticsearch', 'kafka', 'terraform', 'ansible',
    'prometheus', 'grafana', 'helm', 'postman', 'github'
}

POPULAR_SOFTWARE = {
    'visual studio', 'vs code', 'intellij', 'pycharm', 'android studio', 'xcode',
    'eclipse', 'sublime text', 'atom', 'vim', 'emacs', 'figma', 'slack', 'discord',
    'unity', 'unreal engine', 'blender', 'delphi'
}

POPULAR_FRAMEWORKS = {
    'react', 'vue', 'angular', 'svelte', 'next.js', 'nuxt', 'express', 'fastapi',
    'django', 'flask', 'rails', 'laravel', 'spring', '.net', 'node.js', 'tailwind',
    'bootstrap'
}

POPULAR_CLOUD = {
    'aws', 'azure', 'google cloud', 'gcp', 'heroku', 'vercel', 'netlify',
    'cloudflare', 'digitalocean', 'firebase', 'supabase'
}

POPULAR_AI = {
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
    'opencv', 'hugging face', 'openai', 'langchain'
}

def normalize(name):
    return re.sub(r'[^a-z0-9+#.]', '', str(name).lower())

def is_bad_tool(name):
    for pattern in BAD_TOOL_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            return True
    return False

def is_popular(item):
    name = str(item.get('name', '')).lower()
    norm = normalize(name)
    cat = item.get('category', '')
    
    if cat == 'Programming Language':
        for lang in POPULAR_LANGUAGES:
            if norm == normalize(lang) or name == lang:
                return True
        return False
    elif cat == 'Tool':
        for tool in POPULAR_TOOLS:
            if normalize(tool) in norm or tool in name:
                return True
        return False
    elif cat == 'Software':
        for sw in POPULAR_SOFTWARE:
            if normalize(sw) in norm or sw in name:
                return True
        return False
    elif cat == 'Framework':
        for fw in POPULAR_FRAMEWORKS:
            if normalize(fw) in norm or fw in name:
                return True
        return False
    elif cat == 'Cloud':
        for c in POPULAR_CLOUD:
            if normalize(c) in norm or c in name:
                return True
        return False
    elif cat == 'AI/ML':
        for ai in POPULAR_AI:
            if normalize(ai) in norm or ai in name:
                return True
        return False
    return False

# ============================================
# Apply fixes
# ============================================

print("=" * 60)
print("FIXING DATA")
print("=" * 60)

# 1. Fix Software -> Programming Language
print("\n1. Moving misclassified Software to Programming Language:")
moved = 0
for item in data:
    name = item.get('name', '')
    if item.get('category') == 'Software' and name in SOFTWARE_TO_LANGUAGE and name not in KEEP_AS_SOFTWARE:
        print(f"   {name}")
        item['category'] = 'Programming Language'
        moved += 1
print(f"   Moved {moved} items")

# 2. Add missing languages
print("\n2. Adding missing major languages:")
existing_names = {item.get('name') for item in data}
for lang in MISSING_LANGUAGES:
    if lang['name'] not in existing_names:
        print(f"   Adding {lang['name']}")
        data.append(lang)

# 3. Remove bad tool entries
print("\n3. Removing bad Tool entries:")
bad_tools = [item for item in data if item.get('category') == 'Tool' and is_bad_tool(item.get('name', ''))]
for item in bad_tools[:10]:  # Show first 10
    print(f"   Removing: {item.get('name', '')[:60]}")
data = [item for item in data if not (item.get('category') == 'Tool' and is_bad_tool(item.get('name', '')))]
print(f"   Removed {len(bad_tools)} items")

# 4. Update popular flags
print("\n4. Updating popular flags:")
for item in data:
    item['popular'] = is_popular(item)

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

cats = {}
for item in data:
    cat = item.get('category', 'Unknown')
    if cat not in cats:
        cats[cat] = {'total': 0, 'popular': 0}
    cats[cat]['total'] += 1
    if item.get('popular'):
        cats[cat]['popular'] += 1

for cat, c in sorted(cats.items()):
    print(f"  {cat}: {c['popular']} popular / {c['total']} total")

# Show popular Programming Languages
print("\nPopular Programming Languages:")
pop_pl = [i for i in data if i.get('category') == 'Programming Language' and i.get('popular')]
for item in sorted(pop_pl, key=lambda x: x['name']):
    print(f"  - {item['name']}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✓ Saved data.json ({len(data)} items)")
