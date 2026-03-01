#!/usr/bin/env python3
"""
Fix misclassified items and refine popular marking
"""
import json
import re

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Items that should be Programming Language (currently in Software/Tool)
SHOULD_BE_LANGUAGE = {
    'Delphi', 'Go', 'Go!', 'Java', 'MATLAB', 'CSS'
}

# Items that ARE languages (not software despite name similarity)
IS_ACTUALLY_LANGUAGE = {
    'Emacs Lisp', 'Vim script', 'Hartmann pipelines'  # These are scripting/embedding languages
}

# TRULY popular languages (refined - top 30-40 by actual industry usage 2024-2026)
TRULY_POPULAR = {
    # Tier 1: Most used
    'python', 'javascript', 'typescript', 'java', 'c#', 'c++', 'c',
    'go', 'rust', 'php', 'ruby', 'swift', 'kotlin',
    
    # Tier 2: Very popular
    'sql', 'html', 'css', 'shell', 'bash', 'powershell',
    'r', 'matlab', 'scala', 'perl', 'lua', 'dart',
    
    # Tier 3: Popular in specific domains
    'objective-c', 'haskell', 'clojure', 'elixir', 'erlang', 
    'julia', 'f#', 'groovy', 'visual basic', 'vb.net',
    'assembly', 'fortran', 'cobol', 'lisp', 'scheme', 'prolog', 'ada'
}

# Popular items for other categories
POPULAR_TOOLS = {
    'git', 'docker', 'kubernetes', 'npm', 'webpack', 'vite', 'eslint',
    'prettier', 'jest', 'mocha', 'pytest', 'jenkins', 'github actions',
    'circleci', 'travis ci', 'nginx', 'apache', 'postgresql', 'mysql',
    'mongodb', 'redis', 'elasticsearch', 'kafka', 'rabbitmq',
    'terraform', 'ansible', 'prometheus', 'grafana', 'helm',
    'postman', 'curl', 'jq', 'grep', 'awk', 'sed', 'vim', 'tmux'
}

POPULAR_SOFTWARE = {
    'visual studio', 'vs code', 'vscode', 'visual studio code',
    'intellij', 'pycharm', 'webstorm', 'android studio', 'xcode',
    'eclipse', 'sublime text', 'atom', 'notepad++', 'vim', 'neovim', 'emacs',
    'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
    'unity', 'unreal engine', 'blender', 'docker desktop',
    'slack', 'discord', 'zoom', 'notion', 'obsidian', 'linear', 'jira',
    'github desktop', 'sourcetree', 'gitkraken', 'tower',
    'iterm2', 'windows terminal', 'hyper', 'warp',
    'postman', 'insomnia', 'tableplus', 'dbeaver',
    'spotify', 'vlc', 'obs studio', 'handbrake'
}

POPULAR_FRAMEWORKS = {
    'react', 'vue', 'angular', 'svelte', 'next.js', 'nuxt', 'remix',
    'express', 'fastapi', 'django', 'flask', 'rails', 'laravel', 'spring',
    '.net', 'asp.net', 'node.js', 'deno', 'bun',
    'tailwind', 'bootstrap', 'material ui', 'chakra'
}

POPULAR_AI_ML = {
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
    'opencv', 'hugging face', 'langchain', 'openai', 'anthropic', 'llama',
    'stable diffusion', 'midjourney', 'dall-e', 'gpt', 'chatgpt', 'claude',
    'jupyter', 'colab', 'kaggle'
}

POPULAR_CLOUD = {
    'aws', 'amazon web services', 'azure', 'google cloud', 'gcp',
    'heroku', 'vercel', 'netlify', 'cloudflare', 'digitalocean',
    'firebase', 'supabase', 'planetscale', 'railway', 'render', 'fly.io'
}

def normalize(name):
    return re.sub(r'[^a-z0-9+#.]', '', name.lower())

def is_popular(item):
    name = item.get('name', '').lower()
    normalized = normalize(name)
    category = item.get('category', '')
    
    if category == 'Programming Language':
        for lang in TRULY_POPULAR:
            if normalized == normalize(lang) or name == lang:
                return True
        return False
    
    elif category == 'Tool':
        for tool in POPULAR_TOOLS:
            if normalize(tool) in normalized or tool in name:
                return True
        return False
    
    elif category == 'Software':
        for sw in POPULAR_SOFTWARE:
            if normalize(sw) in normalized or sw in name:
                return True
        return False
    
    elif category == 'Framework':
        for fw in POPULAR_FRAMEWORKS:
            if normalize(fw) in normalized or fw in name:
                return True
        return False
    
    elif category == 'AI/ML':
        for ai in POPULAR_AI_ML:
            if normalize(ai) in normalized or ai in name:
                return True
        return False
    
    elif category == 'Cloud':
        for cloud in POPULAR_CLOUD:
            if normalize(cloud) in normalized or cloud in name:
                return True
        return False
    
    return item.get('popular', False)  # Keep existing for other categories

# Fix misclassified items
print("Fixing misclassifications...")
fixed_count = 0

for item in data:
    name = item.get('name', '')
    cat = item.get('category', '')
    
    # Fix items that should be Programming Language
    if name in SHOULD_BE_LANGUAGE and cat != 'Programming Language':
        print(f"  {name}: {cat} -> Programming Language")
        item['category'] = 'Programming Language'
        fixed_count += 1

print(f"Fixed {fixed_count} misclassified items\n")

# Update popular field
print("Updating popular marking...")
for item in data:
    item['popular'] = is_popular(item)

# Count popular by category
popular_by_cat = {}
for item in data:
    cat = item.get('category', 'Unknown')
    if cat not in popular_by_cat:
        popular_by_cat[cat] = {'total': 0, 'popular': 0}
    popular_by_cat[cat]['total'] += 1
    if item.get('popular'):
        popular_by_cat[cat]['popular'] += 1

print("\nPopular items by category:")
for cat, counts in sorted(popular_by_cat.items()):
    print(f"  {cat}: {counts['popular']}/{counts['total']}")

# Show popular Programming Languages
print("\nPopular Programming Languages:")
pl_popular = [i for i in data if i.get('category') == 'Programming Language' and i.get('popular')]
for item in sorted(pl_popular, key=lambda x: x['name']):
    print(f"  - {item['name']}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✓ Saved data.json")
print(f"Total popular: {sum(1 for i in data if i.get('popular'))}")
