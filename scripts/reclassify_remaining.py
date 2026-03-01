#!/usr/bin/env python3
"""
Comprehensive reclassification of remaining Tool items.
"""

import json

# Load data
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Comprehensive mapping for remaining Tool items
# Format: "name": ("category", "description")
REMAINING_TOOLS = {
    # IDEs / Editors
    "Eclipse Che": ("IDE/Editor", "Cloud and desktop IDE"),
    "Eclipse Foundation": ("IDE/Editor", "Open-source software foundation"),
    "Eclipse PDT": ("IDE/Editor", "PHP Development Tools for Eclipse"),
    "GNOME Builder": ("IDE/Editor", "IDE for GNOME platform"),
    "Eddie": ("IDE/Editor", "Text editor"),
    "Elvis": ("IDE/Editor", "Vi clone text editor"),
    "FeatherPad": ("IDE/Editor", "Lightweight Qt text editor"),
    "Fresh": ("IDE/Editor", "IDE for flat assembler"),
    "Greenfoot": ("IDE/Editor", "Java IDE for education"),
    "HxD": ("IDE/Editor", "Hex editor for Windows"),
    "JBuilder": ("IDE/Editor", "Java IDE by Embarcadero"),
    "JDeveloper": ("IDE/Editor", "Oracle's Java IDE"),
    "JED": ("IDE/Editor", "Programmer's editor using S-Lang"),
    "JOE": ("IDE/Editor", "Joe's Own Editor"),
    "KWrite": ("IDE/Editor", "Simple text editor for KDE"),
    "Kakoune": ("IDE/Editor", "Modal code editor"),
    "Kile": ("IDE/Editor", "LaTeX editor for KDE"),
    "LE": ("IDE/Editor", "Terminal text editor"),
    "Leo": ("IDE/Editor", "Outlining editor for programmers"),
    "Light Table": ("IDE/Editor", "Interactive IDE"),
    "LispWorks": ("IDE/Editor", "Common Lisp development environment"),
    "PSPad": ("IDE/Editor", "Freeware text editor for Windows"),
    "Padre": ("IDE/Editor", "Perl IDE"),
    "Pe": ("IDE/Editor", "Programmer's editor for Haiku"),
    "PyDev": ("IDE/Editor", "Python IDE for Eclipse"),
    "QED": ("IDE/Editor", "Early Unix text editor"),
    "RJ TextEd": ("IDE/Editor", "Full-featured text editor"),
    "SciTE": ("IDE/Editor", "Text editor based on Scintilla"),
    "Scintilla": ("Library", "Code editing component"),
    "SharpDevelop": ("IDE/Editor", "Open-source IDE for .NET"),
    "SimpleText": ("IDE/Editor", "Apple's basic text editor"),
    "Simply Fortran": ("IDE/Editor", "Fortran IDE for Windows"),
    "Smultron": ("IDE/Editor", "Text editor for macOS"),
    "Stevie": ("IDE/Editor", "Vi clone for various systems"),
    "TeXShop": ("IDE/Editor", "LaTeX editor for macOS"),
    "TeXnicCenter": ("IDE/Editor", "LaTeX IDE for Windows"),
    "TextPad": ("IDE/Editor", "Text editor for Windows"),
    "Ulysses": ("IDE/Editor", "Writing app for Mac and iOS"),
    "Understand": ("IDE/Editor", "Static analysis and IDE tool"),
    "WinEdt": ("IDE/Editor", "LaTeX editor for Windows"),
    "WordStar": ("IDE/Editor", "Historic word processor"),
    "eric": ("IDE/Editor", "Python IDE"),
    "ed": ("IDE/Editor", "Standard Unix line editor"),
    "ex": ("IDE/Editor", "Unix line editor"),
    "jGRASP": ("IDE/Editor", "Lightweight Java IDE"),
    "iA Writer": ("IDE/Editor", "Focused writing app"),
    "mg": ("IDE/Editor", "Emacs-like editor"),
    "ne": ("IDE/Editor", "Nice editor for Unix"),
    "pluma": ("IDE/Editor", "Text editor for MATE desktop"),
    "se": ("IDE/Editor", "Screen editor"),
    "Sam": ("IDE/Editor", "Text editor from Plan 9"),
    "ECCE": ("IDE/Editor", "Edinburgh Compatible Context Editor"),
    "EDIX": ("IDE/Editor", "Programmer's editor"),
    "EDLIN": ("IDE/Editor", "DOS line editor"),
    "EDT": ("IDE/Editor", "DEC text editor"),
    "EDT (Univac)": ("IDE/Editor", "Univac text editor"),
    "Epsilon": ("IDE/Editor", "Emacs-like programmer's editor"),
    "TheDraw": ("IDE/Editor", "ANSI art editor"),
    "ACiDDraw": ("Design", "ANSI art editor"),
    "Framework": ("IDE/Editor", "Integrated software suite"),
    "Rational Software Architect (Eclipse IBM)": ("IDE/Editor", "IBM's modeling and development IDE"),
    "Oracle JDeveloper": ("IDE/Editor", "Oracle's Java development IDE"),
    "Powerflasher FDT": ("IDE/Editor", "Flash/ActionScript IDE"),
    "RubyMine (IntelliJ IDEA)": ("IDE/Editor", "Ruby IDE by JetBrains"),
    "VisualWorks": ("IDE/Editor", "Smalltalk development environment"),
    "CodeWarrior": ("IDE/Editor", "IDE for embedded and game development"),
    "C++Builder": ("IDE/Editor", "C++ IDE by Embarcadero"),
    "Dolphin Smalltalk": ("IDE/Editor", "Smalltalk IDE for Windows"),
    "LibertyEiffel": ("IDE/Editor", "Eiffel compiler and tools"),
    "PHPEclipse": ("IDE/Editor", "PHP IDE for Eclipse"),
    "SASM": ("IDE/Editor", "Simple assembler IDE"),
    
    # Version Control
    "Git (software)": ("Version Control", "Distributed version control system"),
    "FusionForge": ("Version Control", "Software forge platform"),
    
    # CMS / Wiki / Blog
    "Dotclear": ("CMS", "Open-source blogging platform"),
    "DSpace": ("CMS", "Digital repository software"),
    "EPrints": ("CMS", "Open-source repository software"),
    "Enonic XP": ("CMS", "Content platform and headless CMS"),
    "Fedora Commons": ("CMS", "Digital asset management"),
    "Jahia": ("CMS", "Digital experience platform"),
    "Jamroom": ("CMS", "Social platform CMS"),
    "MoinMoin": ("CMS", "Wiki engine in Python"),
    "Omeka": ("CMS", "Web publishing for cultural heritage"),
    "OpenACS": ("CMS", "Web application framework"),
    "OpenKM": ("CMS", "Document management system"),
    "OpenWGA": ("CMS", "Web content management platform"),
    "Pimcore": ("CMS", "Enterprise digital platform"),
    "SPIP": ("CMS", "French CMS for publishing"),
    "Telligent Community": ("CMS", "Community platform"),
    "ThinkFree Online": ("CMS", "Online office suite"),
    "WebGUI": ("CMS", "Content management system"),
    "XOOPS": ("CMS", "Content management system"),
    "blosxom": ("CMS", "Lightweight weblog application"),
    "Known": ("CMS", "Social publishing platform"),
    "Nuxeo EP": ("CMS", "Enterprise content platform"),
    "Open Semantic Framework": ("CMS", "Knowledge management platform"),
    "uCoz": ("CMS", "Website builder platform"),
    "IBM Enterprise Content Management": ("CMS", "Enterprise content platform"),
    
    # E-commerce
    "OpenCart": ("CMS", "Open-source e-commerce platform"),
    "Shopware": ("CMS", "E-commerce platform"),
    "Sellerdeck": ("CMS", "E-commerce software"),
    
    # Collaboration / Project Management
    "Axosoft": ("Collaboration", "Scrum project management tool"),
    "BigGantt": ("Collaboration", "Gantt chart for Jira"),
    "Easy Redmine": ("Collaboration", "Project management solution"),
    "FastTrack Schedule": ("Collaboration", "Project scheduling software"),
    "FogBugz": ("Collaboration", "Issue tracking and project management"),
    "Freedcamp": ("Collaboration", "Free project management"),
    "Goalscape": ("Collaboration", "Visual goal management"),
    "Helix ALM": ("Collaboration", "Application lifecycle management"),
    "Huddle": ("Collaboration", "Cloud collaboration platform"),
    "Invoicing": ("Collaboration", "Time and billing software"),
    "LibrePlan": ("Collaboration", "Project planning tool"),
    "LiquidPlanner": ("Collaboration", "Project management software"),
    "Meridian Systems": ("Collaboration", "Project management for construction"),
    "Milestones Professional": ("Collaboration", "Project presentation software"),
    "Mingle": ("Collaboration", "Agile project management"),
    "MyWorkPLAN": ("Collaboration", "ERP for project-based manufacturing"),
    "NetPoint": ("Collaboration", "Project scheduling tool"),
    "Onepager pro": ("Collaboration", "Project reporting software"),
    "Open Workbench": ("Collaboration", "Open-source project management"),
    "Oracle Primavera EPPM": ("Collaboration", "Enterprise project portfolio management"),
    "PHProjekt": ("Collaboration", "Project management software"),
    "Pivotal Tracker": ("Collaboration", "Agile project management tool"),
    "Planisware": ("Collaboration", "Project portfolio management"),
    "Priority Matrix": ("Collaboration", "Priority management tool"),
    "ProjeQtOr": ("Collaboration", "Project management software"),
    "Projektron BCS": ("Collaboration", "Project management software"),
    "Pyrus": ("Collaboration", "Workflow automation platform"),
    "RationalPlan": ("Collaboration", "Project management software"),
    "Scoro": ("Collaboration", "Business management software"),
    "Severa": ("Collaboration", "Professional services automation"),
    "Shortcut Software": ("Collaboration", "Project management for software teams"),
    "Streamtime Software": ("Collaboration", "Agency management software"),
    "Tom's Planner": ("Collaboration", "Online Gantt chart tool"),
    "TrackerSuite.Net": ("Collaboration", "Project tracking software"),
    "Vpmi": ("Collaboration", "Project management software"),
    "Windchill (software)": ("Collaboration", "Product lifecycle management"),
    "Workamajig": ("Collaboration", "Project management for creatives"),
    "Workfront": ("Collaboration", "Work management platform"),
    "Workflow system": ("Collaboration", "Automation of business processes"),
    "Workspace.com": ("Collaboration", "Online collaboration platform"),
    "eGroupWare": ("Collaboration", "Groupware suite"),
    "enQuire": ("Collaboration", "Project management tool"),
    "in-Step BLUE": ("Collaboration", "Project management software"),
    "phpGroupWare": ("Collaboration", "Groupware suite"),
    "intaver Institute": ("Collaboration", "Project risk management"),
    "DynaRoad": ("Collaboration", "Road construction planning"),
    "Copper Project": ("Collaboration", "Project management"),
    "Hall.com": ("Collaboration", "Team collaboration (now Atlassian)"),
    "JotSpot": ("CMS", "Wiki platform (acquired by Google)"),
    "PlanPerfect": ("Collaboration", "Project management software"),
    
    # Domain Registrars / Hosting
    "Dynadot": ("Hosting", "Domain registrar"),
    "Enom": ("Hosting", "Domain registrar and reseller"),
    "Epik": ("Hosting", "Domain registrar"),
    "EURid": ("Hosting", "EU domain registry"),
    "Gandi": ("Hosting", "Domain registrar and hosting"),
    "GMO Internet": ("Hosting", "Internet services company"),
    "Infomaniak": ("Hosting", "Swiss web hosting provider"),
    "JPRS": ("Hosting", "Japan Registry Services"),
    "KISA": ("Hosting", "Korea Internet Security Agency"),
    "NameSilo": ("Hosting", "Domain registrar"),
    "Network Solutions": ("Hosting", "Domain registrar and hosting"),
    "Nominet": ("Hosting", "UK domain registry"),
    "Porkbun": ("Hosting", "Domain registrar"),
    "Register.com": ("Hosting", "Domain registrar"),
    "UK2": ("Hosting", "Web hosting provider"),
    "Verisign": ("Hosting", "Domain registry operator"),
    "Web.com": ("Hosting", "Web services company"),
    "Webcentral": ("Hosting", "Australian web hosting"),
    "ISPConfig": ("Hosting", "Hosting control panel"),
    "Froxlor": ("Hosting", "Server management panel"),
    "Kloxo": ("Hosting", "Web hosting control panel"),
    "i-MSCP": ("Hosting", "Multi-server control panel"),
    "Webmin": ("Hosting", "Unix system administration interface"),
    "Usermin": ("Hosting", "Web-based user interface"),
    
    # Cloud / Platforms
    "PythonAnywhere": ("Cloud", "Python hosting and development platform"),
    "SourceLair": ("Cloud", "Online IDE and development platform"),
    "Online integrated development environment": ("Cloud", "Browser-based development environments"),
    
    # Compilers / Programming Languages / Runtimes
    "GCC": ("Build Tool", "GNU Compiler Collection"),
    "LLVM": ("Build Tool", "Compiler infrastructure"),
    "Free Pascal": ("Programming Language", "Open-source Pascal compiler"),
    "IronPython": ("Programming Language", "Python for .NET"),
    "PascalABC.NET": ("Programming Language", "Pascal for .NET"),
    "QuickBASIC": ("Programming Language", "Microsoft BASIC compiler"),
    "QuickPascal": ("Programming Language", "Microsoft Pascal compiler"),
    "Visual Basic .NET": ("Programming Language", ".NET Visual Basic"),
    "Gambas": ("Programming Language", "BASIC for Linux"),
    "GLBasic": ("Programming Language", "BASIC for game development"),
    "Liberty BASIC": ("Programming Language", "Windows BASIC"),
    "FutureBASIC": ("Programming Language", "BASIC for Macintosh"),
    "SdlBasic": ("Programming Language", "Cross-platform BASIC"),
    "C++ compiler": ("Build Tool", "Compiler for C++"),
    "GAS": ("Build Tool", "GNU Assembler"),
    "OpenWatcom": ("Build Tool", "Open-source C/C++ compiler"),
    "RemObjects Software": ("Programming Language", "Cross-platform development tools"),
    "Apex (Salesforce.com, Inc)": ("Programming Language", "Salesforce proprietary language"),
    "BON": ("Programming Language", "Business Object Notation"),
    "Lucee": ("Programming Language", "CFML application server"),
    "Railo": ("Programming Language", "CFML application server"),
    "Mono": ("Runtime", ".NET runtime for cross-platform"),
    "generic JVM": ("Runtime", "Java Virtual Machine implementations"),
    "Wine": ("Runtime", "Windows compatibility layer for Unix"),
    "Toolchain": ("Build Tool", "Set of programming tools"),
    
    # Libraries / Frameworks
    "FastCGI": ("Library", "Protocol for web server interfaces"),
    "FreeMarker": ("Library", "Java template engine"),
    "Socket.io": ("Library", "Real-time bidirectional event-based communication"),
    "Tkinter": ("Library", "Python GUI toolkit"),
    "PyQt": ("Library", "Python bindings for Qt"),
    "Qt5": ("Library", "Cross-platform application framework"),
    "Java Swing": ("Library", "Java GUI widget toolkit"),
    "SWT": ("Library", "Standard Widget Toolkit for Java"),
    "WPF": ("Library", "Windows Presentation Foundation"),
    "wxWidget": ("Library", "Cross-platform GUI library"),
    "GTK#": ("Library", "GTK bindings for .NET"),
    "Widget toolkit": ("Library", "GUI component libraries"),
    "GNUstep": ("Library", "OpenStep implementation"),
    "NeXTSTEP": ("Operating System", "Object-oriented operating system"),
    "Smarty": ("Library", "PHP template engine"),
    "ESS extension": ("Library", "Emacs Speaks Statistics"),
    "Julia extension": ("Library", "Julia language extension for VS Code"),
    "mod_perl": ("Library", "Perl interpreter for Apache"),
    
    # Design Tools
    "Figma": ("Design", "Collaborative UI design tool"),
    "GeoGebra": ("Design", "Interactive geometry and algebra"),
    "Lapis": ("Design", "Text selection and editing tool"),
    "FIGlet": ("Design", "ASCII art text generator"),
    
    # Analytics / BI
    "SAP BusinessObjects": ("Analytics", "Business intelligence suite"),
    
    # Databases
    "Percona Server": ("Database", "MySQL fork with performance improvements"),
    "Sleepycat": ("Database", "Berkeley DB developer (Oracle)"),
    
    # Operating Systems / Desktop Environments
    "LXDE": ("Operating System", "Lightweight X11 desktop environment"),
    "MATE": ("Operating System", "GNOME 2 fork desktop environment"),
    "Maemo": ("Operating System", "Mobile Linux distribution"),
    "OpenIndiana": ("Operating System", "Illumos distribution"),
    "OpenVMS": ("Operating System", "Multi-user operating system"),
    "Symbian": ("Operating System", "Mobile operating system"),
    "BS2000": ("Operating System", "Fujitsu mainframe OS"),
    "Unix": ("Operating System", "Multi-user operating system family"),
    "TOPS-10": ("Operating System", "DEC PDP-10 operating system"),
    "TOPS-20": ("Operating System", "DEC PDP-10 operating system"),
    "System Software 6": ("Operating System", "Classic Mac OS version"),
    
    # Hardware
    "PDP-1": ("Hardware", "DEC minicomputer"),
    "PDP-11s": ("Hardware", "DEC minicomputer series"),
    "ZX81": ("Hardware", "Sinclair home computer"),
    "Fujitsu": ("Hardware", "Japanese IT company"),
    "Unisys": ("Hardware", "IT services and software company"),
    
    # Business / ERP
    "SAP Business ByDesign": ("Business", "Cloud ERP solution"),
    "FinancialForce.com": ("Business", "Cloud ERP on Salesforce"),
    "Quantrix Financial Modeler": ("Business", "Financial modeling software"),
    
    # Documentation / Standards / Misc
    "POSIX": ("Documentation", "Portable Operating System Interface standard"),
    "ISBN": ("Documentation", "International Standard Book Number"),
    "Unicode": ("Documentation", "Character encoding standard"),
    "OWL": ("Documentation", "Web Ontology Language"),
    "RDF": ("Documentation", "Resource Description Framework"),
    "BSL 1.1": ("Documentation", "Business Source License"),
    "EPL": ("Documentation", "Eclipse Public License"),
    "EUPL": ("Documentation", "European Union Public License"),
    "GNU": ("Documentation", "GNU Project and licenses"),
    "GNU linking exception": ("Documentation", "GPL linking exception"),
    "PSFL": ("Documentation", "Python Software Foundation License"),
    "Permissive": ("Documentation", "Permissive software licenses"),
    "Open core": ("Documentation", "Open-core business model"),
    "Open source": ("Documentation", "Open-source software concept"),
    "Free and open-source": ("Documentation", "FOSS software concept"),
    "free": ("Documentation", "Free software concept"),
    "proprietary": ("Documentation", "Proprietary software concept"),
    "commercial": ("Documentation", "Commercial software licensing"),
    "source code": ("Documentation", "Programming source code"),
    "pair programming": ("Documentation", "Collaborative programming practice"),
    "Kanban (development)": ("Documentation", "Agile development methodology"),
    "UML class diagramming": ("Documentation", "Unified Modeling Language"),
    "syntax highlighting": ("Documentation", "Code display feature"),
    "VCS Support": ("Documentation", "Version control system support"),
    "Web application": ("Documentation", "Application accessed via web browser"),
    "Web content lifecycle": ("Documentation", "Content management process"),
    "Web server": ("Backend", "Server software for web content"),
    "Webmaster": ("Documentation", "Website administrator role"),
    "Website governance": ("Documentation", "Website management policies"),
    "graphical user interface": ("Documentation", "GUI concept"),
    "Integrated development environment": ("Documentation", "IDE software category"),
    "killer application": ("Documentation", "Highly successful application"),
    "selection": ("Documentation", "Text selection in editors"),
    "talk page": ("Documentation", "Wikipedia discussion page"),
    "the original": ("Documentation", "Reference to original source"),
    "inline citations": ("Documentation", "Citation format"),
    "reliable": ("Documentation", "Source reliability concept"),
    "doi": ("Documentation", "Digital Object Identifier"),
    "comparison": ("Documentation", "Comparative analysis"),
    "citation needed": ("Documentation", "Wikipedia citation marker"),
    "clarification needed": ("Documentation", "Wikipedia clarification marker"),
    "dead link": ("Documentation", "Broken hyperlink"),
    "examples provided by the user": ("Documentation", "User-contributed examples"),
    "Profiler": ("Debugging", "Performance profiling tool"),
    "Profiling": ("Debugging", "Performance analysis technique"),
    "flame graph": ("Debugging", "Performance visualization"),
    "Valgrind": ("Debugging", "Memory debugging and profiling"),
    "SPARC": ("Documentation", "Scholarly Publishing and Academic Resources Coalition"),
    "INRIA": ("Documentation", "French computer science research institute"),
    "IPM": ("Documentation", "Institute for Research in Fundamental Sciences"),
    "MIT": ("Documentation", "Massachusetts Institute of Technology / MIT License"),
    "Mozilla": ("Documentation", "Mozilla Foundation"),
    "Google Inc.": ("Documentation", "Technology company"),
    "Oracle Corporation": ("Documentation", "Technology company"),
    "Novell": ("Documentation", "Software company"),
    "Rob Pike": ("Documentation", "Computer scientist"),
    "ReadWriteWeb": ("Documentation", "Technology blog"),
    "PC World": ("Documentation", "Technology publication"),
    "PM World Today": ("Documentation", "Project management publication"),
    "Gigaom": ("Documentation", "Technology news site"),
    "Stack Overflow": ("Documentation", "Q&A for programmers"),
    "Unknown Worlds Entertainment": ("Documentation", "Game development studio"),
    "Retail": ("Documentation", "Retail software distribution"),
    
    # Spreadsheets
    "Excel": ("Collaboration", "Microsoft spreadsheet application"),
    "Online spreadsheet": ("Collaboration", "Web-based spreadsheets"),
    "Spreadsheet": ("Collaboration", "Tabular data application"),
    "spreadsheets": ("Collaboration", "Spreadsheet applications"),
    "GNU Oleo": ("Collaboration", "GNU spreadsheet"),
    "KCells": ("Collaboration", "KDE spreadsheet (Calligra Sheets)"),
    "KSpread": ("Collaboration", "KDE spreadsheet"),
    "Lotus Improv": ("Collaboration", "Innovative spreadsheet"),
    "Lotus SmartSuite": ("Collaboration", "Office suite by IBM"),
    "Lotus Symphony": ("Collaboration", "IBM office suite"),
    "Multiplan": ("Collaboration", "Microsoft spreadsheet predecessor"),
    "PlanMaker": ("Collaboration", "SoftMaker spreadsheet"),
    "Pyspread": ("Collaboration", "Python-based spreadsheet"),
    "Quattro Pro": ("Collaboration", "Corel spreadsheet"),
    "Resolver One": ("Collaboration", "Python-based spreadsheet"),
    "Sheetster": ("Collaboration", "Open-source spreadsheet server"),
    "Siag": ("Collaboration", "Spreadsheet application"),
    "SuperCalc": ("Collaboration", "Early PC spreadsheet"),
    "T/Maker": ("Collaboration", "Early spreadsheet/word processor"),
    "VisiCalc": ("Collaboration", "First spreadsheet application"),
    "Wingz": ("Collaboration", "Spreadsheet application"),
    "Zoho Sheet": ("Collaboration", "Online spreadsheet"),
    "The Calligra Suite": ("Collaboration", "KDE office suite"),
    "IBM Lotus Domino": ("Collaboration", "Enterprise collaboration platform"),
    "IBM Lotus Symphony": ("Collaboration", "Free office suite by IBM"),
    "PowerPoint": ("Collaboration", "Microsoft presentation software"),
    
    # PHP-based
    "PHP-Fusion": ("CMS", "PHP content management system"),
    "PHP-Nuke": ("CMS", "PHP web portal system"),
    "phpWebLog": ("CMS", "PHP blogging software"),
    
    # Misc Tools
    "DNN": ("CMS", "DotNetNuke CMS platform"),
    "Flash": ("Library", "Adobe Flash platform"),
    "GUI-baseddesign": ("Design", "GUI design approaches"),
    "HTML5": ("Programming Language", "Latest HTML standard"),
    "JCR": ("API", "Java Content Repository"),
    "Mule (software)": ("API", "Enterprise service bus"),
    "PCBoard": ("Backend", "BBS software"),
    "Peer-to-peer": ("Documentation", "P2P network architecture"),
    "Personalization management system (PMS)": ("CMS", "Content personalization"),
    "SaaS": ("Documentation", "Software-as-a-Service model"),
    "SLIME": ("IDE/Editor", "Superior Lisp Interaction Mode for Emacs"),
    "STOIC": ("Programming Language", "Stack-oriented programming language"),
    "Virtual": ("Hosting", "Virtual hosting concept"),
    "Wing": ("IDE/Editor", "Python IDE by Wingware"),
    "web": ("Documentation", "World Wide Web"),
    "Other platforms": ("Documentation", "Alternative platform support"),
    "IBM mainframes": ("Hardware", "IBM mainframe computers"),
}

# Bad descriptions to replace
BAD_DESCRIPTIONS = {
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
    "Stream editor for text transformation",
    "Functional shell language",
    "Functional programming family",
    "Functional package language",
    "Cloud-native integration language",
    "Esoteric language",
    "Safe C dialect",
    "Low-level processor instructions",
    "Dynamic language for web development",
}

# Update data
changes = []
for item in data:
    name = item.get('name', '')
    if name in REMAINING_TOOLS:
        new_cat, new_desc = REMAINING_TOOLS[name]
        old_cat = item.get('category', '')
        old_desc = item.get('description', '')
        
        # Only update if category is Tool or description is bad
        if old_cat == 'Tool' or old_desc in BAD_DESCRIPTIONS or old_desc.startswith('[Needs review]'):
            item['category'] = new_cat
            if old_desc in BAD_DESCRIPTIONS or old_desc.startswith('[Needs review]') or not old_desc:
                item['description'] = new_desc
            changes.append({
                'name': name,
                'old_cat': old_cat,
                'new_cat': new_cat,
                'old_desc': old_desc[:50] if old_desc else '',
                'new_desc': new_desc
            })

# Save updated data
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Print summary
print(f"Total changes: {len(changes)}")
print("=" * 80)
for c in changes[:50]:
    print(f"{c['name']}: {c['old_cat']} -> {c['new_cat']}")
if len(changes) > 50:
    print(f"... and {len(changes) - 50} more")

# Count remaining Tool items
remaining = sum(1 for i in data if i.get('category') == 'Tool')
print(f"\nRemaining Tool items: {remaining}")

# Save report
with open('reclassification_remaining_report.json', 'w', encoding='utf-8') as f:
    json.dump(changes, f, indent=2, ensure_ascii=False)

print("\nReport saved to reclassification_remaining_report.json")
