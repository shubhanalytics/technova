#!/usr/bin/env python3
"""
Audit categories and fix popular marking
"""
import json
import re

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# TRULY popular programming languages (top 50 by real-world usage)
TRULY_POPULAR_LANGUAGES = {
    'python', 'javascript', 'java', 'c++', 'c#', 'c', 'typescript', 'php', 'ruby',
    'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'lua',
    'haskell', 'clojure', 'elixir', 'erlang', 'f#', 'ocaml', 'julia', 'dart',
    'objective-c', 'assembly', 'sql', 'shell', 'bash', 'powershell', 'groovy',
    'visual basic', 'vb.net', 'cobol', 'fortran', 'lisp', 'scheme', 'prolog',
    'ada', 'pascal', 'delphi', 'abap', 'apex', 'coffeescript', 'actionscript',
    'html', 'css', 'sass', 'less'
}

# Software products (applications, not languages)
KNOWN_SOFTWARE = {
    'visual studio', 'visual studio code', 'vs code', 'vscode', 'intellij',
    'pycharm', 'webstorm', 'phpstorm', 'rider', 'clion', 'goland', 'rubymine',
    'eclipse', 'netbeans', 'xcode', 'android studio', 'atom', 'sublime text',
    'notepad++', 'vim', 'neovim', 'emacs', 'brackets', 'coda', 'textmate',
    'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'bitbucket',
    'jira', 'confluence', 'slack', 'teams', 'discord', 'zoom', 'notion',
    'figma', 'sketch', 'adobe', 'photoshop', 'illustrator', 'premiere',
    'unity', 'unreal engine', 'blender', 'maya', 'cinema 4d', '3ds max',
    'postman', 'insomnia', 'swagger', 'graphql playground',
    'mysql workbench', 'pgadmin', 'mongodb compass', 'redis desktop',
    'datagrip', 'dbeaver', 'sequel pro', 'tableplus', 'azure data studio',
    'terraform', 'ansible', 'puppet', 'chef', 'vagrant', 'virtualbox',
    'vmware', 'parallels', 'hyper-v', 'aws', 'azure', 'google cloud',
    'heroku', 'netlify', 'vercel', 'firebase', 'supabase', 'mongodb atlas',
    'elasticsearch', 'kibana', 'grafana', 'prometheus', 'datadog', 'splunk',
    'new relic', 'sentry', 'rollbar', 'bugsnag', 'logrocket',
    'webpack', 'vite', 'parcel', 'rollup', 'esbuild', 'snowpack',
    'npm', 'yarn', 'pnpm', 'pip', 'conda', 'homebrew', 'chocolatey',
    'git', 'svn', 'mercurial', 'perforce',
    'tableau', 'power bi', 'looker', 'metabase', 'redash', 'superset',
    'jupyter', 'jupyter notebook', 'jupyterlab', 'google colab', 'kaggle',
    'rstudio', 'spyder', 'anaconda', 'miniconda',
}

# Tools/utilities (command-line tools, libraries are NOT software)
KNOWN_TOOLS = {
    'git', 'npm', 'yarn', 'pip', 'cargo', 'maven', 'gradle', 'cmake', 'make',
    'gcc', 'clang', 'llvm', 'gdb', 'valgrind', 'strace', 'ltrace',
    'curl', 'wget', 'ssh', 'scp', 'rsync', 'tar', 'zip', 'gzip',
    'grep', 'sed', 'awk', 'find', 'xargs', 'sort', 'uniq', 'wc',
    'docker', 'kubectl', 'helm', 'terraform', 'ansible', 'packer',
    'nginx', 'apache', 'caddy', 'traefik', 'haproxy', 'envoy',
    'mysql', 'postgresql', 'mongodb', 'redis', 'memcached', 'elasticsearch',
    'rabbitmq', 'kafka', 'zeromq', 'nats', 'pulsar',
    'prometheus', 'grafana', 'jaeger', 'zipkin',
}

def normalize_name(name):
    """Normalize name for comparison"""
    return re.sub(r'[^a-z0-9+#]', '', name.lower())

def is_truly_popular_language(item):
    """Check if this is a truly popular programming language"""
    name = item.get('name', '').lower()
    normalized = normalize_name(name)
    
    for lang in TRULY_POPULAR_LANGUAGES:
        lang_norm = normalize_name(lang)
        if normalized == lang_norm or name == lang:
            return True
    return False

# Audit and fix
print("=" * 60)
print("CATEGORY AUDIT")
print("=" * 60)

# Check each category
categories = {}
for item in data:
    cat = item.get('category', 'Unknown')
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(item)

for cat, items in sorted(categories.items()):
    print(f"\n{cat}: {len(items)} items")

# Find misclassified items
print("\n" + "=" * 60)
print("CHECKING FOR MISCLASSIFIED ITEMS")
print("=" * 60)

misclassified = []

for item in data:
    name = item.get('name', '').lower()
    url = item.get('url', '').lower()
    cat = item.get('category', '')
    
    # Check if a Programming Language is actually software
    if cat == 'Programming Language':
        for sw in KNOWN_SOFTWARE:
            if sw in name:
                misclassified.append({
                    'name': item['name'],
                    'current': cat,
                    'suggested': 'Software',
                    'reason': f'Matches known software: {sw}'
                })
                break
    
    # Check if Tool/Software might be a language
    if cat in ['Tool', 'Software']:
        normalized = normalize_name(name)
        for lang in TRULY_POPULAR_LANGUAGES:
            if normalized == normalize_name(lang) and 'sdk' not in name and 'runtime' not in name:
                misclassified.append({
                    'name': item['name'],
                    'current': cat,
                    'suggested': 'Programming Language',
                    'reason': f'Matches known language: {lang}'
                })
                break

if misclassified:
    print("\nPotentially misclassified items:")
    for m in misclassified:
        print(f"  {m['name']}: {m['current']} -> {m['suggested']} ({m['reason']})")
else:
    print("\nNo obvious misclassifications found.")

# Fix popular marking - only TRULY popular languages
print("\n" + "=" * 60)
print("FIXING POPULAR MARKING")
print("=" * 60)

popular_count_before = sum(1 for i in data if i.get('popular') == True)
print(f"Popular items before: {popular_count_before}")

# Reset popular for Programming Languages, only mark truly popular
pl_popular_before = sum(1 for i in data if i.get('category') == 'Programming Language' and i.get('popular') == True)
print(f"Popular Programming Languages before: {pl_popular_before}")

for item in data:
    if item.get('category') == 'Programming Language':
        item['popular'] = is_truly_popular_language(item)

pl_popular_after = sum(1 for i in data if i.get('category') == 'Programming Language' and i.get('popular') == True)
print(f"Popular Programming Languages after: {pl_popular_after}")

# Show truly popular languages found
truly_popular = [i for i in data if i.get('category') == 'Programming Language' and i.get('popular') == True]
print("\nTruly popular languages:")
for i in sorted(truly_popular, key=lambda x: x['name']):
    print(f"  {i['name']}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✓ Saved data.json")

popular_count_after = sum(1 for i in data if i.get('popular') == True)
print(f"\nTotal popular items: {popular_count_before} -> {popular_count_after}")
