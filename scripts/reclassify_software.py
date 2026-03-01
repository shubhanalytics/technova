"""
Reclassify items from 'Programming Language' to 'Software' using smart heuristics.

Approach:
1. Known software products (curated list) -> Software
2. Items with commercial product URLs (not docs/wiki/github) -> Software
3. Everything else stays as Programming Language
"""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA_JSON = ROOT / 'data.json'
DATA_MIN = ROOT / 'data.min.json'

# Curated list of known software products (not programming languages)
KNOWN_SOFTWARE = {
    'aimms', 'agilent vee', 'rational synergy', 'accent', 'app inventor',
    'labview', 'matlab', 'simulink', 'mathematica', 'wolfram', 'maple',
    'sas', 'spss', 'stata', 'minitab', 'excel', 'powerbi', 'tableau',
    'alteryx', 'knime', 'rapidminer', 'dataiku', 'databricks', 'snowflake',
    'salesforce', 'servicenow', 'sap', 'oracle', 'peoplesoft', 'workday',
    'autodesk', 'solidworks', 'catia', 'ansys', 'abaqus', 'comsol',
    'unity', 'unreal engine', 'godot', 'gamemaker', 'rpg maker',
    'adobe', 'photoshop', 'illustrator', 'premiere', 'after effects',
    'visual studio', 'eclipse', 'intellij', 'pycharm', 'webstorm',
    'xcode', 'android studio', 'qt creator', 'netbeans',
    'jenkins', 'github actions', 'gitlab ci', 'circleci', 'travis',
    'docker', 'kubernetes', 'terraform', 'ansible', 'puppet', 'chef',
    'splunk', 'elastic', 'grafana', 'prometheus', 'datadog', 'new relic',
    'jira', 'confluence', 'trello', 'asana', 'notion', 'monday',
    'slack', 'teams', 'zoom', 'discord',
}

# URL patterns that indicate software products (commercial sites)
SOFTWARE_URL_PATTERNS = [
    r'\.com/product',
    r'\.com/solutions',
    r'\.com/platform',
    r'\.com/software',
    r'\.com/enterprise',
    r'/pricing',
    r'/download',
    r'www\.(mathworks|wolfram|sas|ibm|oracle|sap|salesforce|microsoft)\.com',
    r'\.keysight\.com',  # Agilent VEE
    r'\.aimms\.com',
    r'\.ni\.com',  # National Instruments / LabVIEW
]

# URL patterns that indicate actual programming languages
LANGUAGE_URL_PATTERNS = [
    r'wikipedia\.org',
    r'github\.com/[^/]+$',  # GitHub org pages
    r'github\.io',
    r'\.readthedocs\.',
    r'docs\.',
    r'/spec/',
    r'/reference/',
    r'/manual/',
    r'rosettacode\.org',
    r'\.edu/',
    r'csail\.mit\.edu',
    r'haskell\.org',
    r'rust-lang\.org',
    r'python\.org',
    r'ruby-lang\.org',
    r'golang\.org',
    r'scala-lang\.org',
    r'erlang\.org',
    r'elixir-lang\.org',
    r'clojure\.org',
    r'racket-lang\.org',
    r'ocaml\.org',
    r'fsharp\.org',
    r'purescript\.org',
    r'crystal-lang\.org',
    r'nim-lang\.org',
    r'ziglang\.org',
    r'vlang\.io',
    r'odin-lang\.org',
]

def normalize_name(name: str) -> str:
    """Normalize name for matching."""
    return re.sub(r'[^a-z0-9\s]', '', name.lower()).strip()

def is_known_software(name: str) -> bool:
    """Check if name matches known software products."""
    normalized = normalize_name(name)
    for sw in KNOWN_SOFTWARE:
        if sw in normalized or normalized in sw:
            return True
    return False

def url_looks_like_software(url: str) -> bool:
    """Check if URL pattern suggests a software product."""
    if not url:
        return False
    url_lower = url.lower()
    for pattern in SOFTWARE_URL_PATTERNS:
        if re.search(pattern, url_lower):
            return True
    return False

def url_looks_like_language(url: str) -> bool:
    """Check if URL pattern suggests a programming language."""
    if not url:
        return False
    url_lower = url.lower()
    for pattern in LANGUAGE_URL_PATTERNS:
        if re.search(pattern, url_lower):
            return True
    return False

def should_be_software(item: dict) -> bool:
    """Determine if an item should be classified as Software."""
    name = item.get('name', '')
    url = item.get('url', '')
    
    # Known software products
    if is_known_software(name):
        return True
    
    # URL indicates software product
    if url_looks_like_software(url):
        return True
    
    # URL indicates programming language - keep as is
    if url_looks_like_language(url):
        return False
    
    # Commercial .com domain without docs/wiki patterns might be software
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        
        # Skip obvious language sites
        if any(lang in domain for lang in ['lang.org', 'wiki', 'docs', 'github']):
            return False
        
        # Commercial product sites
        if domain.endswith('.com') and not any(x in path for x in ['/wiki', '/doc', '/spec']):
            # Check if it's a dedicated product domain (company name in URL)
            if re.match(r'^www\.[a-z]+\.com/?$', url.lower().rstrip('/')):
                return True
    except Exception:
        pass
    
    return False

def reclassify(items: list) -> tuple[int, list]:
    """Reclassify items and return count and list of changed items."""
    changed = 0
    changed_items = []
    
    for it in items:
        cat = it.get('category')
        if cat != 'Programming Language':
            continue
        
        if should_be_software(it):
            it['category'] = 'Software'
            changed += 1
            changed_items.append(it.get('name', 'Unknown'))
    
    return changed, changed_items

def main():
    if not DATA_JSON.exists():
        print('data.json not found')
        return
    
    items = json.loads(DATA_JSON.read_text(encoding='utf-8'))
    if not isinstance(items, list):
        print('unexpected data.json format')
        return
    
    changed, changed_items = reclassify(items)
    
    if changed:
        DATA_JSON.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding='utf-8')
        try:
            DATA_MIN.write_text(json.dumps(items, separators=(',', ':'), ensure_ascii=False), encoding='utf-8')
        except Exception:
            pass
        
        print(f'Reclassified {changed} items to Software:')
        for name in sorted(changed_items)[:20]:
            print(f'  - {name}')
        if len(changed_items) > 20:
            print(f'  ... and {len(changed_items) - 20} more')
    else:
        print('No items reclassified')

if __name__ == '__main__':
    main()
