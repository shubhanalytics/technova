#!/usr/bin/env python3
"""
Reorganize and clean up categories in data.json
- Clean up Tool category (remove webpage titles, invalid entries)
- Add new categories: Database, DevOps, IDE/Editor, Testing, Security, Container, Blockchain, Monitoring, API
- Reclassify existing items into appropriate categories
- Add missing key items
"""

import json
import re
from datetime import datetime

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Starting with {len(data)} items")

# Backup
with open(f'data.json.prereorg.bak', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# =============================================================================
# STEP 1: Clean up bad entries (webpage titles, invalid names)
# =============================================================================
def is_bad_entry(item):
    name = item.get('name', '')
    # Skip if name looks like a webpage title
    if name.startswith('"') or name.endswith('"'):
        return True
    if ' - ' in name and len(name) > 50:
        return True
    if '::' in name or '|' in name:
        return True
    if name.startswith('Download') or name.startswith('Install'):
        return True
    if 'Documentation' in name or 'Getting Started' in name:
        return True
    if 'Requirements' in name or 'Configuration' in name:
        return True
    if re.match(r'^\d+\.', name):  # Starts with number like "2. Something"
        return True
    return False

removed = []
cleaned_data = []
for item in data:
    if is_bad_entry(item):
        removed.append(item.get('name', ''))
    else:
        cleaned_data.append(item)

print(f"Removed {len(removed)} bad entries")
data = cleaned_data

# =============================================================================
# STEP 2: Classification rules for new categories
# =============================================================================
classification_rules = {
    'Database': {
        'exact': ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'Cassandra', 
                  'Neo4j', 'MariaDB', 'CouchDB', 'DynamoDB', 'Elasticsearch', 'InfluxDB',
                  'TimescaleDB', 'CockroachDB', 'ScyllaDB', 'RethinkDB', 'ArangoDB', 
                  'ClickHouse', 'PlanetScale', 'Supabase', 'Neon', 'Turso', 'Snowflake',
                  'dBase', 'SQL', 'PL/SQL', 'T-SQL', 'LINQ', 'Firebird', 'H2', 'HSQLDB'],
        'keywords': ['database', 'nosql', 'sql server']
    },
    'DevOps': {
        'exact': ['Jenkins', 'GitLab CI', 'CircleCI', 'Travis CI', 'GitHub Actions', 
                  'ArgoCD', 'Spinnaker', 'Bamboo', 'TeamCity', 'Terraform', 'Pulumi',
                  'Ansible', 'Chef', 'Puppet', 'SaltStack', 'Vagrant', 'Packer'],
        'keywords': ['ci/cd', 'pipeline', 'infrastructure as code']
    },
    'Container': {
        'exact': ['Docker', 'Kubernetes', 'Podman', 'containerd', 'LXC', 'OpenShift',
                  'Rancher', 'Nomad', 'Docker Compose', 'Docker Swarm', 'Helm', 'Istio',
                  'Linkerd', 'Envoy', 'K3s', 'MicroK8s', 'Kind', 'Minikube'],
        'keywords': ['container', 'orchestration', 'service mesh']
    },
    'IDE/Editor': {
        'exact': ['Visual Studio Code', 'VS Code', 'IntelliJ IDEA', 'PyCharm', 'WebStorm',
                  'PhpStorm', 'RubyMine', 'GoLand', 'CLion', 'DataGrip', 'Rider',
                  'Eclipse', 'NetBeans', 'Vim', 'Neovim', 'Emacs', 'Sublime Text',
                  'Atom', 'Brackets', 'Notepad++', 'TextMate', 'BBEdit', 'Gedit',
                  'Kate', 'Nano', 'Visual Studio', 'Xcode', 'Android Studio',
                  'JetBrains Fleet', 'Zed', 'Helix', 'Cursor', 'Windsurf'],
        'keywords': ['code editor', 'development environment']
    },
    'Testing': {
        'exact': ['Jest', 'Mocha', 'Jasmine', 'Cypress', 'Playwright', 'Selenium',
                  'Puppeteer', 'TestCafe', 'PyTest', 'unittest', 'JUnit', 'TestNG',
                  'NUnit', 'xUnit', 'RSpec', 'Minitest', 'PHPUnit', 'Vitest',
                  'Testing Library', 'Enzyme', 'Postman', 'Insomnia', 'k6', 'Gatling',
                  'JMeter', 'Locust', 'Artillery', 'Cucumber', 'SpecFlow'],
        'keywords': ['testing framework', 'test runner', 'load testing', 'e2e testing']
    },
    'Security': {
        'exact': ['OWASP ZAP', 'Burp Suite', 'Nmap', 'Wireshark', 'Metasploit',
                  'Snort', 'Suricata', 'Nessus', 'OpenVAS', 'Trivy', 'Snyk',
                  'SonarQube', 'Dependabot', 'HashiCorp Vault', 'CyberArk',
                  'Keycloak', 'Auth0', 'Okta', 'OpenSSL', 'Let\'s Encrypt',
                  'Certbot', 'Falco', 'Aqua Security', 'Prisma Cloud'],
        'keywords': ['security scanner', 'vulnerability', 'penetration testing', 'authentication']
    },
    'Monitoring': {
        'exact': ['Prometheus', 'Grafana', 'Datadog', 'New Relic', 'Splunk',
                  'Elastic Stack', 'ELK Stack', 'Kibana', 'Logstash', 'Fluentd',
                  'Jaeger', 'Zipkin', 'OpenTelemetry', 'PagerDuty', 'OpsGenie',
                  'Sentry', 'Rollbar', 'Bugsnag', 'Raygun', 'AppDynamics',
                  'Dynatrace', 'Honeycomb', 'Lightstep', 'Signoz', 'Uptrace'],
        'keywords': ['monitoring', 'observability', 'logging', 'tracing', 'apm']
    },
    'API': {
        'exact': ['Swagger', 'OpenAPI', 'GraphQL', 'Apollo', 'Hasura', 'PostgREST',
                  'Kong', 'Apigee', 'AWS API Gateway', 'Tyk', 'FastAPI', 'Express',
                  'gRPC', 'tRPC', 'Hono', 'Elysia', 'Postman', 'Insomnia', 'Paw',
                  'RapidAPI', 'Stoplight', 'Readme', 'Redoc'],
        'keywords': ['api gateway', 'api management', 'rest api', 'graphql']
    },
    'Blockchain': {
        'exact': ['Ethereum', 'Solana', 'Polygon', 'Avalanche', 'Cardano', 'Polkadot',
                  'Cosmos', 'Near', 'Algorand', 'Tezos', 'Chainlink', 'Hardhat',
                  'Truffle', 'Foundry', 'OpenZeppelin', 'Ethers.js', 'Web3.js',
                  'Solidity', 'Vyper', 'Rust (Solana)', 'Move', 'IPFS', 'Filecoin'],
        'keywords': ['blockchain', 'smart contract', 'web3', 'defi', 'nft']
    },
    'Mobile': {
        'exact': ['React Native', 'Flutter', 'Ionic', 'Capacitor', 'NativeScript',
                  'Xamarin', 'MAUI', 'Kotlin Multiplatform', 'SwiftUI', 'Jetpack Compose',
                  'Expo', 'Tauri', 'Electron'],
        'keywords': ['mobile development', 'cross-platform', 'native app']
    },
    'CMS': {
        'exact': ['WordPress', 'Drupal', 'Joomla', 'Ghost', 'Strapi', 'Contentful',
                  'Sanity', 'Prismic', 'Directus', 'Payload', 'KeystoneJS', 'Craft CMS',
                  'Umbraco', 'Sitecore', 'Adobe Experience Manager', 'Webflow',
                  'Squarespace', 'Wix', 'Shopify', 'Magento', 'WooCommerce'],
        'keywords': ['content management', 'headless cms', 'ecommerce platform']
    },
    'Low-Code': {
        'exact': ['Bubble', 'Retool', 'Appsmith', 'Budibase', 'Tooljet', 'Zapier',
                  'n8n', 'Make', 'Integromat', 'Power Apps', 'Power Automate',
                  'Airtable', 'Notion', 'Coda', 'OutSystems', 'Mendix', 'Appian'],
        'keywords': ['low-code', 'no-code', 'workflow automation', 'visual builder']
    }
}

# =============================================================================
# STEP 3: Reclassify existing items
# =============================================================================
reclassified = {'total': 0}
for cat in classification_rules:
    reclassified[cat] = 0

for item in data:
    name = item.get('name', '')
    desc = item.get('description', '').lower()
    old_cat = item.get('category', '')
    
    # Skip Programming Language - they stay as is
    if old_cat == 'Programming Language':
        continue
    
    # Check exact matches first
    for new_cat, rules in classification_rules.items():
        if name in rules.get('exact', []):
            if old_cat != new_cat:
                item['category'] = new_cat
                reclassified[new_cat] += 1
                reclassified['total'] += 1
            break
    else:
        # Check keyword matches
        for new_cat, rules in classification_rules.items():
            if any(kw in desc for kw in rules.get('keywords', [])):
                if old_cat != new_cat:
                    item['category'] = new_cat
                    reclassified[new_cat] += 1
                    reclassified['total'] += 1
                break

print(f"\nReclassified {reclassified['total']} items:")
for cat, count in reclassified.items():
    if cat != 'total' and count > 0:
        print(f"  {cat}: {count}")

# =============================================================================
# STEP 4: Add missing key items
# =============================================================================
new_items = [
    # Databases
    {'name': 'PostgreSQL', 'description': 'Powerful open-source relational database with advanced features', 'url': 'https://www.postgresql.org/', 'category': 'Database', 'popular': True},
    {'name': 'MySQL', 'description': 'Popular open-source relational database management system', 'url': 'https://www.mysql.com/', 'category': 'Database', 'popular': True},
    {'name': 'MongoDB', 'description': 'Document-oriented NoSQL database for modern applications', 'url': 'https://www.mongodb.com/', 'category': 'Database', 'popular': True},
    {'name': 'Redis', 'description': 'In-memory data structure store used as database, cache, and message broker', 'url': 'https://redis.io/', 'category': 'Database', 'popular': True},
    {'name': 'SQLite', 'description': 'Self-contained, serverless SQL database engine', 'url': 'https://www.sqlite.org/', 'category': 'Database', 'popular': True},
    {'name': 'Elasticsearch', 'description': 'Distributed search and analytics engine', 'url': 'https://www.elastic.co/elasticsearch/', 'category': 'Database', 'popular': True},
    {'name': 'Neo4j', 'description': 'Graph database platform for connected data', 'url': 'https://neo4j.com/', 'category': 'Database'},
    {'name': 'Cassandra', 'description': 'Distributed NoSQL database for handling large amounts of data', 'url': 'https://cassandra.apache.org/', 'category': 'Database'},
    {'name': 'ClickHouse', 'description': 'Fast open-source column-oriented database for analytics', 'url': 'https://clickhouse.com/', 'category': 'Database'},
    {'name': 'CockroachDB', 'description': 'Distributed SQL database designed for cloud-native applications', 'url': 'https://www.cockroachlabs.com/', 'category': 'Database'},
    
    # DevOps
    {'name': 'Jenkins', 'description': 'Open-source automation server for CI/CD pipelines', 'url': 'https://www.jenkins.io/', 'category': 'DevOps', 'popular': True},
    {'name': 'GitHub Actions', 'description': 'CI/CD platform integrated with GitHub repositories', 'url': 'https://github.com/features/actions', 'category': 'DevOps', 'popular': True},
    {'name': 'GitLab CI', 'description': 'Continuous integration and delivery built into GitLab', 'url': 'https://docs.gitlab.com/ee/ci/', 'category': 'DevOps', 'popular': True},
    {'name': 'CircleCI', 'description': 'Cloud-based continuous integration and delivery platform', 'url': 'https://circleci.com/', 'category': 'DevOps'},
    {'name': 'ArgoCD', 'description': 'Declarative GitOps continuous delivery tool for Kubernetes', 'url': 'https://argoproj.github.io/cd/', 'category': 'DevOps'},
    {'name': 'Pulumi', 'description': 'Infrastructure as code using familiar programming languages', 'url': 'https://www.pulumi.com/', 'category': 'DevOps'},
    
    # Containers
    {'name': 'Kubernetes', 'description': 'Container orchestration platform for automating deployment and scaling', 'url': 'https://kubernetes.io/', 'category': 'Container', 'popular': True},
    {'name': 'Helm', 'description': 'Package manager for Kubernetes applications', 'url': 'https://helm.sh/', 'category': 'Container'},
    {'name': 'Podman', 'description': 'Daemonless container engine for developing and running OCI containers', 'url': 'https://podman.io/', 'category': 'Container'},
    {'name': 'Istio', 'description': 'Service mesh for connecting, securing, and observing microservices', 'url': 'https://istio.io/', 'category': 'Container'},
    {'name': 'K3s', 'description': 'Lightweight Kubernetes distribution for edge and IoT', 'url': 'https://k3s.io/', 'category': 'Container'},
    
    # IDEs/Editors
    {'name': 'Visual Studio Code', 'description': 'Free, open-source code editor with extensive extension ecosystem', 'url': 'https://code.visualstudio.com/', 'category': 'IDE/Editor', 'popular': True},
    {'name': 'IntelliJ IDEA', 'description': 'Powerful IDE for Java and other JVM languages', 'url': 'https://www.jetbrains.com/idea/', 'category': 'IDE/Editor', 'popular': True},
    {'name': 'Neovim', 'description': 'Hyperextensible Vim-based text editor', 'url': 'https://neovim.io/', 'category': 'IDE/Editor', 'popular': True},
    {'name': 'Sublime Text', 'description': 'Sophisticated text editor for code and markup', 'url': 'https://www.sublimetext.com/', 'category': 'IDE/Editor'},
    {'name': 'Zed', 'description': 'High-performance multiplayer code editor', 'url': 'https://zed.dev/', 'category': 'IDE/Editor'},
    {'name': 'Cursor', 'description': 'AI-first code editor built for pair programming with AI', 'url': 'https://cursor.sh/', 'category': 'IDE/Editor'},
    {'name': 'PyCharm', 'description': 'Python IDE with intelligent code assistance', 'url': 'https://www.jetbrains.com/pycharm/', 'category': 'IDE/Editor'},
    
    # Testing
    {'name': 'Jest', 'description': 'Delightful JavaScript testing framework', 'url': 'https://jestjs.io/', 'category': 'Testing', 'popular': True},
    {'name': 'Cypress', 'description': 'JavaScript end-to-end testing framework', 'url': 'https://www.cypress.io/', 'category': 'Testing', 'popular': True},
    {'name': 'Playwright', 'description': 'End-to-end testing framework for modern web apps', 'url': 'https://playwright.dev/', 'category': 'Testing', 'popular': True},
    {'name': 'Selenium', 'description': 'Browser automation framework for web testing', 'url': 'https://www.selenium.dev/', 'category': 'Testing', 'popular': True},
    {'name': 'PyTest', 'description': 'Simple and powerful testing framework for Python', 'url': 'https://pytest.org/', 'category': 'Testing', 'popular': True},
    {'name': 'Vitest', 'description': 'Blazing fast unit test framework for Vite projects', 'url': 'https://vitest.dev/', 'category': 'Testing'},
    {'name': 'JUnit', 'description': 'Unit testing framework for Java', 'url': 'https://junit.org/', 'category': 'Testing'},
    {'name': 'k6', 'description': 'Modern load testing tool for developers', 'url': 'https://k6.io/', 'category': 'Testing'},
    
    # Security
    {'name': 'OWASP ZAP', 'description': 'Open-source web application security scanner', 'url': 'https://www.zaproxy.org/', 'category': 'Security', 'popular': True},
    {'name': 'Burp Suite', 'description': 'Web vulnerability scanner and security testing platform', 'url': 'https://portswigger.net/burp', 'category': 'Security', 'popular': True},
    {'name': 'Snyk', 'description': 'Developer security platform for finding and fixing vulnerabilities', 'url': 'https://snyk.io/', 'category': 'Security', 'popular': True},
    {'name': 'HashiCorp Vault', 'description': 'Secrets management and data protection platform', 'url': 'https://www.vaultproject.io/', 'category': 'Security', 'popular': True},
    {'name': 'Trivy', 'description': 'Comprehensive security scanner for containers and infrastructure', 'url': 'https://trivy.dev/', 'category': 'Security'},
    {'name': 'SonarQube', 'description': 'Continuous code quality and security inspection', 'url': 'https://www.sonarqube.org/', 'category': 'Security'},
    {'name': 'Keycloak', 'description': 'Open-source identity and access management solution', 'url': 'https://www.keycloak.org/', 'category': 'Security'},
    {'name': 'Nmap', 'description': 'Network discovery and security auditing tool', 'url': 'https://nmap.org/', 'category': 'Security'},
    
    # Monitoring
    {'name': 'Grafana', 'description': 'Open-source analytics and monitoring platform', 'url': 'https://grafana.com/', 'category': 'Monitoring', 'popular': True},
    {'name': 'Datadog', 'description': 'Cloud monitoring and security platform', 'url': 'https://www.datadoghq.com/', 'category': 'Monitoring', 'popular': True},
    {'name': 'Sentry', 'description': 'Application monitoring and error tracking platform', 'url': 'https://sentry.io/', 'category': 'Monitoring', 'popular': True},
    {'name': 'New Relic', 'description': 'Full-stack observability platform', 'url': 'https://newrelic.com/', 'category': 'Monitoring'},
    {'name': 'OpenTelemetry', 'description': 'Observability framework for cloud-native software', 'url': 'https://opentelemetry.io/', 'category': 'Monitoring'},
    {'name': 'Jaeger', 'description': 'Distributed tracing platform', 'url': 'https://www.jaegertracing.io/', 'category': 'Monitoring'},
    {'name': 'Elastic Stack', 'description': 'Search, observability, and security platform (ELK)', 'url': 'https://www.elastic.co/elastic-stack', 'category': 'Monitoring'},
    
    # API
    {'name': 'Swagger', 'description': 'API documentation and design tools', 'url': 'https://swagger.io/', 'category': 'API', 'popular': True},
    {'name': 'GraphQL', 'description': 'Query language and runtime for APIs', 'url': 'https://graphql.org/', 'category': 'API', 'popular': True},
    {'name': 'Postman', 'description': 'API platform for building and testing APIs', 'url': 'https://www.postman.com/', 'category': 'API', 'popular': True},
    {'name': 'Kong', 'description': 'Cloud-native API gateway and service mesh', 'url': 'https://konghq.com/', 'category': 'API'},
    {'name': 'Apollo GraphQL', 'description': 'GraphQL implementation with client and server libraries', 'url': 'https://www.apollographql.com/', 'category': 'API'},
    {'name': 'Hasura', 'description': 'Instant GraphQL APIs on your data', 'url': 'https://hasura.io/', 'category': 'API'},
    {'name': 'tRPC', 'description': 'End-to-end typesafe APIs for TypeScript', 'url': 'https://trpc.io/', 'category': 'API'},
    
    # Blockchain
    {'name': 'Hardhat', 'description': 'Ethereum development environment for professionals', 'url': 'https://hardhat.org/', 'category': 'Blockchain', 'popular': True},
    {'name': 'Solidity', 'description': 'Programming language for Ethereum smart contracts', 'url': 'https://soliditylang.org/', 'category': 'Blockchain', 'popular': True},
    {'name': 'Foundry', 'description': 'Blazing fast Ethereum development toolkit', 'url': 'https://getfoundry.sh/', 'category': 'Blockchain'},
    {'name': 'OpenZeppelin', 'description': 'Security products for building blockchain applications', 'url': 'https://www.openzeppelin.com/', 'category': 'Blockchain'},
    {'name': 'Ethers.js', 'description': 'Complete Ethereum library for JavaScript', 'url': 'https://ethers.org/', 'category': 'Blockchain'},
    {'name': 'Solana', 'description': 'High-performance blockchain for decentralized applications', 'url': 'https://solana.com/', 'category': 'Blockchain'},
    
    # Mobile
    {'name': 'Expo', 'description': 'Platform for building React Native apps', 'url': 'https://expo.dev/', 'category': 'Mobile', 'popular': True},
    {'name': 'Ionic', 'description': 'Cross-platform mobile app development framework', 'url': 'https://ionicframework.com/', 'category': 'Mobile'},
    {'name': 'Capacitor', 'description': 'Cross-platform native runtime for web apps', 'url': 'https://capacitorjs.com/', 'category': 'Mobile'},
    {'name': 'Tauri', 'description': 'Framework for building desktop apps with web technologies', 'url': 'https://tauri.app/', 'category': 'Mobile'},
    
    # CMS
    {'name': 'WordPress', 'description': 'Popular open-source content management system', 'url': 'https://wordpress.org/', 'category': 'CMS', 'popular': True},
    {'name': 'Strapi', 'description': 'Open-source headless CMS built with Node.js', 'url': 'https://strapi.io/', 'category': 'CMS', 'popular': True},
    {'name': 'Ghost', 'description': 'Professional publishing platform', 'url': 'https://ghost.org/', 'category': 'CMS'},
    {'name': 'Sanity', 'description': 'Composable content cloud platform', 'url': 'https://www.sanity.io/', 'category': 'CMS'},
    {'name': 'Contentful', 'description': 'Headless CMS for digital experiences', 'url': 'https://www.contentful.com/', 'category': 'CMS'},
    {'name': 'Payload', 'description': 'Headless CMS and application framework', 'url': 'https://payloadcms.com/', 'category': 'CMS'},
    
    # Low-Code
    {'name': 'Retool', 'description': 'Build internal tools remarkably fast', 'url': 'https://retool.com/', 'category': 'Low-Code', 'popular': True},
    {'name': 'n8n', 'description': 'Workflow automation tool with fair-code license', 'url': 'https://n8n.io/', 'category': 'Low-Code', 'popular': True},
    {'name': 'Appsmith', 'description': 'Open-source framework for building internal apps', 'url': 'https://www.appsmith.com/', 'category': 'Low-Code'},
    {'name': 'Zapier', 'description': 'Automation platform connecting apps and services', 'url': 'https://zapier.com/', 'category': 'Low-Code'},
    {'name': 'Budibase', 'description': 'Open-source low-code platform', 'url': 'https://budibase.com/', 'category': 'Low-Code'},
]

# Add items that don't already exist
existing_names = {item.get('name', '').lower() for item in data}
added = 0
for new_item in new_items:
    if new_item['name'].lower() not in existing_names:
        data.append(new_item)
        existing_names.add(new_item['name'].lower())
        added += 1

print(f"\nAdded {added} new items")

# =============================================================================
# STEP 5: Move items from Technology to appropriate new categories
# =============================================================================
tech_moves = {
    'Docker': 'Container',
    'Ansible': 'DevOps',
    'Terraform': 'DevOps',
    'Prometheus': 'Monitoring',
    'Wireshark': 'Security',
    'Snort': 'Security',
    'Ethereum': 'Blockchain',
    'Chainlink': 'Blockchain',
    'IPFS': 'Blockchain',
    'Flutter': 'Mobile',
    'React Native': 'Mobile',
}

moved_from_tech = 0
for item in data:
    name = item.get('name', '')
    if name in tech_moves:
        old_cat = item.get('category', '')
        new_cat = tech_moves[name]
        if old_cat != new_cat:
            item['category'] = new_cat
            moved_from_tech += 1

print(f"Moved {moved_from_tech} items from Technology to new categories")

# =============================================================================
# STEP 6: Final cleanup - merge Software into Tool if only a few items
# =============================================================================
software_items = [i for i in data if i.get('category') == 'Software']
if len(software_items) <= 5:
    for item in data:
        if item.get('category') == 'Software':
            item['category'] = 'Tool'
    print(f"Merged {len(software_items)} Software items into Tool")

# =============================================================================
# STEP 7: Summary
# =============================================================================
from collections import Counter
cats = Counter(i.get('category', '') for i in data)

print(f"\n{'='*50}")
print(f"Final Summary: {len(data)} items")
print(f"{'='*50}")
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nSaved to data.json")

# Also save removed items for review
with open('data.removed.json', 'w', encoding='utf-8') as f:
    json.dump(removed, f, indent=2, ensure_ascii=False)
print(f"Removed items saved to data.removed.json ({len(removed)} items)")
