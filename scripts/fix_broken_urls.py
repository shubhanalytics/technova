#!/usr/bin/env python3
"""
Fix URLs based on the url_check_report.json results.
- Remove defunct/historical entries
- Fix broken URLs with known alternatives
- Update redirects to new domains
"""

import json

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('url_check_report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

# Items to remove (defunct/historical/dead projects)
items_to_remove = {
    # Historical programming languages with dead links
    "A+ (A plus)", "APT", "COMTRAN", "Cybil", "Dog", "ESPOL", "ELAN",
    "Euclid", "Generational", "FLOW-MATIC (B0)", "GRASS", "Janus (concurrent constraint programming language)",
    "Karel", "Legoscript", "JEAN", "Mouse", "Not Quite C", "NWScript",
    "Chronological", "esoteric programming languages", "GOM", "MIMIC",
    "Napier88", "Cryptol", "Cayenne (Lennart Augustsson)", "Etoys",
    "Clipper", "Algebraic Logic Functional programming language",
    "DATATRIEVE", "Magik", "Maude system", "MPD", "Model 204",
    "bc (basic calculator)", "CMS EXEC", "EusLisp Robot Programming Language",
    "ObjectLOGO", "ProSet", "REBOL", "Visual Prolog", "Self", "Strongtalk",
    "TIE", "YQL", "XL", "XSB", "Z Shell", "ZOPL",
    # Dead collaboration/project management tools
    "project management software", "Tom's Planner", "Pivotal Tracker",
    "Framework", "Widget toolkit", "Appcelerator", "ACiDDraw",
    "Nintendo Wii", "Atari ST",
    # Concept entries that shouldn't be product listings
    "citation needed", "reliable", "SaaS", "pair programming",
    "operating systems", "Debugger", "Profiling", "Profiler", "Code refactoring",
    "registrars", "Code coverage", "domain-specific languages",
    "Free and open-source", "Novell", "UML class diagramming",
    "Web application", "executable",
}

# URL fixes (broken -> working)
url_fixes = {
    "OpenAI": {"url": "https://platform.openai.com/"},
    "Meta AI": {"url": "https://www.meta.ai/"},
    "Linode": {"url": "https://www.akamai.com/solutions/linode", "description": "Cloud hosting by Akamai (formerly Linode)"},
    "Ada": {"url": "https://ada-lang.io/"},
    "AutoHotkey": {"url": "https://github.com/AutoHotkey/AutoHotkey"},
    "Clarion": {"url": "https://clarionsharp.com/"},
    "Lasso": {"url": "https://en.wikipedia.org/wiki/Lasso_(programming_language)"},
    "MATLAB": {"url": "https://www.mathworks.com/"},
    "Maxima": {"url": "https://wxmaxima-developers.github.io/wxmaxima/"},
    "NewLISP": {"url": "https://github.com/kosh04/newlisp"},
    "Bolt (CMS)": {"url": "https://bolt.cm/"},
    "C1 CMS": {"url": "https://github.com/Orckestra"},
    "Height": {"url": "https://height.app/"},  # SSL fix
    "LXDE": {"url": "https://wiki.lxde.org/en/Main_Page"},
    "ColdFusion": {"url": "https://www.adobe.com/products/coldfusion.html"},
    "Dylan": {"url": "https://github.com/opendylan/"},
    "WebXR": {"url": "https://immersiveweb.dev/"},
    "Mortran": {"url": "https://en.wikipedia.org/wiki/Mortran"},
    "SiMPLE": {"remove": True},
    "XOTcl": {"url": "https://wiki.tcl-lang.org/page/XOTcl"},
    "Geeklog": {"url": "https://github.com/Geeklog-Core/geeklog"},
    "DSpace": {"url": "https://dspace.lyrasis.org/"},
    "Workfront": {"url": "https://www.workfront.com/"},
}

# Redirect fixes (update to new domains)
redirect_fixes = {
    "Cohere": {"url": "https://cohere.com/"},
    "Google DeepMind / Google AI": {"url": "https://deepmind.google/"},
    "Vercel AI SDK": {"url": "https://ai-sdk.dev/"},
    "Ollama": {"url": "https://ollama.com/"},
    "JAX": {"url": "https://docs.jax.dev/en/latest/"},
    "Codeium": {"url": "https://windsurf.com/", "name": "Windsurf (Codeium)"},
    "Microsoft Power BI": {"url": "https://www.microsoft.com/en-us/power-platform/products/power-bi/"},
    "MicroStrategy": {"url": "https://www.strategy.com/software", "name": "Strategy (MicroStrategy)"},
    "Segment": {"url": "https://www.twilio.com/en-us/segment"},
    "Google Data Studio": {"url": "https://lookerstudio.google.com/", "name": "Looker Studio"},
    "Ory": {"url": "https://www.ory.com/"},
    "Vite": {"url": "https://vite.dev/"},
    "Turbopack": {"url": "https://nextjs.org/docs/app/api-reference/turbopack"},
    "Turborepo": {"url": "https://turborepo.dev/"},
    "Alfresco": {"url": "https://www.hyland.com/en/solutions/products/alfresco-platform"},
    "Cloud CMS": {"url": "https://gitana.io"},
    "Episerver CMS": {"url": "https://www.optimizely.com/", "name": "Optimizely (Episerver)"},
    "Telligent Community": {"url": "https://www.verint.com/"},
    "Neon": {"url": "https://neon.com/"},
    "Railway": {"url": "https://railway.com/"},
    "TimescaleDB": {"url": "https://www.tigerdata.com/", "name": "TigerData (TimescaleDB)"},
    "QuestDB": {"url": "https://questdb.com/"},
    "ArangoDB": {"url": "https://arango.ai"},
    "EdgeDB": {"url": "https://www.geldata.com/", "name": "Gel (EdgeDB)"},
    "InVision": {"url": "https://miro.com/", "description": "Collaborative design platform (acquired InVision)"},
    "Ansible": {"url": "https://www.redhat.com/en/technologies/management/ansible"},
    "Terraform": {"url": "https://developer.hashicorp.com/terraform"},
    "Consul": {"url": "https://developer.hashicorp.com/consul"},
    "Packer": {"url": "https://developer.hashicorp.com/packer"},
    "Vagrant": {"url": "https://developer.hashicorp.com/vagrant"},
    "SparkPost": {"url": "https://bird.com/developer/email-api"},
    "SendGrid": {"url": "https://www.twilio.com/en-us/sendgrid"},
    "Buttondown": {"url": "https://buttondown.com/"},
    "React": {"url": "https://react.dev/"},
    "Angular": {"url": "https://angular.dev/"},
    "Glitch": {"url": "https://blog.glitch.com/"},
    "Platform.sh": {"url": "https://upsun.com/", "name": "Upsun (Platform.sh)"},
    "Atom": {"url": "https://github.blog/news-insights/product-news/sunsetting-atom/", "description": "Discontinued code editor (open-sourced, archived)"},
    "Cloud9 IDE": {"url": "https://aws.amazon.com/cloud9/"},
    "Eclipse Che": {"url": "https://eclipse.dev/che/"},
    "Komodo IDE": {"url": "https://docs.activestate.com/komodo/12/"},
    "Cursor": {"url": "https://cursor.com/"},
    "Gitpod": {"url": "https://ona.com/", "name": "Ona (Gitpod)"},
    "Lapce": {"url": "https://lap.dev/lapce/"},
    "Framer Motion": {"url": "https://motion.dev", "name": "Motion (Framer Motion)"},
    "AppDynamics": {"url": "https://www.splunk.com/en_us/products/appdynamics.html"},
    "HashiCorp Vault": {"url": "https://developer.hashicorp.com/vault"},
    "Vault": {"url": "https://developer.hashicorp.com/vault"},
    "SonarQube": {"url": "https://www.sonarsource.com/products/sonarqube/"},
    "SonarCloud": {"url": "https://www.sonarsource.com/products/sonarqube/cloud/"},
    "Go": {"url": "https://go.dev/"},
    "Go!": {"url": "https://go.dev/", "description": "Concurrent programming language from Google"},
    "Braintree": {"url": "https://www.paypal.com/us/braintree"},
    "Orama": {"url": "https://orama.com/"},
    "Zinc": {"url": "https://openobserve.ai", "name": "OpenObserve (Zinc)"},
    "LambdaTest": {"url": "https://www.testmuai.com/", "name": "TestMu (LambdaTest)"},
    "GitLab": {"url": "https://about.gitlab.com/"},
    "Gitea": {"url": "https://about.gitea.com/"},
    "GitHub Desktop": {"url": "https://github.com/apps/desktop"},
    "Read the Docs": {"url": "https://about.readthedocs.com/"},
    "Numbers": {"url": "https://www.apple.com/numbers/"},
    "Zoom": {"url": "https://www.zoom.com"},
    "Google Meet": {"url": "https://workspace.google.com/products/meet/"},
    "Google Drive": {"url": "https://workspace.google.com/products/drive/"},
    "Power Automate": {"url": "https://www.microsoft.com/en-us/power-platform/products/power-automate/"},
    "Power Apps": {"url": "https://www.microsoft.com/en-us/power-platform/products/power-apps/"},
    "Waypoint": {"url": "https://developer.hashicorp.com/waypoint"},
}

# Process data
removed_count = 0
fixed_count = 0
redirect_count = 0
new_data = []

for item in data:
    name = item.get('name', '')
    
    # Check if should be removed
    if name in items_to_remove:
        print(f"  Removing: {name}")
        removed_count += 1
        continue
    
    # Check for URL fixes (broken)
    if name in url_fixes:
        fixes = url_fixes[name]
        if fixes.get('remove'):
            print(f"  Removing: {name}")
            removed_count += 1
            continue
        changes = []
        for key in ['url', 'description', 'name']:
            if key in fixes:
                item[key] = fixes[key]
                changes.append(key)
        if changes:
            print(f"  Fixed broken: {name} ({', '.join(changes)})")
            fixed_count += 1
    
    # Check for redirect fixes
    elif name in redirect_fixes:
        fixes = redirect_fixes[name]
        changes = []
        for key in ['url', 'description', 'name']:
            if key in fixes:
                item[key] = fixes[key]
                changes.append(key)
        if changes:
            print(f"  Updated redirect: {name} ({', '.join(changes)})")
            redirect_count += 1
    
    new_data.append(item)

print(f"\n{'='*60}")
print(f"✅ Removed {removed_count} defunct/concept entries")
print(f"✅ Fixed {fixed_count} broken URLs")
print(f"✅ Updated {redirect_count} redirects to new domains")
print(f"📊 Total entries: {len(data)} -> {len(new_data)}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print("\n✅ Saved to data.json")
