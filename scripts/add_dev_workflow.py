#!/usr/bin/env python3
"""
Add comprehensive developer workflow categories:
- Build Tools, Package Managers, Version Control, Message Queues
- Search, ORM, Storage, Email, Analytics, CDN, Payment
- Serverless, Runtime, Design, Collaboration, Documentation
- Feature Flags, and expanded AI/ML
"""

import json

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Starting with {len(data)} items")

# Get existing names to avoid duplicates
existing_names = {item.get('name', '').lower() for item in data}

def add_items(items_to_add):
    added = 0
    for item in items_to_add:
        if item['name'].lower() not in existing_names:
            item['verified'] = True
            data.append(item)
            existing_names.add(item['name'].lower())
            added += 1
    return added

# =============================================================================
# BUILD TOOLS
# =============================================================================
build_tools = [
    {'name': 'Vite', 'description': 'Next generation frontend build tool', 'url': 'https://vitejs.dev/', 'category': 'Build Tool', 'popular': True},
    {'name': 'Webpack', 'description': 'Static module bundler for JavaScript applications', 'url': 'https://webpack.js.org/', 'category': 'Build Tool', 'popular': True},
    {'name': 'esbuild', 'description': 'Extremely fast JavaScript bundler and minifier', 'url': 'https://esbuild.github.io/', 'category': 'Build Tool', 'popular': True},
    {'name': 'Turbopack', 'description': 'Rust-based successor to Webpack by Vercel', 'url': 'https://turbo.build/pack', 'category': 'Build Tool', 'popular': True},
    {'name': 'Rollup', 'description': 'Module bundler for JavaScript libraries', 'url': 'https://rollupjs.org/', 'category': 'Build Tool', 'popular': True},
    {'name': 'SWC', 'description': 'Super-fast TypeScript/JavaScript compiler written in Rust', 'url': 'https://swc.rs/', 'category': 'Build Tool', 'popular': True},
    {'name': 'Babel', 'description': 'JavaScript compiler for using next-gen JS today', 'url': 'https://babeljs.io/', 'category': 'Build Tool', 'popular': True},
    {'name': 'Parcel', 'description': 'Zero configuration web application bundler', 'url': 'https://parceljs.org/', 'category': 'Build Tool'},
    {'name': 'Gulp', 'description': 'Streaming build system and task runner', 'url': 'https://gulpjs.com/', 'category': 'Build Tool'},
    {'name': 'Grunt', 'description': 'JavaScript task runner', 'url': 'https://gruntjs.com/', 'category': 'Build Tool'},
    {'name': 'Turborepo', 'description': 'High-performance build system for monorepos', 'url': 'https://turbo.build/repo', 'category': 'Build Tool', 'popular': True},
    {'name': 'Nx', 'description': 'Smart monorepo build system', 'url': 'https://nx.dev/', 'category': 'Build Tool', 'popular': True},
    {'name': 'Lerna', 'description': 'Tool for managing JavaScript monorepos', 'url': 'https://lerna.js.org/', 'category': 'Build Tool'},
    {'name': 'Rome', 'description': 'Unified toolchain for JavaScript and TypeScript', 'url': 'https://rome.tools/', 'category': 'Build Tool'},
    {'name': 'Biome', 'description': 'Fast formatter and linter for web projects', 'url': 'https://biomejs.dev/', 'category': 'Build Tool'},
    {'name': 'ESLint', 'description': 'Pluggable linting utility for JavaScript', 'url': 'https://eslint.org/', 'category': 'Build Tool', 'popular': True},
    {'name': 'Prettier', 'description': 'Opinionated code formatter', 'url': 'https://prettier.io/', 'category': 'Build Tool', 'popular': True},
    {'name': 'TypeScript', 'description': 'Typed superset of JavaScript that compiles to plain JS', 'url': 'https://www.typescriptlang.org/', 'category': 'Build Tool', 'popular': True},
    {'name': 'PostCSS', 'description': 'Tool for transforming CSS with JavaScript', 'url': 'https://postcss.org/', 'category': 'Build Tool'},
    {'name': 'Sass', 'description': 'CSS extension language with variables and nesting', 'url': 'https://sass-lang.com/', 'category': 'Build Tool', 'popular': True},
    {'name': 'Less', 'description': 'Backwards-compatible language extension for CSS', 'url': 'https://lesscss.org/', 'category': 'Build Tool'},
    {'name': 'Make', 'description': 'Build automation tool using Makefiles', 'url': 'https://www.gnu.org/software/make/', 'category': 'Build Tool'},
    {'name': 'CMake', 'description': 'Cross-platform build system generator', 'url': 'https://cmake.org/', 'category': 'Build Tool'},
    {'name': 'Bazel', 'description': 'Fast, scalable build tool by Google', 'url': 'https://bazel.build/', 'category': 'Build Tool'},
    {'name': 'Buck', 'description': 'Fast build system by Meta', 'url': 'https://buck.build/', 'category': 'Build Tool'},
]

# =============================================================================
# PACKAGE MANAGERS
# =============================================================================
package_managers = [
    {'name': 'npm', 'description': 'Default package manager for Node.js', 'url': 'https://www.npmjs.com/', 'category': 'Package Manager', 'popular': True},
    {'name': 'Yarn', 'description': 'Fast, reliable dependency management', 'url': 'https://yarnpkg.com/', 'category': 'Package Manager', 'popular': True},
    {'name': 'pnpm', 'description': 'Fast, disk space efficient package manager', 'url': 'https://pnpm.io/', 'category': 'Package Manager', 'popular': True},
    {'name': 'Bun', 'description': 'All-in-one JavaScript runtime and package manager', 'url': 'https://bun.sh/', 'category': 'Package Manager', 'popular': True},
    {'name': 'pip', 'description': 'Package installer for Python', 'url': 'https://pip.pypa.io/', 'category': 'Package Manager', 'popular': True},
    {'name': 'Poetry', 'description': 'Python dependency management and packaging', 'url': 'https://python-poetry.org/', 'category': 'Package Manager', 'popular': True},
    {'name': 'uv', 'description': 'Extremely fast Python package installer by Astral', 'url': 'https://github.com/astral-sh/uv', 'category': 'Package Manager', 'popular': True},
    {'name': 'Conda', 'description': 'Package and environment management for any language', 'url': 'https://docs.conda.io/', 'category': 'Package Manager', 'popular': True},
    {'name': 'Pipenv', 'description': 'Python packaging tool with Pipfile', 'url': 'https://pipenv.pypa.io/', 'category': 'Package Manager'},
    {'name': 'Cargo', 'description': 'Rust package manager and build system', 'url': 'https://doc.rust-lang.org/cargo/', 'category': 'Package Manager', 'popular': True},
    {'name': 'Maven', 'description': 'Build automation and dependency management for Java', 'url': 'https://maven.apache.org/', 'category': 'Package Manager', 'popular': True},
    {'name': 'Gradle', 'description': 'Build automation tool for multi-language projects', 'url': 'https://gradle.org/', 'category': 'Package Manager', 'popular': True},
    {'name': 'NuGet', 'description': 'Package manager for .NET', 'url': 'https://www.nuget.org/', 'category': 'Package Manager', 'popular': True},
    {'name': 'Composer', 'description': 'Dependency manager for PHP', 'url': 'https://getcomposer.org/', 'category': 'Package Manager', 'popular': True},
    {'name': 'RubyGems', 'description': 'Package manager for Ruby', 'url': 'https://rubygems.org/', 'category': 'Package Manager'},
    {'name': 'Bundler', 'description': 'Dependency manager for Ruby projects', 'url': 'https://bundler.io/', 'category': 'Package Manager'},
    {'name': 'Go Modules', 'description': 'Dependency management for Go', 'url': 'https://go.dev/ref/mod', 'category': 'Package Manager'},
    {'name': 'Homebrew', 'description': 'Package manager for macOS and Linux', 'url': 'https://brew.sh/', 'category': 'Package Manager', 'popular': True},
    {'name': 'Chocolatey', 'description': 'Package manager for Windows', 'url': 'https://chocolatey.org/', 'category': 'Package Manager'},
    {'name': 'Scoop', 'description': 'Command-line installer for Windows', 'url': 'https://scoop.sh/', 'category': 'Package Manager'},
    {'name': 'apt', 'description': 'Package manager for Debian-based Linux', 'url': 'https://wiki.debian.org/Apt', 'category': 'Package Manager'},
    {'name': 'CocoaPods', 'description': 'Dependency manager for Swift and Objective-C', 'url': 'https://cocoapods.org/', 'category': 'Package Manager'},
    {'name': 'Swift Package Manager', 'description': 'Dependency manager for Swift projects', 'url': 'https://swift.org/package-manager/', 'category': 'Package Manager'},
    {'name': 'Hex', 'description': 'Package manager for Erlang ecosystem', 'url': 'https://hex.pm/', 'category': 'Package Manager'},
    {'name': 'Pub', 'description': 'Package manager for Dart and Flutter', 'url': 'https://pub.dev/', 'category': 'Package Manager'},
]

# =============================================================================
# VERSION CONTROL
# =============================================================================
version_control = [
    {'name': 'Git', 'description': 'Distributed version control system', 'url': 'https://git-scm.com/', 'category': 'Version Control', 'popular': True},
    {'name': 'GitHub', 'description': 'Code hosting platform for Git repositories', 'url': 'https://github.com/', 'category': 'Version Control', 'popular': True},
    {'name': 'GitLab', 'description': 'DevOps platform with Git repository management', 'url': 'https://gitlab.com/', 'category': 'Version Control', 'popular': True},
    {'name': 'Bitbucket', 'description': 'Git code management by Atlassian', 'url': 'https://bitbucket.org/', 'category': 'Version Control', 'popular': True},
    {'name': 'Azure DevOps', 'description': 'Development collaboration tools by Microsoft', 'url': 'https://azure.microsoft.com/en-us/products/devops/', 'category': 'Version Control'},
    {'name': 'Gitea', 'description': 'Self-hosted Git service', 'url': 'https://gitea.io/', 'category': 'Version Control'},
    {'name': 'Forgejo', 'description': 'Community-driven self-hosted Git forge', 'url': 'https://forgejo.org/', 'category': 'Version Control'},
    {'name': 'SourceHut', 'description': 'Minimalist software development platform', 'url': 'https://sourcehut.org/', 'category': 'Version Control'},
    {'name': 'Mercurial', 'description': 'Distributed version control system', 'url': 'https://www.mercurial-scm.org/', 'category': 'Version Control'},
    {'name': 'SVN', 'description': 'Centralized version control system', 'url': 'https://subversion.apache.org/', 'category': 'Version Control'},
    {'name': 'Perforce', 'description': 'Enterprise version control for large codebases', 'url': 'https://www.perforce.com/', 'category': 'Version Control'},
    {'name': 'GitKraken', 'description': 'Visual Git client', 'url': 'https://www.gitkraken.com/', 'category': 'Version Control'},
    {'name': 'SourceTree', 'description': 'Free Git client by Atlassian', 'url': 'https://www.sourcetreeapp.com/', 'category': 'Version Control'},
    {'name': 'GitHub Desktop', 'description': 'Official GitHub desktop client', 'url': 'https://desktop.github.com/', 'category': 'Version Control'},
    {'name': 'Conventional Commits', 'description': 'Specification for commit messages', 'url': 'https://www.conventionalcommits.org/', 'category': 'Version Control'},
    {'name': 'git-crypt', 'description': 'Transparent file encryption in Git', 'url': 'https://github.com/AGWA/git-crypt', 'category': 'Version Control'},
    {'name': 'git-lfs', 'description': 'Git extension for large file storage', 'url': 'https://git-lfs.com/', 'category': 'Version Control'},
]

# =============================================================================
# MESSAGE QUEUES
# =============================================================================
message_queues = [
    {'name': 'Apache Kafka', 'description': 'Distributed event streaming platform', 'url': 'https://kafka.apache.org/', 'category': 'Message Queue', 'popular': True},
    {'name': 'RabbitMQ', 'description': 'Open-source message broker', 'url': 'https://www.rabbitmq.com/', 'category': 'Message Queue', 'popular': True},
    {'name': 'Amazon SQS', 'description': 'Fully managed message queuing service', 'url': 'https://aws.amazon.com/sqs/', 'category': 'Message Queue', 'popular': True},
    {'name': 'Amazon SNS', 'description': 'Fully managed pub/sub messaging service', 'url': 'https://aws.amazon.com/sns/', 'category': 'Message Queue'},
    {'name': 'NATS', 'description': 'High-performance messaging system', 'url': 'https://nats.io/', 'category': 'Message Queue', 'popular': True},
    {'name': 'Redis Pub/Sub', 'description': 'Messaging paradigm in Redis', 'url': 'https://redis.io/docs/manual/pubsub/', 'category': 'Message Queue'},
    {'name': 'Apache Pulsar', 'description': 'Distributed pub-sub messaging platform', 'url': 'https://pulsar.apache.org/', 'category': 'Message Queue'},
    {'name': 'ZeroMQ', 'description': 'High-performance asynchronous messaging library', 'url': 'https://zeromq.org/', 'category': 'Message Queue'},
    {'name': 'Bull', 'description': 'Redis-based queue for Node.js', 'url': 'https://github.com/OptimalBits/bull', 'category': 'Message Queue'},
    {'name': 'BullMQ', 'description': 'Message queue based on Redis for Node.js', 'url': 'https://bullmq.io/', 'category': 'Message Queue', 'popular': True},
    {'name': 'Celery', 'description': 'Distributed task queue for Python', 'url': 'https://docs.celeryq.dev/', 'category': 'Message Queue', 'popular': True},
    {'name': 'Azure Service Bus', 'description': 'Enterprise message broker by Microsoft', 'url': 'https://azure.microsoft.com/en-us/products/service-bus/', 'category': 'Message Queue'},
    {'name': 'Google Cloud Pub/Sub', 'description': 'Messaging and ingestion for streaming data', 'url': 'https://cloud.google.com/pubsub', 'category': 'Message Queue'},
    {'name': 'ActiveMQ', 'description': 'Open-source message broker', 'url': 'https://activemq.apache.org/', 'category': 'Message Queue'},
    {'name': 'Redpanda', 'description': 'Kafka-compatible streaming data platform', 'url': 'https://redpanda.com/', 'category': 'Message Queue'},
    {'name': 'Inngest', 'description': 'Durable workflow engine for background jobs', 'url': 'https://www.inngest.com/', 'category': 'Message Queue'},
    {'name': 'Trigger.dev', 'description': 'Background jobs with no infrastructure', 'url': 'https://trigger.dev/', 'category': 'Message Queue'},
    {'name': 'Upstash Kafka', 'description': 'Serverless Kafka', 'url': 'https://upstash.com/kafka', 'category': 'Message Queue'},
    {'name': 'Upstash QStash', 'description': 'Serverless message queue', 'url': 'https://upstash.com/qstash', 'category': 'Message Queue'},
]

# =============================================================================
# SEARCH
# =============================================================================
search = [
    {'name': 'Algolia', 'description': 'Hosted search API for websites and apps', 'url': 'https://www.algolia.com/', 'category': 'Search', 'popular': True},
    {'name': 'Meilisearch', 'description': 'Lightning fast, open-source search engine', 'url': 'https://www.meilisearch.com/', 'category': 'Search', 'popular': True},
    {'name': 'Typesense', 'description': 'Fast, typo-tolerant search engine', 'url': 'https://typesense.org/', 'category': 'Search', 'popular': True},
    {'name': 'Elasticsearch', 'description': 'Distributed search and analytics engine', 'url': 'https://www.elastic.co/elasticsearch/', 'category': 'Search', 'popular': True},
    {'name': 'OpenSearch', 'description': 'Open-source search and analytics suite', 'url': 'https://opensearch.org/', 'category': 'Search'},
    {'name': 'Solr', 'description': 'Open-source enterprise search platform', 'url': 'https://solr.apache.org/', 'category': 'Search'},
    {'name': 'Zinc', 'description': 'Lightweight Elasticsearch alternative', 'url': 'https://zincsearch.com/', 'category': 'Search'},
    {'name': 'Orama', 'description': 'In-memory full-text search engine', 'url': 'https://oramasearch.com/', 'category': 'Search'},
    {'name': 'Fuse.js', 'description': 'Lightweight fuzzy-search JavaScript library', 'url': 'https://fusejs.io/', 'category': 'Search'},
    {'name': 'Lunr.js', 'description': 'Full-text search library for the browser', 'url': 'https://lunrjs.com/', 'category': 'Search'},
    {'name': 'FlexSearch', 'description': 'Fastest full-text search library', 'url': 'https://github.com/nextapps-de/flexsearch', 'category': 'Search'},
    {'name': 'DocSearch', 'description': 'Search for documentation sites by Algolia', 'url': 'https://docsearch.algolia.com/', 'category': 'Search'},
    {'name': 'Pagefind', 'description': 'Static search library for static sites', 'url': 'https://pagefind.app/', 'category': 'Search'},
]

# =============================================================================
# ORM / DATABASE TOOLS
# =============================================================================
orm = [
    {'name': 'Prisma', 'description': 'Next-generation Node.js and TypeScript ORM', 'url': 'https://www.prisma.io/', 'category': 'ORM', 'popular': True},
    {'name': 'Drizzle ORM', 'description': 'TypeScript ORM with SQL-like syntax', 'url': 'https://orm.drizzle.team/', 'category': 'ORM', 'popular': True},
    {'name': 'TypeORM', 'description': 'ORM for TypeScript and JavaScript', 'url': 'https://typeorm.io/', 'category': 'ORM', 'popular': True},
    {'name': 'Sequelize', 'description': 'Promise-based Node.js ORM', 'url': 'https://sequelize.org/', 'category': 'ORM', 'popular': True},
    {'name': 'Knex.js', 'description': 'SQL query builder for JavaScript', 'url': 'https://knexjs.org/', 'category': 'ORM'},
    {'name': 'Kysely', 'description': 'Type-safe TypeScript SQL query builder', 'url': 'https://kysely.dev/', 'category': 'ORM', 'popular': True},
    {'name': 'MikroORM', 'description': 'TypeScript ORM for Node.js based on Data Mapper', 'url': 'https://mikro-orm.io/', 'category': 'ORM'},
    {'name': 'Objection.js', 'description': 'SQL-friendly ORM for Node.js', 'url': 'https://vincit.github.io/objection.js/', 'category': 'ORM'},
    {'name': 'SQLAlchemy', 'description': 'Python SQL toolkit and ORM', 'url': 'https://www.sqlalchemy.org/', 'category': 'ORM', 'popular': True},
    {'name': 'Django ORM', 'description': 'Built-in ORM for Django framework', 'url': 'https://docs.djangoproject.com/en/stable/topics/db/', 'category': 'ORM', 'popular': True},
    {'name': 'Peewee', 'description': 'Simple and small Python ORM', 'url': 'http://docs.peewee-orm.com/', 'category': 'ORM'},
    {'name': 'Tortoise ORM', 'description': 'Async ORM for Python', 'url': 'https://tortoise.github.io/', 'category': 'ORM'},
    {'name': 'SQLModel', 'description': 'SQL databases in Python with Pydantic', 'url': 'https://sqlmodel.tiangolo.com/', 'category': 'ORM', 'popular': True},
    {'name': 'ActiveRecord', 'description': 'ORM pattern in Ruby on Rails', 'url': 'https://guides.rubyonrails.org/active_record_basics.html', 'category': 'ORM'},
    {'name': 'Hibernate', 'description': 'ORM framework for Java', 'url': 'https://hibernate.org/', 'category': 'ORM', 'popular': True},
    {'name': 'Entity Framework', 'description': 'ORM for .NET applications', 'url': 'https://docs.microsoft.com/en-us/ef/', 'category': 'ORM', 'popular': True},
    {'name': 'Dapper', 'description': 'Simple object mapper for .NET', 'url': 'https://github.com/DapperLib/Dapper', 'category': 'ORM'},
    {'name': 'GORM', 'description': 'ORM library for Go', 'url': 'https://gorm.io/', 'category': 'ORM', 'popular': True},
    {'name': 'Ent', 'description': 'Entity framework for Go', 'url': 'https://entgo.io/', 'category': 'ORM'},
    {'name': 'Diesel', 'description': 'Safe Rust ORM', 'url': 'https://diesel.rs/', 'category': 'ORM'},
    {'name': 'SeaORM', 'description': 'Async ORM for Rust', 'url': 'https://www.sea-ql.org/SeaORM/', 'category': 'ORM'},
]

# =============================================================================
# STORAGE / FILE HANDLING
# =============================================================================
storage = [
    {'name': 'Amazon S3', 'description': 'Scalable object storage by AWS', 'url': 'https://aws.amazon.com/s3/', 'category': 'Storage', 'popular': True},
    {'name': 'Cloudflare R2', 'description': 'Object storage with zero egress fees', 'url': 'https://www.cloudflare.com/products/r2/', 'category': 'Storage', 'popular': True},
    {'name': 'Google Cloud Storage', 'description': 'Object storage by Google', 'url': 'https://cloud.google.com/storage', 'category': 'Storage'},
    {'name': 'Azure Blob Storage', 'description': 'Object storage by Microsoft', 'url': 'https://azure.microsoft.com/en-us/products/storage/blobs/', 'category': 'Storage'},
    {'name': 'MinIO', 'description': 'High-performance, S3 compatible object storage', 'url': 'https://min.io/', 'category': 'Storage', 'popular': True},
    {'name': 'Cloudinary', 'description': 'Media management and optimization platform', 'url': 'https://cloudinary.com/', 'category': 'Storage', 'popular': True},
    {'name': 'Uploadthing', 'description': 'File uploads for full-stack TypeScript apps', 'url': 'https://uploadthing.com/', 'category': 'Storage', 'popular': True},
    {'name': 'Bunny.net Storage', 'description': 'Global edge storage platform', 'url': 'https://bunny.net/storage/', 'category': 'Storage'},
    {'name': 'Backblaze B2', 'description': 'Affordable cloud object storage', 'url': 'https://www.backblaze.com/b2/', 'category': 'Storage'},
    {'name': 'Wasabi', 'description': 'Hot cloud storage at cold prices', 'url': 'https://wasabi.com/', 'category': 'Storage'},
    {'name': 'DigitalOcean Spaces', 'description': 'Simple object storage with CDN', 'url': 'https://www.digitalocean.com/products/spaces', 'category': 'Storage'},
    {'name': 'Supabase Storage', 'description': 'S3-compatible storage by Supabase', 'url': 'https://supabase.com/storage', 'category': 'Storage'},
    {'name': 'Uppy', 'description': 'Modular JavaScript file uploader', 'url': 'https://uppy.io/', 'category': 'Storage'},
    {'name': 'Filepond', 'description': 'Flexible file upload library', 'url': 'https://pqina.nl/filepond/', 'category': 'Storage'},
    {'name': 'Dropzone.js', 'description': 'Drag and drop file uploads', 'url': 'https://www.dropzone.dev/', 'category': 'Storage'},
    {'name': 'react-dropzone', 'description': 'Simple React hook for file uploads', 'url': 'https://react-dropzone.js.org/', 'category': 'Storage'},
    {'name': 'tus', 'description': 'Resumable file upload protocol', 'url': 'https://tus.io/', 'category': 'Storage'},
    {'name': 'imgix', 'description': 'Real-time image processing and CDN', 'url': 'https://imgix.com/', 'category': 'Storage'},
    {'name': 'ImageKit', 'description': 'Real-time image optimization and transformation', 'url': 'https://imagekit.io/', 'category': 'Storage'},
]

# =============================================================================
# EMAIL
# =============================================================================
email = [
    {'name': 'SendGrid', 'description': 'Cloud-based email delivery platform', 'url': 'https://sendgrid.com/', 'category': 'Email', 'popular': True},
    {'name': 'Resend', 'description': 'Email API for developers', 'url': 'https://resend.com/', 'category': 'Email', 'popular': True},
    {'name': 'Postmark', 'description': 'Transactional email service', 'url': 'https://postmarkapp.com/', 'category': 'Email', 'popular': True},
    {'name': 'Mailgun', 'description': 'Email API for sending and receiving', 'url': 'https://www.mailgun.com/', 'category': 'Email', 'popular': True},
    {'name': 'Amazon SES', 'description': 'Cloud email service by AWS', 'url': 'https://aws.amazon.com/ses/', 'category': 'Email', 'popular': True},
    {'name': 'Mailchimp Transactional', 'description': 'Transactional email by Mailchimp', 'url': 'https://mailchimp.com/developer/transactional/', 'category': 'Email'},
    {'name': 'SparkPost', 'description': 'Email delivery service', 'url': 'https://www.sparkpost.com/', 'category': 'Email'},
    {'name': 'Nodemailer', 'description': 'Email sending module for Node.js', 'url': 'https://nodemailer.com/', 'category': 'Email', 'popular': True},
    {'name': 'React Email', 'description': 'Build emails using React components', 'url': 'https://react.email/', 'category': 'Email', 'popular': True},
    {'name': 'MJML', 'description': 'Markup language for responsive emails', 'url': 'https://mjml.io/', 'category': 'Email'},
    {'name': 'Mailtrap', 'description': 'Email testing and debugging platform', 'url': 'https://mailtrap.io/', 'category': 'Email'},
    {'name': 'Loops', 'description': 'Email platform for SaaS companies', 'url': 'https://loops.so/', 'category': 'Email'},
    {'name': 'Plunk', 'description': 'Open-source email platform', 'url': 'https://www.useplunk.com/', 'category': 'Email'},
    {'name': 'Buttondown', 'description': 'Newsletter platform for developers', 'url': 'https://buttondown.email/', 'category': 'Email'},
    {'name': 'ConvertKit', 'description': 'Email marketing for creators', 'url': 'https://convertkit.com/', 'category': 'Email'},
]

# =============================================================================
# ANALYTICS
# =============================================================================
analytics = [
    {'name': 'PostHog', 'description': 'Open-source product analytics platform', 'url': 'https://posthog.com/', 'category': 'Analytics', 'popular': True},
    {'name': 'Mixpanel', 'description': 'Product analytics for mobile and web', 'url': 'https://mixpanel.com/', 'category': 'Analytics', 'popular': True},
    {'name': 'Amplitude', 'description': 'Product intelligence platform', 'url': 'https://amplitude.com/', 'category': 'Analytics', 'popular': True},
    {'name': 'Plausible', 'description': 'Privacy-friendly web analytics', 'url': 'https://plausible.io/', 'category': 'Analytics', 'popular': True},
    {'name': 'Fathom', 'description': 'Simple, privacy-focused analytics', 'url': 'https://usefathom.com/', 'category': 'Analytics'},
    {'name': 'Umami', 'description': 'Open-source, privacy-focused web analytics', 'url': 'https://umami.is/', 'category': 'Analytics', 'popular': True},
    {'name': 'Google Analytics', 'description': 'Web analytics service by Google', 'url': 'https://analytics.google.com/', 'category': 'Analytics', 'popular': True},
    {'name': 'Segment', 'description': 'Customer data platform', 'url': 'https://segment.com/', 'category': 'Analytics', 'popular': True},
    {'name': 'Heap', 'description': 'Digital insights platform', 'url': 'https://heap.io/', 'category': 'Analytics'},
    {'name': 'Hotjar', 'description': 'Behavior analytics and feedback platform', 'url': 'https://www.hotjar.com/', 'category': 'Analytics', 'popular': True},
    {'name': 'FullStory', 'description': 'Digital experience analytics', 'url': 'https://www.fullstory.com/', 'category': 'Analytics'},
    {'name': 'LogRocket', 'description': 'Session replay and product analytics', 'url': 'https://logrocket.com/', 'category': 'Analytics'},
    {'name': 'Matomo', 'description': 'Open-source web analytics platform', 'url': 'https://matomo.org/', 'category': 'Analytics'},
    {'name': 'Pirsch', 'description': 'Privacy-friendly web analytics', 'url': 'https://pirsch.io/', 'category': 'Analytics'},
    {'name': 'Simple Analytics', 'description': 'Privacy-first analytics', 'url': 'https://simpleanalytics.com/', 'category': 'Analytics'},
    {'name': 'Splitbee', 'description': 'Analytics and A/B testing', 'url': 'https://splitbee.io/', 'category': 'Analytics'},
    {'name': 'June', 'description': 'Product analytics for B2B SaaS', 'url': 'https://www.june.so/', 'category': 'Analytics'},
]

# =============================================================================
# CDN
# =============================================================================
cdn = [
    {'name': 'Cloudflare', 'description': 'Global CDN and security platform', 'url': 'https://www.cloudflare.com/', 'category': 'CDN', 'popular': True},
    {'name': 'Fastly', 'description': 'Edge cloud platform and CDN', 'url': 'https://www.fastly.com/', 'category': 'CDN', 'popular': True},
    {'name': 'Amazon CloudFront', 'description': 'Content delivery network by AWS', 'url': 'https://aws.amazon.com/cloudfront/', 'category': 'CDN', 'popular': True},
    {'name': 'Akamai', 'description': 'Global content delivery network', 'url': 'https://www.akamai.com/', 'category': 'CDN'},
    {'name': 'Bunny.net', 'description': 'Fast and affordable CDN', 'url': 'https://bunny.net/', 'category': 'CDN', 'popular': True},
    {'name': 'KeyCDN', 'description': 'High-performance content delivery network', 'url': 'https://www.keycdn.com/', 'category': 'CDN'},
    {'name': 'StackPath', 'description': 'Edge services and CDN', 'url': 'https://www.stackpath.com/', 'category': 'CDN'},
    {'name': 'Azure CDN', 'description': 'Content delivery network by Microsoft', 'url': 'https://azure.microsoft.com/en-us/products/cdn/', 'category': 'CDN'},
    {'name': 'Google Cloud CDN', 'description': 'Content delivery network by Google', 'url': 'https://cloud.google.com/cdn', 'category': 'CDN'},
    {'name': 'jsDelivr', 'description': 'Free CDN for open-source projects', 'url': 'https://www.jsdelivr.com/', 'category': 'CDN'},
    {'name': 'unpkg', 'description': 'Fast global CDN for npm packages', 'url': 'https://unpkg.com/', 'category': 'CDN'},
    {'name': 'cdnjs', 'description': 'Free CDN for JavaScript libraries', 'url': 'https://cdnjs.com/', 'category': 'CDN'},
    {'name': 'esm.sh', 'description': 'CDN for ES modules', 'url': 'https://esm.sh/', 'category': 'CDN'},
]

# =============================================================================
# PAYMENT
# =============================================================================
payment = [
    {'name': 'Stripe', 'description': 'Payment processing platform for developers', 'url': 'https://stripe.com/', 'category': 'Payment', 'popular': True},
    {'name': 'PayPal', 'description': 'Online payment system', 'url': 'https://www.paypal.com/', 'category': 'Payment', 'popular': True},
    {'name': 'LemonSqueezy', 'description': 'Merchant of record for digital products', 'url': 'https://www.lemonsqueezy.com/', 'category': 'Payment', 'popular': True},
    {'name': 'Paddle', 'description': 'Payment infrastructure for SaaS', 'url': 'https://www.paddle.com/', 'category': 'Payment', 'popular': True},
    {'name': 'Gumroad', 'description': 'E-commerce platform for creators', 'url': 'https://gumroad.com/', 'category': 'Payment'},
    {'name': 'Square', 'description': 'Financial services and payment platform', 'url': 'https://squareup.com/', 'category': 'Payment', 'popular': True},
    {'name': 'Braintree', 'description': 'Payment platform by PayPal', 'url': 'https://www.braintreepayments.com/', 'category': 'Payment'},
    {'name': 'Adyen', 'description': 'Global payment platform', 'url': 'https://www.adyen.com/', 'category': 'Payment'},
    {'name': 'Chargebee', 'description': 'Subscription billing and revenue management', 'url': 'https://www.chargebee.com/', 'category': 'Payment'},
    {'name': 'Recurly', 'description': 'Subscription management platform', 'url': 'https://recurly.com/', 'category': 'Payment'},
    {'name': 'Plaid', 'description': 'Financial data connectivity', 'url': 'https://plaid.com/', 'category': 'Payment', 'popular': True},
    {'name': 'Wise', 'description': 'International money transfers', 'url': 'https://wise.com/', 'category': 'Payment'},
    {'name': 'Ko-fi', 'description': 'Support platform for creators', 'url': 'https://ko-fi.com/', 'category': 'Payment'},
    {'name': 'Buy Me a Coffee', 'description': 'Support platform for creators', 'url': 'https://www.buymeacoffee.com/', 'category': 'Payment'},
    {'name': 'Polar', 'description': 'Funding platform for open-source', 'url': 'https://polar.sh/', 'category': 'Payment'},
    {'name': 'Open Collective', 'description': 'Financial platform for communities', 'url': 'https://opencollective.com/', 'category': 'Payment'},
]

# =============================================================================
# SERVERLESS
# =============================================================================
serverless = [
    {'name': 'AWS Lambda', 'description': 'Serverless compute service by Amazon', 'url': 'https://aws.amazon.com/lambda/', 'category': 'Serverless', 'popular': True},
    {'name': 'Cloudflare Workers', 'description': 'Serverless execution at the edge', 'url': 'https://workers.cloudflare.com/', 'category': 'Serverless', 'popular': True},
    {'name': 'Vercel Functions', 'description': 'Serverless functions on Vercel', 'url': 'https://vercel.com/docs/functions', 'category': 'Serverless', 'popular': True},
    {'name': 'Netlify Functions', 'description': 'Serverless functions on Netlify', 'url': 'https://www.netlify.com/products/functions/', 'category': 'Serverless'},
    {'name': 'Google Cloud Functions', 'description': 'Event-driven serverless compute', 'url': 'https://cloud.google.com/functions', 'category': 'Serverless'},
    {'name': 'Azure Functions', 'description': 'Serverless compute by Microsoft', 'url': 'https://azure.microsoft.com/en-us/products/functions/', 'category': 'Serverless'},
    {'name': 'Supabase Edge Functions', 'description': 'Serverless functions by Supabase', 'url': 'https://supabase.com/edge-functions', 'category': 'Serverless'},
    {'name': 'Deno Deploy', 'description': 'Serverless platform for Deno', 'url': 'https://deno.com/deploy', 'category': 'Serverless'},
    {'name': 'Fastly Compute', 'description': 'Serverless compute at the edge', 'url': 'https://www.fastly.com/products/edge-compute', 'category': 'Serverless'},
    {'name': 'AWS Fargate', 'description': 'Serverless containers on AWS', 'url': 'https://aws.amazon.com/fargate/', 'category': 'Serverless'},
    {'name': 'Google Cloud Run', 'description': 'Serverless containers by Google', 'url': 'https://cloud.google.com/run', 'category': 'Serverless', 'popular': True},
    {'name': 'Azure Container Apps', 'description': 'Serverless containers by Microsoft', 'url': 'https://azure.microsoft.com/en-us/products/container-apps/', 'category': 'Serverless'},
    {'name': 'Serverless Framework', 'description': 'Framework for building serverless apps', 'url': 'https://www.serverless.com/', 'category': 'Serverless'},
    {'name': 'SST', 'description': 'Build full-stack apps on AWS', 'url': 'https://sst.dev/', 'category': 'Serverless', 'popular': True},
    {'name': 'Architect', 'description': 'Build serverless apps on AWS', 'url': 'https://arc.codes/', 'category': 'Serverless'},
    {'name': 'Modal', 'description': 'Serverless cloud for AI/ML workloads', 'url': 'https://modal.com/', 'category': 'Serverless'},
    {'name': 'Beam', 'description': 'Serverless GPU cloud', 'url': 'https://beam.cloud/', 'category': 'Serverless'},
]

# =============================================================================
# RUNTIME
# =============================================================================
runtime = [
    {'name': 'Node.js', 'description': 'JavaScript runtime built on V8 engine', 'url': 'https://nodejs.org/', 'category': 'Runtime', 'popular': True},
    {'name': 'Deno', 'description': 'Secure runtime for JavaScript and TypeScript', 'url': 'https://deno.com/', 'category': 'Runtime', 'popular': True},
    {'name': 'Bun', 'description': 'Fast all-in-one JavaScript runtime', 'url': 'https://bun.sh/', 'category': 'Runtime', 'popular': True},
    {'name': 'JVM', 'description': 'Java Virtual Machine', 'url': 'https://www.java.com/', 'category': 'Runtime', 'popular': True},
    {'name': '.NET Runtime', 'description': 'Runtime for .NET applications', 'url': 'https://dotnet.microsoft.com/', 'category': 'Runtime', 'popular': True},
    {'name': 'Python Runtime', 'description': 'CPython interpreter', 'url': 'https://www.python.org/', 'category': 'Runtime', 'popular': True},
    {'name': 'GraalVM', 'description': 'High-performance polyglot VM', 'url': 'https://www.graalvm.org/', 'category': 'Runtime'},
    {'name': 'WASM Runtime', 'description': 'WebAssembly runtime environments', 'url': 'https://webassembly.org/', 'category': 'Runtime'},
    {'name': 'Wasmtime', 'description': 'Fast and secure WebAssembly runtime', 'url': 'https://wasmtime.dev/', 'category': 'Runtime'},
    {'name': 'WasmEdge', 'description': 'Lightweight WebAssembly runtime', 'url': 'https://wasmedge.org/', 'category': 'Runtime'},
    {'name': 'Spin', 'description': 'Framework for WebAssembly microservices', 'url': 'https://www.fermyon.com/spin', 'category': 'Runtime'},
]

# =============================================================================
# DESIGN TOOLS
# =============================================================================
design = [
    {'name': 'Figma', 'description': 'Collaborative interface design tool', 'url': 'https://www.figma.com/', 'category': 'Design', 'popular': True},
    {'name': 'Framer', 'description': 'Website builder with design tools', 'url': 'https://www.framer.com/', 'category': 'Design', 'popular': True},
    {'name': 'Sketch', 'description': 'Digital design toolkit for macOS', 'url': 'https://www.sketch.com/', 'category': 'Design', 'popular': True},
    {'name': 'Adobe XD', 'description': 'UI/UX design and prototyping tool', 'url': 'https://www.adobe.com/products/xd.html', 'category': 'Design'},
    {'name': 'Canva', 'description': 'Online graphic design platform', 'url': 'https://www.canva.com/', 'category': 'Design', 'popular': True},
    {'name': 'Penpot', 'description': 'Open-source design and prototyping platform', 'url': 'https://penpot.app/', 'category': 'Design'},
    {'name': 'Zeplin', 'description': 'Design handoff and collaboration', 'url': 'https://zeplin.io/', 'category': 'Design'},
    {'name': 'InVision', 'description': 'Digital product design platform', 'url': 'https://www.invisionapp.com/', 'category': 'Design'},
    {'name': 'Storybook', 'description': 'UI component workshop', 'url': 'https://storybook.js.org/', 'category': 'Design', 'popular': True},
    {'name': 'Chromatic', 'description': 'Visual testing for Storybook', 'url': 'https://www.chromatic.com/', 'category': 'Design'},
    {'name': 'Excalidraw', 'description': 'Virtual whiteboard for sketching', 'url': 'https://excalidraw.com/', 'category': 'Design', 'popular': True},
    {'name': 'tldraw', 'description': 'Collaborative digital whiteboard', 'url': 'https://www.tldraw.com/', 'category': 'Design'},
    {'name': 'Whimsical', 'description': 'Visual collaboration workspace', 'url': 'https://whimsical.com/', 'category': 'Design'},
    {'name': 'Lucidchart', 'description': 'Diagramming and visual collaboration', 'url': 'https://www.lucidchart.com/', 'category': 'Design'},
    {'name': 'Draw.io', 'description': 'Free online diagram software', 'url': 'https://www.drawio.com/', 'category': 'Design'},
    {'name': 'Eraser', 'description': 'Whiteboard for engineering teams', 'url': 'https://www.eraser.io/', 'category': 'Design'},
    {'name': 'Spline', 'description': '3D design tool for the web', 'url': 'https://spline.design/', 'category': 'Design'},
    {'name': 'Rive', 'description': 'Create interactive animations', 'url': 'https://rive.app/', 'category': 'Design'},
]

# =============================================================================
# COLLABORATION
# =============================================================================
collaboration = [
    {'name': 'Linear', 'description': 'Issue tracking for high-performance teams', 'url': 'https://linear.app/', 'category': 'Collaboration', 'popular': True},
    {'name': 'Notion', 'description': 'All-in-one workspace for notes and docs', 'url': 'https://www.notion.so/', 'category': 'Collaboration', 'popular': True},
    {'name': 'Slack', 'description': 'Business communication platform', 'url': 'https://slack.com/', 'category': 'Collaboration', 'popular': True},
    {'name': 'Discord', 'description': 'Voice, video, and text communication', 'url': 'https://discord.com/', 'category': 'Collaboration', 'popular': True},
    {'name': 'Jira', 'description': 'Issue and project tracking by Atlassian', 'url': 'https://www.atlassian.com/software/jira', 'category': 'Collaboration', 'popular': True},
    {'name': 'Trello', 'description': 'Visual project management tool', 'url': 'https://trello.com/', 'category': 'Collaboration'},
    {'name': 'Asana', 'description': 'Work management platform', 'url': 'https://asana.com/', 'category': 'Collaboration'},
    {'name': 'Monday.com', 'description': 'Work operating system', 'url': 'https://monday.com/', 'category': 'Collaboration'},
    {'name': 'ClickUp', 'description': 'All-in-one productivity platform', 'url': 'https://clickup.com/', 'category': 'Collaboration'},
    {'name': 'Basecamp', 'description': 'Project management and team communication', 'url': 'https://basecamp.com/', 'category': 'Collaboration'},
    {'name': 'Height', 'description': 'Autonomous project management tool', 'url': 'https://height.app/', 'category': 'Collaboration'},
    {'name': 'Plane', 'description': 'Open-source project management', 'url': 'https://plane.so/', 'category': 'Collaboration'},
    {'name': 'Loom', 'description': 'Async video messaging for teams', 'url': 'https://www.loom.com/', 'category': 'Collaboration'},
    {'name': 'Zoom', 'description': 'Video communications platform', 'url': 'https://zoom.us/', 'category': 'Collaboration', 'popular': True},
    {'name': 'Microsoft Teams', 'description': 'Business communication platform', 'url': 'https://www.microsoft.com/en-us/microsoft-teams/', 'category': 'Collaboration', 'popular': True},
    {'name': 'Gather', 'description': 'Virtual office for remote teams', 'url': 'https://www.gather.town/', 'category': 'Collaboration'},
    {'name': 'Tuple', 'description': 'Remote pair programming app', 'url': 'https://tuple.app/', 'category': 'Collaboration'},
    {'name': 'Pop', 'description': 'Screen sharing for developers', 'url': 'https://pop.com/', 'category': 'Collaboration'},
    {'name': 'Obsidian', 'description': 'Private knowledge base with Markdown', 'url': 'https://obsidian.md/', 'category': 'Collaboration', 'popular': True},
    {'name': 'Cron', 'description': 'Calendar for professionals', 'url': 'https://cron.com/', 'category': 'Collaboration'},
    {'name': 'Cal.com', 'description': 'Open-source scheduling infrastructure', 'url': 'https://cal.com/', 'category': 'Collaboration'},
    {'name': 'Calendly', 'description': 'Scheduling automation platform', 'url': 'https://calendly.com/', 'category': 'Collaboration'},
]

# =============================================================================
# DOCUMENTATION
# =============================================================================
documentation = [
    {'name': 'Docusaurus', 'description': 'Build optimized documentation websites', 'url': 'https://docusaurus.io/', 'category': 'Documentation', 'popular': True},
    {'name': 'Mintlify', 'description': 'Beautiful documentation for developers', 'url': 'https://mintlify.com/', 'category': 'Documentation', 'popular': True},
    {'name': 'GitBook', 'description': 'Documentation platform for teams', 'url': 'https://www.gitbook.com/', 'category': 'Documentation', 'popular': True},
    {'name': 'ReadMe', 'description': 'API documentation platform', 'url': 'https://readme.com/', 'category': 'Documentation'},
    {'name': 'VitePress', 'description': 'Vite-powered static site generator', 'url': 'https://vitepress.dev/', 'category': 'Documentation', 'popular': True},
    {'name': 'Nextra', 'description': 'Next.js-based documentation theme', 'url': 'https://nextra.site/', 'category': 'Documentation'},
    {'name': 'Starlight', 'description': 'Documentation template for Astro', 'url': 'https://starlight.astro.build/', 'category': 'Documentation'},
    {'name': 'MkDocs', 'description': 'Project documentation with Markdown', 'url': 'https://www.mkdocs.org/', 'category': 'Documentation'},
    {'name': 'Material for MkDocs', 'description': 'Material Design theme for MkDocs', 'url': 'https://squidfunk.github.io/mkdocs-material/', 'category': 'Documentation', 'popular': True},
    {'name': 'Sphinx', 'description': 'Documentation generator for Python', 'url': 'https://www.sphinx-doc.org/', 'category': 'Documentation'},
    {'name': 'Read the Docs', 'description': 'Documentation hosting platform', 'url': 'https://readthedocs.org/', 'category': 'Documentation'},
    {'name': 'Swagger UI', 'description': 'API documentation from OpenAPI specs', 'url': 'https://swagger.io/tools/swagger-ui/', 'category': 'Documentation'},
    {'name': 'Redoc', 'description': 'OpenAPI/Swagger documentation generator', 'url': 'https://redocly.com/redoc/', 'category': 'Documentation'},
    {'name': 'Stoplight', 'description': 'API design and documentation platform', 'url': 'https://stoplight.io/', 'category': 'Documentation'},
    {'name': 'Archbee', 'description': 'Documentation platform for teams', 'url': 'https://www.archbee.com/', 'category': 'Documentation'},
    {'name': 'Notion', 'description': 'All-in-one documentation workspace', 'url': 'https://www.notion.so/', 'category': 'Documentation'},
    {'name': 'Confluence', 'description': 'Team workspace by Atlassian', 'url': 'https://www.atlassian.com/software/confluence', 'category': 'Documentation'},
    {'name': 'Outline', 'description': 'Open-source team knowledge base', 'url': 'https://www.getoutline.com/', 'category': 'Documentation'},
    {'name': 'Slite', 'description': 'Knowledge base for teams', 'url': 'https://slite.com/', 'category': 'Documentation'},
]

# =============================================================================
# FEATURE FLAGS
# =============================================================================
feature_flags = [
    {'name': 'LaunchDarkly', 'description': 'Feature management platform', 'url': 'https://launchdarkly.com/', 'category': 'Feature Flags', 'popular': True},
    {'name': 'Flagsmith', 'description': 'Open-source feature flag management', 'url': 'https://www.flagsmith.com/', 'category': 'Feature Flags', 'popular': True},
    {'name': 'PostHog Feature Flags', 'description': 'Feature flags with PostHog', 'url': 'https://posthog.com/feature-flags', 'category': 'Feature Flags'},
    {'name': 'Split', 'description': 'Feature delivery platform', 'url': 'https://www.split.io/', 'category': 'Feature Flags'},
    {'name': 'ConfigCat', 'description': 'Feature flag service', 'url': 'https://configcat.com/', 'category': 'Feature Flags'},
    {'name': 'Unleash', 'description': 'Open-source feature flag management', 'url': 'https://www.getunleash.io/', 'category': 'Feature Flags'},
    {'name': 'GrowthBook', 'description': 'Open-source feature flags and A/B testing', 'url': 'https://www.growthbook.io/', 'category': 'Feature Flags', 'popular': True},
    {'name': 'Statsig', 'description': 'Feature flags and experimentation', 'url': 'https://statsig.com/', 'category': 'Feature Flags'},
    {'name': 'Eppo', 'description': 'Experimentation and feature flagging', 'url': 'https://www.geteppo.com/', 'category': 'Feature Flags'},
    {'name': 'DevCycle', 'description': 'Feature flag management platform', 'url': 'https://devcycle.com/', 'category': 'Feature Flags'},
    {'name': 'Flipt', 'description': 'Open-source feature flag solution', 'url': 'https://www.flipt.io/', 'category': 'Feature Flags'},
    {'name': 'Optimizely', 'description': 'Digital experience platform', 'url': 'https://www.optimizely.com/', 'category': 'Feature Flags'},
    {'name': 'VWO', 'description': 'A/B testing and experimentation', 'url': 'https://vwo.com/', 'category': 'Feature Flags'},
]

# =============================================================================
# AI/ML (Expanded)
# =============================================================================
ai_ml = [
    {'name': 'OpenAI API', 'description': 'API for GPT models and AI services', 'url': 'https://platform.openai.com/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Anthropic Claude', 'description': 'AI assistant API by Anthropic', 'url': 'https://www.anthropic.com/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Google Gemini', 'description': 'Multimodal AI model by Google', 'url': 'https://deepmind.google/technologies/gemini/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Hugging Face', 'description': 'Platform for machine learning models', 'url': 'https://huggingface.co/', 'category': 'AI/ML', 'popular': True},
    {'name': 'LangChain', 'description': 'Framework for LLM applications', 'url': 'https://www.langchain.com/', 'category': 'AI/ML', 'popular': True},
    {'name': 'LlamaIndex', 'description': 'Data framework for LLM applications', 'url': 'https://www.llamaindex.ai/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Ollama', 'description': 'Run LLMs locally', 'url': 'https://ollama.ai/', 'category': 'AI/ML', 'popular': True},
    {'name': 'LM Studio', 'description': 'Desktop app for local LLMs', 'url': 'https://lmstudio.ai/', 'category': 'AI/ML'},
    {'name': 'Replicate', 'description': 'Run ML models in the cloud', 'url': 'https://replicate.com/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Together AI', 'description': 'Fast inference for open-source models', 'url': 'https://www.together.ai/', 'category': 'AI/ML'},
    {'name': 'Groq', 'description': 'Fast AI inference', 'url': 'https://groq.com/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Fireworks AI', 'description': 'Fast generative AI platform', 'url': 'https://fireworks.ai/', 'category': 'AI/ML'},
    {'name': 'Anyscale', 'description': 'Platform for scaling AI applications', 'url': 'https://www.anyscale.com/', 'category': 'AI/ML'},
    {'name': 'TensorFlow', 'description': 'Open-source machine learning framework', 'url': 'https://www.tensorflow.org/', 'category': 'AI/ML', 'popular': True},
    {'name': 'PyTorch', 'description': 'Machine learning framework by Meta', 'url': 'https://pytorch.org/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Keras', 'description': 'Deep learning API for Python', 'url': 'https://keras.io/', 'category': 'AI/ML', 'popular': True},
    {'name': 'scikit-learn', 'description': 'Machine learning library for Python', 'url': 'https://scikit-learn.org/', 'category': 'AI/ML', 'popular': True},
    {'name': 'JAX', 'description': 'High-performance numerical computing', 'url': 'https://jax.readthedocs.io/', 'category': 'AI/ML'},
    {'name': 'MLflow', 'description': 'Platform for ML lifecycle management', 'url': 'https://mlflow.org/', 'category': 'AI/ML'},
    {'name': 'Weights & Biases', 'description': 'ML experiment tracking', 'url': 'https://wandb.ai/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Comet ML', 'description': 'ML experiment management', 'url': 'https://www.comet.com/', 'category': 'AI/ML'},
    {'name': 'DVC', 'description': 'Data version control for ML', 'url': 'https://dvc.org/', 'category': 'AI/ML'},
    {'name': 'Label Studio', 'description': 'Data labeling platform', 'url': 'https://labelstud.io/', 'category': 'AI/ML'},
    {'name': 'Roboflow', 'description': 'Computer vision developer tools', 'url': 'https://roboflow.com/', 'category': 'AI/ML'},
    {'name': 'Vercel AI SDK', 'description': 'Build AI-powered apps with React', 'url': 'https://sdk.vercel.ai/', 'category': 'AI/ML', 'popular': True},
    {'name': 'OpenRouter', 'description': 'Unified API for LLMs', 'url': 'https://openrouter.ai/', 'category': 'AI/ML'},
    {'name': 'Cohere', 'description': 'NLP API for enterprises', 'url': 'https://cohere.com/', 'category': 'AI/ML'},
    {'name': 'AI21 Labs', 'description': 'Foundation model provider', 'url': 'https://www.ai21.com/', 'category': 'AI/ML'},
    {'name': 'Stability AI', 'description': 'Open-source generative AI', 'url': 'https://stability.ai/', 'category': 'AI/ML'},
    {'name': 'Midjourney', 'description': 'AI image generation', 'url': 'https://www.midjourney.com/', 'category': 'AI/ML', 'popular': True},
    {'name': 'DALL-E', 'description': 'AI image generation by OpenAI', 'url': 'https://openai.com/dall-e-3', 'category': 'AI/ML', 'popular': True},
    {'name': 'ElevenLabs', 'description': 'AI voice generation', 'url': 'https://elevenlabs.io/', 'category': 'AI/ML'},
    {'name': 'Whisper', 'description': 'Speech recognition model by OpenAI', 'url': 'https://openai.com/research/whisper', 'category': 'AI/ML'},
    {'name': 'AssemblyAI', 'description': 'Speech-to-text API', 'url': 'https://www.assemblyai.com/', 'category': 'AI/ML'},
    {'name': 'Deepgram', 'description': 'Speech recognition platform', 'url': 'https://deepgram.com/', 'category': 'AI/ML'},
    {'name': 'Pinecone', 'description': 'Vector database for AI', 'url': 'https://www.pinecone.io/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Weaviate', 'description': 'Open-source vector database', 'url': 'https://weaviate.io/', 'category': 'AI/ML', 'popular': True},
    {'name': 'Qdrant', 'description': 'Vector similarity search engine', 'url': 'https://qdrant.tech/', 'category': 'AI/ML'},
    {'name': 'Milvus', 'description': 'Open-source vector database', 'url': 'https://milvus.io/', 'category': 'AI/ML'},
    {'name': 'Chroma', 'description': 'Open-source embedding database', 'url': 'https://www.trychroma.com/', 'category': 'AI/ML', 'popular': True},
    {'name': 'pgvector', 'description': 'Vector extension for PostgreSQL', 'url': 'https://github.com/pgvector/pgvector', 'category': 'AI/ML'},
    {'name': 'Haystack', 'description': 'LLM framework for building AI apps', 'url': 'https://haystack.deepset.ai/', 'category': 'AI/ML'},
    {'name': 'Semantic Kernel', 'description': 'AI orchestration SDK by Microsoft', 'url': 'https://learn.microsoft.com/en-us/semantic-kernel/', 'category': 'AI/ML'},
    {'name': 'AutoGPT', 'description': 'Autonomous AI agent', 'url': 'https://autogpt.net/', 'category': 'AI/ML'},
    {'name': 'CrewAI', 'description': 'Framework for orchestrating AI agents', 'url': 'https://www.crewai.com/', 'category': 'AI/ML'},
    {'name': 'Langfuse', 'description': 'LLM observability platform', 'url': 'https://langfuse.com/', 'category': 'AI/ML'},
    {'name': 'PromptLayer', 'description': 'Prompt engineering platform', 'url': 'https://promptlayer.com/', 'category': 'AI/ML'},
    {'name': 'Helicone', 'description': 'LLM observability and monitoring', 'url': 'https://www.helicone.ai/', 'category': 'AI/ML'},
]

# Add all categories
categories_added = {}
categories_added['Build Tool'] = add_items(build_tools)
categories_added['Package Manager'] = add_items(package_managers)
categories_added['Version Control'] = add_items(version_control)
categories_added['Message Queue'] = add_items(message_queues)
categories_added['Search'] = add_items(search)
categories_added['ORM'] = add_items(orm)
categories_added['Storage'] = add_items(storage)
categories_added['Email'] = add_items(email)
categories_added['Analytics'] = add_items(analytics)
categories_added['CDN'] = add_items(cdn)
categories_added['Payment'] = add_items(payment)
categories_added['Serverless'] = add_items(serverless)
categories_added['Runtime'] = add_items(runtime)
categories_added['Design'] = add_items(design)
categories_added['Collaboration'] = add_items(collaboration)
categories_added['Documentation'] = add_items(documentation)
categories_added['Feature Flags'] = add_items(feature_flags)
categories_added['AI/ML'] = add_items(ai_ml)

print("\n" + "="*50)
print("ITEMS ADDED BY CATEGORY")
print("="*50)
total_added = 0
for cat, count in sorted(categories_added.items(), key=lambda x: -x[1]):
    if count > 0:
        print(f"  {cat}: {count}")
        total_added += count
print(f"\n  TOTAL NEW ITEMS: {total_added}")

print(f"\nFinal count: {len(data)} items")

# Summary by category
from collections import Counter
cats = Counter(i.get('category', '') for i in data)
print("\n" + "="*50)
print("FINAL CATEGORY BREAKDOWN")
print("="*50)
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nSaved to data.json")
