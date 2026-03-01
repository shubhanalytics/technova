#!/usr/bin/env python3
"""Add missing important tools to data.json"""

import json

NEW_TOOLS = [
    # Data Science & ML
    {"name": "Jupyter Notebook", "description": "Open-source web application for creating and sharing documents with live code, equations, and visualizations", "url": "https://jupyter.org/", "category": "Data Science", "popular": True},
    {"name": "JupyterLab", "description": "Next-generation web-based interface for Project Jupyter with flexible building blocks", "url": "https://jupyterlab.readthedocs.io/", "category": "Data Science", "popular": True},
    {"name": "SciPy", "description": "Python library for scientific and technical computing with modules for optimization, integration, and statistics", "url": "https://scipy.org/", "category": "Data Science", "popular": True},
    {"name": "Bokeh", "description": "Interactive visualization library for modern web browsers with elegant graphics", "url": "https://bokeh.org/", "category": "Data Visualization"},
    {"name": "Altair", "description": "Declarative statistical visualization library for Python based on Vega-Lite", "url": "https://altair-viz.github.io/", "category": "Data Visualization"},
    {"name": "OpenCV", "description": "Open source computer vision and machine learning software library", "url": "https://opencv.org/", "category": "ML/AI", "popular": True},
    {"name": "Pillow", "description": "Python Imaging Library fork for opening, manipulating, and saving image files", "url": "https://pillow.readthedocs.io/", "category": "Data Science"},
    {"name": "NLTK", "description": "Natural Language Toolkit - platform for building Python programs to work with human language data", "url": "https://www.nltk.org/", "category": "ML/AI", "popular": True},
    {"name": "spaCy", "description": "Industrial-strength Natural Language Processing library with pre-trained pipelines", "url": "https://spacy.io/", "category": "ML/AI", "popular": True},
    {"name": "Hugging Face", "description": "Platform and library for state-of-the-art machine learning models, especially NLP transformers", "url": "https://huggingface.co/", "category": "ML/AI", "popular": True},
    {"name": "Transformers", "description": "State-of-the-art machine learning library for PyTorch, TensorFlow, and JAX", "url": "https://huggingface.co/transformers", "category": "ML/AI", "popular": True},
    {"name": "FastAI", "description": "Deep learning library providing high-level components for fast practical results", "url": "https://www.fast.ai/", "category": "ML/AI"},
    {"name": "XGBoost", "description": "Optimized distributed gradient boosting library for efficient machine learning", "url": "https://xgboost.readthedocs.io/", "category": "ML/AI", "popular": True},
    {"name": "LightGBM", "description": "Fast gradient boosting framework using tree-based learning algorithms", "url": "https://lightgbm.readthedocs.io/", "category": "ML/AI"},
    {"name": "CatBoost", "description": "Gradient boosting library with categorical feature support by Yandex", "url": "https://catboost.ai/", "category": "ML/AI"},
    {"name": "Dask", "description": "Parallel computing library for analytics with task scheduling and DataFrame support", "url": "https://dask.org/", "category": "Data Science"},
    {"name": "Vaex", "description": "High performance Python library for lazy out-of-core DataFrames", "url": "https://vaex.io/", "category": "Data Science"},
    {"name": "Polars", "description": "Blazingly fast DataFrame library implemented in Rust with Python bindings", "url": "https://pola.rs/", "category": "Data Science", "popular": True},
    {"name": "DVC", "description": "Data Version Control - Git for data and machine learning experiments", "url": "https://dvc.org/", "category": "ML/AI"},
    {"name": "Weights & Biases", "description": "MLOps platform for experiment tracking, model management, and collaboration", "url": "https://wandb.ai/", "category": "ML/AI"},
    {"name": "Neptune.ai", "description": "Experiment tracker for ML teams that struggle with debugging models", "url": "https://neptune.ai/", "category": "ML/AI"},
    {"name": "Optuna", "description": "Automatic hyperparameter optimization framework for machine learning", "url": "https://optuna.org/", "category": "ML/AI"},
    {"name": "ONNX", "description": "Open Neural Network Exchange - open format for AI models", "url": "https://onnx.ai/", "category": "ML/AI"},
    {"name": "TensorRT", "description": "NVIDIA SDK for high-performance deep learning inference", "url": "https://developer.nvidia.com/tensorrt", "category": "ML/AI"},
    
    # Big Data & Data Engineering  
    {"name": "Apache Airflow", "description": "Platform to programmatically author, schedule, and monitor workflows", "url": "https://airflow.apache.org/", "category": "Data Engineering", "popular": True},
    {"name": "Apache Hadoop", "description": "Framework for distributed storage and processing of big data using MapReduce", "url": "https://hadoop.apache.org/", "category": "Data Engineering", "popular": True},
    {"name": "Apache Flink", "description": "Stream processing framework for distributed, high-performing, always-available data pipelines", "url": "https://flink.apache.org/", "category": "Data Engineering"},
    {"name": "Apache Beam", "description": "Unified programming model for batch and streaming data processing pipelines", "url": "https://beam.apache.org/", "category": "Data Engineering"},
    {"name": "Apache NiFi", "description": "Data integration tool for automating data flow between systems", "url": "https://nifi.apache.org/", "category": "Data Engineering"},
    {"name": "Dagster", "description": "Cloud-native data pipeline orchestrator for machine learning and analytics", "url": "https://dagster.io/", "category": "Data Engineering"},
    {"name": "Prefect", "description": "Modern workflow orchestration framework for data engineering", "url": "https://www.prefect.io/", "category": "Data Engineering"},
    {"name": "dbt", "description": "Data build tool for transforming data in warehouses using SQL", "url": "https://www.getdbt.com/", "category": "Data Engineering", "popular": True},
    {"name": "Fivetran", "description": "Automated data integration platform for syncing data to warehouses", "url": "https://www.fivetran.com/", "category": "Data Engineering"},
    {"name": "Airbyte", "description": "Open-source data integration platform for ELT pipelines", "url": "https://airbyte.com/", "category": "Data Engineering"},
    {"name": "Snowflake", "description": "Cloud-based data warehouse platform for analytics", "url": "https://www.snowflake.com/", "category": "Data Engineering", "popular": True},
    {"name": "Databricks", "description": "Unified analytics platform for data engineering and data science", "url": "https://www.databricks.com/", "category": "Data Engineering", "popular": True},
    {"name": "Delta Lake", "description": "Open-source storage layer bringing reliability to data lakes", "url": "https://delta.io/", "category": "Data Engineering"},
    {"name": "Apache Iceberg", "description": "Open table format for huge analytic datasets", "url": "https://iceberg.apache.org/", "category": "Data Engineering"},
    {"name": "Apache Hudi", "description": "Data lake platform for incremental data processing", "url": "https://hudi.apache.org/", "category": "Data Engineering"},
    
    # JetBrains IDEs
    {"name": "PHPStorm", "description": "JetBrains IDE for PHP development with deep code understanding", "url": "https://www.jetbrains.com/phpstorm/", "category": "IDE/Editor"},
    {"name": "Rider", "description": "JetBrains cross-platform .NET IDE based on IntelliJ and ReSharper", "url": "https://www.jetbrains.com/rider/", "category": "IDE/Editor"},
    {"name": "GoLand", "description": "JetBrains IDE for Go development with smart code assistance", "url": "https://www.jetbrains.com/go/", "category": "IDE/Editor"},
    {"name": "CLion", "description": "JetBrains cross-platform IDE for C and C++ development", "url": "https://www.jetbrains.com/clion/", "category": "IDE/Editor"},
    {"name": "DataGrip", "description": "JetBrains database IDE supporting multiple databases", "url": "https://www.jetbrains.com/datagrip/", "category": "IDE/Editor"},
    {"name": "RubyMine", "description": "JetBrains IDE for Ruby and Rails development", "url": "https://www.jetbrains.com/ruby/", "category": "IDE/Editor"},
    {"name": "AppCode", "description": "JetBrains IDE for iOS and macOS development", "url": "https://www.jetbrains.com/objc/", "category": "IDE/Editor"},
    
    # Infrastructure & DevOps
    {"name": "Nginx", "description": "High-performance HTTP server, reverse proxy, and load balancer", "url": "https://nginx.org/", "category": "DevOps", "popular": True},
    {"name": "Traefik", "description": "Modern HTTP reverse proxy and load balancer for microservices", "url": "https://traefik.io/", "category": "DevOps"},
    {"name": "Caddy", "description": "Fast, multi-platform web server with automatic HTTPS", "url": "https://caddyserver.com/", "category": "DevOps"},
    {"name": "HAProxy", "description": "Reliable, high performance TCP/HTTP load balancer", "url": "https://www.haproxy.org/", "category": "DevOps"},
    {"name": "Consul", "description": "Service mesh solution providing service discovery and configuration", "url": "https://www.consul.io/", "category": "DevOps"},
    {"name": "Vault", "description": "HashiCorp tool for secrets management and data protection", "url": "https://www.vaultproject.io/", "category": "Security", "popular": True},
    {"name": "Packer", "description": "Tool for creating identical machine images for multiple platforms", "url": "https://www.packer.io/", "category": "DevOps"},
    {"name": "Vagrant", "description": "Tool for building and managing virtual machine environments", "url": "https://www.vagrantup.com/", "category": "DevOps"},
    {"name": "Podman", "description": "Daemonless container engine for developing and running OCI containers", "url": "https://podman.io/", "category": "Container"},
    {"name": "Buildah", "description": "Tool for building OCI container images", "url": "https://buildah.io/", "category": "Container"},
    {"name": "Skopeo", "description": "Tool for working with remote container images and registries", "url": "https://github.com/containers/skopeo", "category": "Container"},
    {"name": "Containerd", "description": "Industry-standard container runtime for managing container lifecycle", "url": "https://containerd.io/", "category": "Container"},
    {"name": "CRI-O", "description": "Lightweight container runtime specifically for Kubernetes", "url": "https://cri-o.io/", "category": "Container"},
    {"name": "k3s", "description": "Lightweight Kubernetes distribution for IoT and edge computing", "url": "https://k3s.io/", "category": "Container"},
    {"name": "k9s", "description": "Terminal UI to interact with Kubernetes clusters", "url": "https://k9scli.io/", "category": "Container"},
    {"name": "Lens", "description": "Kubernetes IDE for managing and debugging clusters", "url": "https://k8slens.dev/", "category": "Container"},
    {"name": "Rancher", "description": "Complete container management platform for Kubernetes", "url": "https://rancher.com/", "category": "Container"},
    {"name": "OpenShift", "description": "Red Hat's enterprise Kubernetes platform", "url": "https://www.redhat.com/en/technologies/cloud-computing/openshift", "category": "Container"},
    
    # Cloud Platforms
    {"name": "Vultr", "description": "Cloud infrastructure provider with SSD cloud servers", "url": "https://www.vultr.com/", "category": "Cloud"},
    {"name": "Hetzner", "description": "European cloud hosting and dedicated server provider", "url": "https://www.hetzner.com/", "category": "Cloud"},
    {"name": "Fly.io", "description": "Platform for running full-stack apps and databases close to users", "url": "https://fly.io/", "category": "Cloud"},
    {"name": "Railway", "description": "Platform for deploying infrastructure primitives", "url": "https://railway.app/", "category": "Cloud"},
    {"name": "Render", "description": "Unified cloud to build and run apps and websites", "url": "https://render.com/", "category": "Cloud"},
    {"name": "PlanetScale", "description": "Serverless MySQL database platform with branching", "url": "https://planetscale.com/", "category": "Database"},
    {"name": "Neon", "description": "Serverless Postgres with branching and bottomless storage", "url": "https://neon.tech/", "category": "Database"},
    {"name": "Supabase", "description": "Open source Firebase alternative with Postgres database", "url": "https://supabase.com/", "category": "Backend", "popular": True},
    {"name": "Appwrite", "description": "Open-source backend server for web and mobile developers", "url": "https://appwrite.io/", "category": "Backend"},
    
    # Testing & Quality
    {"name": "Playwright", "description": "End-to-end testing framework for modern web apps by Microsoft", "url": "https://playwright.dev/", "category": "Testing", "popular": True},
    {"name": "Vitest", "description": "Blazing fast unit test framework powered by Vite", "url": "https://vitest.dev/", "category": "Testing", "popular": True},
    {"name": "Storybook", "description": "Frontend workshop for building UI components and pages in isolation", "url": "https://storybook.js.org/", "category": "Testing", "popular": True},
    {"name": "Chromatic", "description": "Visual testing and review platform for Storybook", "url": "https://www.chromatic.com/", "category": "Testing"},
    {"name": "Locust", "description": "Open source load testing tool written in Python", "url": "https://locust.io/", "category": "Testing"},
    {"name": "k6", "description": "Modern load testing tool for developers and testers", "url": "https://k6.io/", "category": "Testing"},
    {"name": "Artillery", "description": "Modern load testing and smoke testing for developers", "url": "https://www.artillery.io/", "category": "Testing"},
    {"name": "Gatling", "description": "Load testing tool for analyzing and measuring performance", "url": "https://gatling.io/", "category": "Testing"},
    {"name": "SonarQube", "description": "Platform for continuous inspection of code quality", "url": "https://www.sonarqube.org/", "category": "Code Quality", "popular": True},
    {"name": "SonarCloud", "description": "Cloud-based code analysis service for clean code", "url": "https://sonarcloud.io/", "category": "Code Quality"},
    
    # Security
    {"name": "OWASP ZAP", "description": "Open source web application security scanner", "url": "https://www.zaproxy.org/", "category": "Security"},
    {"name": "Burp Suite", "description": "Web security testing toolkit for penetration testing", "url": "https://portswigger.net/burp", "category": "Security"},
    {"name": "Nmap", "description": "Network discovery and security auditing utility", "url": "https://nmap.org/", "category": "Security"},
    {"name": "Wireshark", "description": "Network protocol analyzer for troubleshooting and analysis", "url": "https://www.wireshark.org/", "category": "Security"},
    {"name": "Trivy", "description": "Comprehensive security scanner for containers and other artifacts", "url": "https://trivy.dev/", "category": "Security"},
    {"name": "Snyk", "description": "Developer security platform for finding and fixing vulnerabilities", "url": "https://snyk.io/", "category": "Security", "popular": True},
    {"name": "Semgrep", "description": "Lightweight static analysis tool for finding bugs and vulnerabilities", "url": "https://semgrep.dev/", "category": "Security"},
    {"name": "Checkov", "description": "Static code analysis tool for infrastructure as code", "url": "https://www.checkov.io/", "category": "Security"},
    
    # Documentation & API
    {"name": "Swagger", "description": "API development tools for designing, building, and documenting APIs", "url": "https://swagger.io/", "category": "API", "popular": True},
    {"name": "OpenAPI", "description": "Specification for describing RESTful APIs", "url": "https://www.openapis.org/", "category": "API"},
    {"name": "Redoc", "description": "OpenAPI documentation generator with responsive three-panel design", "url": "https://redocly.com/redoc", "category": "API"},
    {"name": "Stoplight", "description": "API design, documentation, and development platform", "url": "https://stoplight.io/", "category": "API"},
    {"name": "Hoppscotch", "description": "Open source API development ecosystem", "url": "https://hoppscotch.io/", "category": "API"},
    {"name": "Insomnia", "description": "API client for REST, GraphQL, and gRPC", "url": "https://insomnia.rest/", "category": "API"},
    {"name": "Bruno", "description": "Open source IDE for exploring and testing APIs", "url": "https://www.usebruno.com/", "category": "API"},
    {"name": "Docusaurus", "description": "Easy to maintain open source documentation websites", "url": "https://docusaurus.io/", "category": "Documentation", "popular": True},
    {"name": "VitePress", "description": "Vite & Vue powered static site generator for documentation", "url": "https://vitepress.dev/", "category": "Documentation"},
    {"name": "MkDocs", "description": "Fast, simple static site generator for project documentation", "url": "https://www.mkdocs.org/", "category": "Documentation"},
    {"name": "Nextra", "description": "Next.js based static site generator for documentation", "url": "https://nextra.site/", "category": "Documentation"},
    {"name": "GitBook", "description": "Knowledge management tool for technical teams", "url": "https://www.gitbook.com/", "category": "Documentation"},
    {"name": "Read the Docs", "description": "Documentation hosting platform for open source projects", "url": "https://readthedocs.org/", "category": "Documentation"},
    {"name": "Mintlify", "description": "Modern documentation that converts visitors to users", "url": "https://mintlify.com/", "category": "Documentation"},
    
    # Misc Dev Tools
    {"name": "ngrok", "description": "Secure tunnels to localhost for exposing local servers", "url": "https://ngrok.com/", "category": "DevOps", "popular": True},
    {"name": "LocalTunnel", "description": "Expose your localhost to the world for testing and sharing", "url": "https://theboroer.github.io/localtunnel-www/", "category": "DevOps"},
    {"name": "mkcert", "description": "Simple tool for making locally-trusted development certificates", "url": "https://github.com/FiloSottile/mkcert", "category": "DevOps"},
    {"name": "direnv", "description": "Environment switcher for the shell", "url": "https://direnv.net/", "category": "DevOps"},
    {"name": "asdf", "description": "Extendable version manager for multiple runtime versions", "url": "https://asdf-vm.com/", "category": "DevOps"},
    {"name": "mise", "description": "Polyglot runtime manager (formerly rtx)", "url": "https://mise.jdx.dev/", "category": "DevOps"},
    {"name": "Zsh", "description": "Powerful Unix shell with scripting and interactive features", "url": "https://www.zsh.org/", "category": "CLI"},
    {"name": "Oh My Zsh", "description": "Framework for managing Zsh configuration with plugins and themes", "url": "https://ohmyz.sh/", "category": "CLI"},
    {"name": "Fish", "description": "Smart and user-friendly command line shell", "url": "https://fishshell.com/", "category": "CLI"},
    {"name": "Starship", "description": "Minimal, blazing-fast, customizable prompt for any shell", "url": "https://starship.rs/", "category": "CLI"},
    {"name": "tmux", "description": "Terminal multiplexer for managing multiple terminal sessions", "url": "https://github.com/tmux/tmux", "category": "CLI", "popular": True},
    {"name": "Zellij", "description": "Terminal workspace with panes and tabs written in Rust", "url": "https://zellij.dev/", "category": "CLI"},
    {"name": "fzf", "description": "General-purpose command-line fuzzy finder", "url": "https://github.com/junegunn/fzf", "category": "CLI"},
    {"name": "ripgrep", "description": "Recursively searches directories for regex pattern", "url": "https://github.com/BurntSushi/ripgrep", "category": "CLI"},
    {"name": "bat", "description": "Cat clone with syntax highlighting and Git integration", "url": "https://github.com/sharkdp/bat", "category": "CLI"},
    {"name": "exa", "description": "Modern replacement for ls with colors and icons", "url": "https://the.exa.website/", "category": "CLI"},
    {"name": "fd", "description": "Simple, fast alternative to find command", "url": "https://github.com/sharkdp/fd", "category": "CLI"},
    {"name": "jq", "description": "Lightweight command-line JSON processor", "url": "https://stedolan.github.io/jq/", "category": "CLI", "popular": True},
    {"name": "yq", "description": "Command-line YAML/JSON/XML processor", "url": "https://mikefarah.gitbook.io/yq/", "category": "CLI"},
    {"name": "httpie", "description": "User-friendly command-line HTTP client for the API era", "url": "https://httpie.io/", "category": "CLI"},
    {"name": "curl", "description": "Command-line tool for transferring data with URLs", "url": "https://curl.se/", "category": "CLI", "popular": True},
    {"name": "wget", "description": "Non-interactive network downloader", "url": "https://www.gnu.org/software/wget/", "category": "CLI"},
]

def main():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing_names = {item.get('name', '').lower() for item in data}
    
    added = []
    skipped = []
    
    for tool in NEW_TOOLS:
        if tool['name'].lower() not in existing_names:
            data.append(tool)
            added.append(tool['name'])
        else:
            skipped.append(tool['name'])
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Added {len(added)} tools:")
    for name in added:
        print(f"  + {name}")
    
    if skipped:
        print(f"\nSkipped {len(skipped)} (already exist):")
        for name in skipped:
            print(f"  - {name}")
    
    print(f"\nTotal items now: {len(data)}")

if __name__ == '__main__':
    main()
