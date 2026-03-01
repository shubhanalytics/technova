"""
Mark popular items and add missing descriptions to data.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_JSON = ROOT / 'data.json'
DATA_MIN = ROOT / 'data.min.json'

# Popular items by category (case-insensitive matching)
POPULAR_ITEMS = {
    'Programming Language': [
        'python', 'javascript', 'typescript', 'java', 'c#', 'c++', 'c',
        'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r',
        'sql', 'bash', 'powershell', 'perl', 'lua', 'dart', 'elixir',
        'haskell', 'clojure', 'f#', 'objective-c', 'matlab', 'julia',
        'assembly', 'fortran', 'cobol', 'lisp', 'scheme', 'erlang',
        'groovy', 'visual basic', 'delphi', 'pascal'
    ],
    'Tool': [
        'git', 'docker', 'kubernetes', 'jenkins', 'github', 'gitlab',
        'vscode', 'visual studio', 'intellij', 'vim', 'neovim', 'emacs',
        'postman', 'insomnia', 'curl', 'wget', 'npm', 'yarn', 'pip',
        'maven', 'gradle', 'webpack', 'vite', 'eslint', 'prettier',
        'jest', 'pytest', 'selenium', 'cypress', 'terraform', 'ansible',
        'prometheus', 'grafana', 'nginx', 'apache', 'redis', 'postgresql',
        'mysql', 'mongodb', 'elasticsearch', 'kafka', 'rabbitmq',
        'slack', 'jira', 'confluence', 'notion', 'figma', 'sketch',
        'chrome devtools', 'firefox', 'safari', 'lighthouse'
    ],
    'Framework': [
        'react', 'angular', 'vue', 'svelte', 'django', 'flask', 'rails',
        'spring', 'laravel', 'express', 'next.js', 'nuxt', 'fastapi',
        'nest.js', 'asp.net', '.net', 'electron', 'react native', 'flutter'
    ],
    'AI/ML': [
        'tensorflow', 'pytorch', 'openai', 'hugging face', 'scikit-learn',
        'anthropic', 'google deepmind', 'meta ai', 'mistral', 'cohere',
        'stability ai', 'mlflow', 'databricks'
    ],
    'Software': [
        'matlab', 'mathematica', 'labview', 'salesforce', 'sap',
        'oracle', 'visual studio', 'unity', 'unreal'
    ],
    'Startup': [],
    'Cloud': [
        'aws', 'azure', 'google cloud', 'gcp', 'digitalocean', 'heroku',
        'vercel', 'netlify', 'cloudflare'
    ],
    'Technology': [],
    'Data': []
}

# Descriptions for common programming languages
DESCRIPTIONS = {
    # Programming Languages
    'python': 'High-level, general-purpose programming language',
    'javascript': 'Dynamic language for web development',
    'typescript': 'Typed superset of JavaScript',
    'java': 'Object-oriented language for enterprise apps',
    'c#': 'Modern object-oriented language by Microsoft',
    'c++': 'High-performance systems programming language',
    'c': 'Low-level systems programming language',
    'go': 'Fast, statically typed language by Google',
    'rust': 'Memory-safe systems programming language',
    'ruby': 'Dynamic, object-oriented scripting language',
    'php': 'Server-side scripting for web development',
    'swift': 'Modern language for Apple platforms',
    'kotlin': 'Modern JVM language for Android',
    'scala': 'Functional and OO language on the JVM',
    'r': 'Statistical computing and graphics language',
    'sql': 'Standard language for relational databases',
    'bash': 'Unix shell and command language',
    'powershell': 'Task automation shell by Microsoft',
    'perl': 'High-level text processing language',
    'lua': 'Lightweight embeddable scripting language',
    'dart': 'Client-optimized language for Flutter',
    'elixir': 'Functional language on the Erlang VM',
    'haskell': 'Purely functional programming language',
    'clojure': 'Functional Lisp dialect on the JVM',
    'f#': 'Functional-first language on .NET',
    'objective-c': 'OO language for Apple legacy apps',
    'matlab': 'Numerical computing environment',
    'julia': 'High-performance scientific computing',
    'assembly': 'Low-level processor instructions',
    'assembly language': 'Low-level processor instructions',
    'fortran': 'Scientific and numerical computing',
    'cobol': 'Business-oriented legacy language',
    'lisp': 'Family of functional programming languages',
    'scheme': 'Minimalist Lisp dialect',
    'erlang': 'Concurrent, fault-tolerant language',
    'groovy': 'Dynamic JVM language for scripting',
    'visual basic': 'Event-driven language by Microsoft',
    'delphi': 'RAD tool for native applications',
    'pascal': 'Procedural programming language',
    'prolog': 'Logic programming language',
    'ada': 'High-integrity systems language',
    'ocaml': 'Functional language with type inference',
    'racket': 'General-purpose Lisp dialect',
    'smalltalk': 'Pure object-oriented language',
    'forth': 'Stack-based programming language',
    'apl': 'Array-oriented language with symbols',
    'coffeescript': 'Language that compiles to JavaScript',
    'actionscript': 'Language for Flash applications',
    'vhdl': 'Hardware description language',
    'verilog': 'Hardware description language',
    'tcl': 'Dynamic scripting language',
    'awk': 'Pattern scanning and processing',
    'sed': 'Stream editor for text transformation',
    'abap': 'SAP enterprise programming language',
    'apex': 'Salesforce proprietary language',
    'solidity': 'Smart contract language for Ethereum',
    'move': 'Resource-oriented blockchain language',
    'zig': 'Low-level systems language',
    'nim': 'Efficient compiled systems language',
    'crystal': 'Ruby-like compiled language',
    'd': 'Systems programming language',
    'v': 'Simple, fast compiled language',
    'raku': 'Expressive multi-paradigm language',
    'red': 'Full-stack programming language',
    'ballerina': 'Cloud-native integration language',
    'chapel': 'Parallel programming language',
    'pony': 'Actor-model compiled language',
    'reason': 'Syntax for OCaml',
    'purescript': 'Strongly-typed functional for JS',
    'elm': 'Functional language for web UIs',
    'idris': 'Dependently typed language',
    'agda': 'Dependently typed proof assistant',
    'coq': 'Proof assistant and language',
    'lean': 'Theorem prover and language',
    'futhark': 'Functional GPU programming',
    'jai': 'Game development language',
    'odin': 'Systems programming language',
    'gleam': 'Type-safe language for Erlang VM',
    'unison': 'Content-addressed language',
    'roc': 'Fast, friendly functional language',
    'mojo': 'Python superset for AI hardware',
    'carbon': 'C++ successor by Google',
    
    # More languages
    '.ql': 'Query language for code analysis',
    'a+': 'Array programming language',
    'abc': 'Interactive programming language',
    'algol': 'Influential algorithmic language',
    'algol 58': 'Early version of ALGOL',
    'algol 60': 'Influential structured language',
    'algol 68': 'Advanced ALGOL variant',
    'alice ml': 'Concurrent functional language',
    'ampl': 'Mathematical programming language',
    'angelscript': 'Game scripting language',
    'applescript': 'macOS automation language',
    'arc': 'Lisp dialect for web apps',
    'arkts': 'TypeScript variant for HarmonyOS',
    'assemblyscript': 'TypeScript to WebAssembly',
    'ats': 'Functional language with proofs',
    'autohotkey': 'Windows automation scripting',
    'autoit': 'Windows GUI automation',
    'autolisp': 'AutoCAD scripting language',
    'basic': 'Beginners all-purpose language',
    'batch file': 'Windows command scripting',
    'bc': 'Arbitrary precision calculator',
    'befunge': 'Esoteric 2D language',
    'beta': 'Object-oriented language',
    'blitzbasic': 'Game development BASIC',
    'boo': 'Pythonic .NET language',
    'brainfuck': 'Minimalist esoteric language',
    'c--': 'Portable assembly language',
    'caml': 'Functional ML dialect',
    'ceylon': 'JVM language by Red Hat',
    'chill': 'Telecom programming language',
    'cilk': 'Parallel programming extension',
    'clean': 'Pure functional language',
    'clips': 'Expert systems language',
    'comega': 'C# with concurrency',
    'curl': 'Web content language',
    'cyclone': 'Safe C dialect',
    'cython': 'C extensions for Python',
    'e': 'Capability-based language',
    'eiffel': 'Object-oriented with Design by Contract',
    'euphoria': 'Simple programming language',
    'factor': 'Stack-based language',
    'fantom': 'Cross-platform JVM language',
    'felix': 'High-performance ML language',
    'fstar': 'ML dialect for verification',
    'gambas': 'BASIC for Linux',
    'gdscript': 'Godot game engine language',
    'gml': 'GameMaker scripting language',
    'golo': 'Lightweight JVM language',
    'hack': 'PHP dialect by Facebook',
    'harbour': 'xBase compiler',
    'haxe': 'Cross-platform language',
    'icon': 'High-level pattern language',
    'inform': 'Interactive fiction language',
    'io': 'Prototype-based language',
    'j': 'Array programming language',
    'jade': 'Agent-oriented language',
    'jasmin': 'JVM assembler',
    'jcl': 'IBM mainframe job control',
    'jolie': 'Service-oriented language',
    'jsonnet': 'Data templating language',
    'k': 'Array programming for finance',
    'korn shell': 'Unix shell language',
    'labview': 'Visual programming for hardware',
    'ladder logic': 'PLC programming language',
    'lasso': 'Web development language',
    'lfe': 'Lisp Flavoured Erlang',
    'limbo': 'Inferno OS language',
    'lingo': 'Director scripting language',
    'logo': 'Educational programming language',
    'logtalk': 'Object-oriented Prolog',
    'lolcode': 'Esoteric meme language',
    'lotusscript': 'Notes/Domino scripting',
    'm4': 'Macro processing language',
    'malbolge': 'Difficult esoteric language',
    'maple': 'Computer algebra system',
    'mathematica': 'Computational knowledge engine',
    'maxscript': '3ds Max scripting',
    'mdx': 'Multidimensional expressions',
    'mercury': 'Logic/functional language',
    'mips assembly': 'MIPS processor assembly',
    'mirah': 'Ruby-like JVM language',
    'ml': 'Functional programming family',
    'modula-2': 'Structured systems language',
    'modula-3': 'Object-oriented Modula',
    'moo': 'MUD object-oriented',
    'moonscript': 'CoffeeScript for Lua',
    'mumps': 'Healthcare data language',
    'mupad': 'Computer algebra system',
    'netrexx': 'REXX for JVM',
    'newlisp': 'Scripting Lisp dialect',
    'nix': 'Functional package language',
    'noop': 'Experimental JVM language',
    'nu': 'Functional shell language',
    'oberon': 'Modula variant',
    'object pascal': 'OO Pascal variant',
    'objective-j': 'JavaScript with Objective-C',
    'occam': 'Concurrent programming language',
    'octave': 'MATLAB-compatible computing',
    'omgrofl': 'Esoteric language',
    'opa': 'Web development language',
    'openedge abl': 'Progress business language',
    'openscad': '3D modeling language',
    'parasail': 'Parallel language',
    'parrot': 'Virtual machine language',
    'pawn': 'Embedded scripting language',
    'pict': 'Concurrent pi-calculus',
    'pike': 'Dynamic programming language',
    'pilot': 'Authoring language',
    'pl/i': 'IBM general-purpose language',
    'pl/sql': 'Oracle procedural SQL',
    'planner': 'AI planning language',
    'pop-11': 'AI research language',
    'postscript': 'Page description language',
    'processing': 'Visual arts programming',
    'progress': 'Business application language',
    'pure': 'Functional language',
    'purebasic': 'Cross-platform BASIC',
    'puredata': 'Visual programming for audio',
    'q': 'Array language for kdb+',
    'qml': 'Qt UI markup language',
    'quorum': 'Evidence-based language',
    'rapira': 'Educational language',
    'ratfor': 'Fortran preprocessor',
    'rc': 'Plan 9 shell',
    'realbasic': 'Cross-platform BASIC',
    'rebol': 'Messaging language',
    'refal': 'Pattern matching language',
    'rexx': 'Scripting language',
    'ring': 'Practical multi-paradigm',
    'robot': 'Automation language',
    'rpg': 'IBM business language',
    's-lang': 'Scripting language',
    'sather': 'Object-oriented language',
    'scilab': 'Numerical computing',
    'scratch': 'Visual educational language',
    'self': 'Prototype-based language',
    'shex': 'Shape expressions language',
    'simula': 'First OO language',
    'sisal': 'Dataflow language',
    'snobol': 'String processing language',
    'sparql': 'RDF query language',
    'squeak': 'Smalltalk implementation',
    'squirrel': 'Game scripting language',
    'standard ml': 'ML implementation',
    'starlark': 'Python-like config language',
    'stata': 'Statistical analysis language',
    'supercollider': 'Audio synthesis language',
    't-sql': 'Microsoft SQL extension',
    'tads': 'Interactive fiction language',
    'tea': 'Scripting language',
    'tex': 'Document typesetting system',
    'thrift': 'Service definition language',
    'tikz': 'Graphics language for TeX',
    'turing': 'Educational language',
    'twig': 'PHP templating language',
    'uml': 'Unified modeling language',
    'unrealscript': 'Unreal Engine scripting',
    'vala': 'GNOME programming language',
    'vb.net': '.NET Visual Basic',
    'vbscript': 'Windows scripting language',
    'webassembly': 'Binary instruction format',
    'wasm': 'Binary instruction format',
    'whitespace': 'Esoteric language',
    'wolfram': 'Computational language',
    'x10': 'Parallel programming language',
    'xbase': 'dBASE family language',
    'xc': 'Concurrent systems language',
    'xojo': 'Cross-platform BASIC IDE',
    'xquery': 'XML query language',
    'xslt': 'XML transformation language',
    'yacc': 'Parser generator',
    'yaml': 'Data serialization language',
    'yorick': 'Scientific computing language',
    'z': 'Formal specification language',
    'zsh': 'Unix shell language',
}

def normalize_name(name: str) -> str:
    """Normalize name for matching."""
    return re.sub(r'[^a-z0-9#+.\s]', '', name.lower()).strip()

def is_popular(name: str, category: str) -> bool:
    """Check if item should be marked as popular."""
    normalized = normalize_name(name)
    popular_list = POPULAR_ITEMS.get(category, [])
    
    for popular in popular_list:
        pop_norm = normalize_name(popular)
        if pop_norm in normalized or normalized in pop_norm:
            return True
        # Check if first word matches
        if normalized.split()[0] == pop_norm.split()[0]:
            return True
    
    return False

def get_description(name: str, existing: str) -> str:
    """Get description for an item, using existing if available."""
    if existing and existing.strip():
        return existing
    
    normalized = normalize_name(name)
    
    # Try exact match
    if normalized in DESCRIPTIONS:
        return DESCRIPTIONS[normalized]
    
    # Try first word match
    first_word = normalized.split()[0] if normalized else ''
    if first_word in DESCRIPTIONS:
        return DESCRIPTIONS[first_word]
    
    # Try partial match
    for key, desc in DESCRIPTIONS.items():
        if key in normalized or normalized in key:
            return desc
    
    return ''

def main():
    if not DATA_JSON.exists():
        print('data.json not found')
        return
    
    items = json.loads(DATA_JSON.read_text(encoding='utf-8'))
    if not isinstance(items, list):
        print('unexpected data.json format')
        return
    
    popular_count = 0
    desc_count = 0
    
    for item in items:
        name = item.get('name', '')
        category = item.get('category', '')
        existing_desc = item.get('description', '')
        
        # Mark as popular
        if is_popular(name, category):
            item['popular'] = True
            popular_count += 1
        else:
            item['popular'] = False
        
        # Add description if missing
        new_desc = get_description(name, existing_desc)
        if new_desc and new_desc != existing_desc:
            item['description'] = new_desc
            desc_count += 1
    
    # Save
    DATA_JSON.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding='utf-8')
    
    try:
        DATA_MIN.write_text(json.dumps(items, separators=(',', ':'), ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass
    
    print(f'Marked {popular_count} items as popular')
    print(f'Added {desc_count} descriptions')
    
    # Show stats by category
    from collections import defaultdict
    stats = defaultdict(lambda: {'popular': 0, 'total': 0})
    for item in items:
        cat = item.get('category', 'Other')
        stats[cat]['total'] += 1
        if item.get('popular'):
            stats[cat]['popular'] += 1
    
    print('\nPopular items by category:')
    for cat, s in sorted(stats.items()):
        print(f'  {cat}: {s["popular"]}/{s["total"]}')

if __name__ == '__main__':
    main()
