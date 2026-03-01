#!/usr/bin/env python3
"""
Add comprehensive items for:
- Databases (more)
- Hosting platforms (new category)
- Authentication (new category)
- Libraries (new category)
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
            # Add verified flag for items with official URLs
            item['verified'] = True
            data.append(item)
            existing_names.add(item['name'].lower())
            added += 1
    return added

# =============================================================================
# MORE DATABASES
# =============================================================================
databases = [
    {'name': 'DynamoDB', 'description': 'Fully managed NoSQL database service by AWS', 'url': 'https://aws.amazon.com/dynamodb/', 'category': 'Database', 'popular': True},
    {'name': 'Supabase', 'description': 'Open-source Firebase alternative with Postgres database', 'url': 'https://supabase.com/', 'category': 'Database', 'popular': True},
    {'name': 'PlanetScale', 'description': 'Serverless MySQL platform with branching', 'url': 'https://planetscale.com/', 'category': 'Database', 'popular': True},
    {'name': 'Turso', 'description': 'Edge-hosted distributed database based on libSQL', 'url': 'https://turso.tech/', 'category': 'Database'},
    {'name': 'Neon', 'description': 'Serverless Postgres with autoscaling and branching', 'url': 'https://neon.tech/', 'category': 'Database', 'popular': True},
    {'name': 'CouchDB', 'description': 'Document-oriented NoSQL database with multi-master replication', 'url': 'https://couchdb.apache.org/', 'category': 'Database'},
    {'name': 'InfluxDB', 'description': 'Time series database for metrics, events, and analytics', 'url': 'https://www.influxdata.com/', 'category': 'Database'},
    {'name': 'TimescaleDB', 'description': 'Time series database built on PostgreSQL', 'url': 'https://www.timescale.com/', 'category': 'Database'},
    {'name': 'RethinkDB', 'description': 'Real-time database for the pushable web', 'url': 'https://rethinkdb.com/', 'category': 'Database'},
    {'name': 'ArangoDB', 'description': 'Multi-model database for graphs, documents, and key-values', 'url': 'https://www.arangodb.com/', 'category': 'Database'},
    {'name': 'ScyllaDB', 'description': 'High-performance NoSQL database compatible with Cassandra', 'url': 'https://www.scylladb.com/', 'category': 'Database'},
    {'name': 'Firebird', 'description': 'Open-source relational database with ANSI SQL support', 'url': 'https://firebirdsql.org/', 'category': 'Database'},
    {'name': 'Couchbase', 'description': 'Distributed NoSQL cloud database', 'url': 'https://www.couchbase.com/', 'category': 'Database'},
    {'name': 'Apache Druid', 'description': 'Real-time analytics database for fast OLAP queries', 'url': 'https://druid.apache.org/', 'category': 'Database'},
    {'name': 'QuestDB', 'description': 'High-performance time series database', 'url': 'https://questdb.io/', 'category': 'Database'},
    {'name': 'TiDB', 'description': 'Distributed SQL database compatible with MySQL', 'url': 'https://www.pingcap.com/tidb/', 'category': 'Database'},
    {'name': 'YugabyteDB', 'description': 'Distributed SQL database for cloud-native apps', 'url': 'https://www.yugabyte.com/', 'category': 'Database'},
    {'name': 'Dgraph', 'description': 'Native GraphQL database with graph backend', 'url': 'https://dgraph.io/', 'category': 'Database'},
    {'name': 'FaunaDB', 'description': 'Serverless document-relational database', 'url': 'https://fauna.com/', 'category': 'Database'},
    {'name': 'Vitess', 'description': 'Database clustering system for horizontal scaling of MySQL', 'url': 'https://vitess.io/', 'category': 'Database'},
    {'name': 'Memcached', 'description': 'Distributed memory object caching system', 'url': 'https://memcached.org/', 'category': 'Database'},
    {'name': 'Amazon Aurora', 'description': 'MySQL and PostgreSQL-compatible cloud database', 'url': 'https://aws.amazon.com/rds/aurora/', 'category': 'Database'},
    {'name': 'Cloud Spanner', 'description': 'Globally distributed relational database by Google', 'url': 'https://cloud.google.com/spanner', 'category': 'Database'},
    {'name': 'Azure Cosmos DB', 'description': 'Multi-model globally distributed database by Microsoft', 'url': 'https://azure.microsoft.com/en-us/products/cosmos-db/', 'category': 'Database'},
    {'name': 'Dolt', 'description': 'SQL database with Git-like version control', 'url': 'https://www.dolthub.com/', 'category': 'Database'},
    {'name': 'EdgeDB', 'description': 'Graph-relational database with declarative schema', 'url': 'https://www.edgedb.com/', 'category': 'Database'},
    {'name': 'SurrealDB', 'description': 'Multi-model cloud database for web, mobile, and serverless', 'url': 'https://surrealdb.com/', 'category': 'Database'},
]

# =============================================================================
# HOSTING PLATFORMS
# =============================================================================
hosting = [
    {'name': 'Vercel', 'description': 'Platform for frontend developers with serverless functions', 'url': 'https://vercel.com/', 'category': 'Hosting', 'popular': True},
    {'name': 'Netlify', 'description': 'Platform for deploying modern web projects', 'url': 'https://www.netlify.com/', 'category': 'Hosting', 'popular': True},
    {'name': 'Heroku', 'description': 'Cloud platform for deploying and scaling apps', 'url': 'https://www.heroku.com/', 'category': 'Hosting', 'popular': True},
    {'name': 'Render', 'description': 'Unified cloud platform to build and run apps', 'url': 'https://render.com/', 'category': 'Hosting', 'popular': True},
    {'name': 'Railway', 'description': 'Infrastructure platform for deploying apps instantly', 'url': 'https://railway.app/', 'category': 'Hosting', 'popular': True},
    {'name': 'Fly.io', 'description': 'Platform for running full-stack apps globally', 'url': 'https://fly.io/', 'category': 'Hosting', 'popular': True},
    {'name': 'Cloudflare Pages', 'description': 'JAMstack platform for frontend developers', 'url': 'https://pages.cloudflare.com/', 'category': 'Hosting', 'popular': True},
    {'name': 'GitHub Pages', 'description': 'Static site hosting directly from GitHub repositories', 'url': 'https://pages.github.com/', 'category': 'Hosting', 'popular': True},
    {'name': 'Firebase Hosting', 'description': 'Fast and secure hosting for web apps by Google', 'url': 'https://firebase.google.com/products/hosting', 'category': 'Hosting', 'popular': True},
    {'name': 'AWS Amplify Hosting', 'description': 'Fully managed hosting for full-stack web apps', 'url': 'https://aws.amazon.com/amplify/hosting/', 'category': 'Hosting'},
    {'name': 'Azure Static Web Apps', 'description': 'Service for hosting static web apps with serverless APIs', 'url': 'https://azure.microsoft.com/en-us/products/app-service/static/', 'category': 'Hosting'},
    {'name': 'Deno Deploy', 'description': 'Serverless platform for Deno applications', 'url': 'https://deno.com/deploy', 'category': 'Hosting'},
    {'name': 'Surge', 'description': 'Static web publishing for front-end developers', 'url': 'https://surge.sh/', 'category': 'Hosting'},
    {'name': 'Glitch', 'description': 'Collaborative platform for building web apps', 'url': 'https://glitch.com/', 'category': 'Hosting'},
    {'name': 'Replit', 'description': 'Browser-based IDE with instant hosting', 'url': 'https://replit.com/', 'category': 'Hosting'},
    {'name': 'CodeSandbox', 'description': 'Online IDE for rapid web development', 'url': 'https://codesandbox.io/', 'category': 'Hosting'},
    {'name': 'StackBlitz', 'description': 'Online IDE for web applications', 'url': 'https://stackblitz.com/', 'category': 'Hosting'},
    {'name': 'Cyclic', 'description': 'Serverless hosting for Node.js apps', 'url': 'https://www.cyclic.sh/', 'category': 'Hosting'},
    {'name': 'Koyeb', 'description': 'Serverless platform for deploying apps globally', 'url': 'https://www.koyeb.com/', 'category': 'Hosting'},
    {'name': 'Dokku', 'description': 'Open-source PaaS alternative to Heroku', 'url': 'https://dokku.com/', 'category': 'Hosting'},
    {'name': 'Platform.sh', 'description': 'End-to-end PaaS for web applications', 'url': 'https://platform.sh/', 'category': 'Hosting'},
    {'name': 'Coolify', 'description': 'Open-source self-hostable Heroku/Netlify alternative', 'url': 'https://coolify.io/', 'category': 'Hosting'},
    {'name': 'Caprover', 'description': 'Free and open-source PaaS', 'url': 'https://caprover.com/', 'category': 'Hosting'},
    {'name': 'Back4app', 'description': 'Backend-as-a-Service platform', 'url': 'https://www.back4app.com/', 'category': 'Hosting'},
]

# =============================================================================
# AUTHENTICATION
# =============================================================================
authentication = [
    {'name': 'Auth0', 'description': 'Identity platform for authentication and authorization', 'url': 'https://auth0.com/', 'category': 'Authentication', 'popular': True},
    {'name': 'Okta', 'description': 'Enterprise identity and access management', 'url': 'https://www.okta.com/', 'category': 'Authentication', 'popular': True},
    {'name': 'Clerk', 'description': 'Complete user management and authentication', 'url': 'https://clerk.com/', 'category': 'Authentication', 'popular': True},
    {'name': 'Firebase Authentication', 'description': 'Easy-to-use authentication by Google', 'url': 'https://firebase.google.com/products/auth', 'category': 'Authentication', 'popular': True},
    {'name': 'AWS Cognito', 'description': 'User identity and access management for web and mobile', 'url': 'https://aws.amazon.com/cognito/', 'category': 'Authentication', 'popular': True},
    {'name': 'Supabase Auth', 'description': 'Open-source authentication with Postgres', 'url': 'https://supabase.com/auth', 'category': 'Authentication', 'popular': True},
    {'name': 'NextAuth.js', 'description': 'Authentication for Next.js applications', 'url': 'https://next-auth.js.org/', 'category': 'Authentication', 'popular': True},
    {'name': 'Passport.js', 'description': 'Simple authentication middleware for Node.js', 'url': 'https://www.passportjs.org/', 'category': 'Authentication', 'popular': True},
    {'name': 'OAuth 2.0', 'description': 'Authorization framework for secure delegated access', 'url': 'https://oauth.net/2/', 'category': 'Authentication', 'popular': True},
    {'name': 'OpenID Connect', 'description': 'Identity layer on top of OAuth 2.0', 'url': 'https://openid.net/connect/', 'category': 'Authentication', 'popular': True},
    {'name': 'SAML', 'description': 'XML-based standard for enterprise SSO', 'url': 'https://en.wikipedia.org/wiki/SAML_2.0', 'category': 'Authentication'},
    {'name': 'JWT', 'description': 'JSON Web Tokens for secure information transmission', 'url': 'https://jwt.io/', 'category': 'Authentication', 'popular': True},
    {'name': 'Lucia', 'description': 'Simple session-based authentication library', 'url': 'https://lucia-auth.com/', 'category': 'Authentication'},
    {'name': 'Kinde', 'description': 'Authentication and user management platform', 'url': 'https://kinde.com/', 'category': 'Authentication'},
    {'name': 'Hanko', 'description': 'Passwordless authentication for web apps', 'url': 'https://www.hanko.io/', 'category': 'Authentication'},
    {'name': 'Stytch', 'description': 'Passwordless authentication API', 'url': 'https://stytch.com/', 'category': 'Authentication'},
    {'name': 'FusionAuth', 'description': 'Authentication and authorization platform', 'url': 'https://fusionauth.io/', 'category': 'Authentication'},
    {'name': 'Authelia', 'description': 'Open-source authentication and authorization server', 'url': 'https://www.authelia.com/', 'category': 'Authentication'},
    {'name': 'Ory', 'description': 'Open-source identity infrastructure', 'url': 'https://www.ory.sh/', 'category': 'Authentication'},
    {'name': 'SuperTokens', 'description': 'Open-source user authentication', 'url': 'https://supertokens.com/', 'category': 'Authentication'},
    {'name': 'WorkOS', 'description': 'Enterprise authentication and SSO', 'url': 'https://workos.com/', 'category': 'Authentication'},
    {'name': 'Frontegg', 'description': 'User management and authentication platform', 'url': 'https://frontegg.com/', 'category': 'Authentication'},
    {'name': 'Descope', 'description': 'Drag-and-drop authentication workflows', 'url': 'https://www.descope.com/', 'category': 'Authentication'},
    {'name': 'Magic', 'description': 'Passwordless authentication with magic links', 'url': 'https://magic.link/', 'category': 'Authentication'},
    {'name': 'WebAuthn', 'description': 'Web standard for passwordless authentication', 'url': 'https://webauthn.io/', 'category': 'Authentication'},
    {'name': 'Passkeys', 'description': 'FIDO2 passwordless authentication standard', 'url': 'https://passkeys.dev/', 'category': 'Authentication'},
]

# =============================================================================
# LIBRARIES (JavaScript, Python, etc.)
# =============================================================================
libraries = [
    # JavaScript Libraries
    {'name': 'Lodash', 'description': 'Modern JavaScript utility library for arrays, objects, and strings', 'url': 'https://lodash.com/', 'category': 'Library', 'popular': True},
    {'name': 'Axios', 'description': 'Promise-based HTTP client for browser and Node.js', 'url': 'https://axios-http.com/', 'category': 'Library', 'popular': True},
    {'name': 'Moment.js', 'description': 'Parse, validate, and display dates in JavaScript', 'url': 'https://momentjs.com/', 'category': 'Library'},
    {'name': 'date-fns', 'description': 'Modern JavaScript date utility library', 'url': 'https://date-fns.org/', 'category': 'Library', 'popular': True},
    {'name': 'Day.js', 'description': 'Lightweight alternative to Moment.js', 'url': 'https://day.js.org/', 'category': 'Library', 'popular': True},
    {'name': 'Ramda', 'description': 'Functional programming library for JavaScript', 'url': 'https://ramdajs.com/', 'category': 'Library'},
    {'name': 'RxJS', 'description': 'Reactive extensions library for JavaScript', 'url': 'https://rxjs.dev/', 'category': 'Library', 'popular': True},
    {'name': 'Immer', 'description': 'Immutable state management library', 'url': 'https://immerjs.github.io/immer/', 'category': 'Library', 'popular': True},
    {'name': 'Zod', 'description': 'TypeScript-first schema validation library', 'url': 'https://zod.dev/', 'category': 'Library', 'popular': True},
    {'name': 'Yup', 'description': 'JavaScript schema validation library', 'url': 'https://github.com/jquense/yup', 'category': 'Library'},
    {'name': 'Joi', 'description': 'Schema description and data validation for JavaScript', 'url': 'https://joi.dev/', 'category': 'Library'},
    {'name': 'Valibot', 'description': 'Modular schema validation library', 'url': 'https://valibot.dev/', 'category': 'Library'},
    {'name': 'uuid', 'description': 'RFC4122 UUID generation library', 'url': 'https://github.com/uuidjs/uuid', 'category': 'Library'},
    {'name': 'nanoid', 'description': 'Tiny unique string ID generator', 'url': 'https://zelark.github.io/nano-id-cc/', 'category': 'Library'},
    {'name': 'class-validator', 'description': 'Decorator-based validation for TypeScript', 'url': 'https://github.com/typestack/class-validator', 'category': 'Library'},
    
    # State Management
    {'name': 'Redux', 'description': 'Predictable state container for JavaScript apps', 'url': 'https://redux.js.org/', 'category': 'Library', 'popular': True},
    {'name': 'Zustand', 'description': 'Small, fast state management for React', 'url': 'https://zustand-demo.pmnd.rs/', 'category': 'Library', 'popular': True},
    {'name': 'Jotai', 'description': 'Primitive and flexible state management for React', 'url': 'https://jotai.org/', 'category': 'Library', 'popular': True},
    {'name': 'Recoil', 'description': 'State management library for React', 'url': 'https://recoiljs.org/', 'category': 'Library'},
    {'name': 'MobX', 'description': 'Simple, scalable state management', 'url': 'https://mobx.js.org/', 'category': 'Library'},
    {'name': 'Pinia', 'description': 'Intuitive state management for Vue.js', 'url': 'https://pinia.vuejs.org/', 'category': 'Library', 'popular': True},
    {'name': 'Vuex', 'description': 'State management pattern and library for Vue.js', 'url': 'https://vuex.vuejs.org/', 'category': 'Library'},
    {'name': 'XState', 'description': 'State machines and statecharts for JavaScript', 'url': 'https://xstate.js.org/', 'category': 'Library'},
    {'name': 'Valtio', 'description': 'Proxy-based state management for React', 'url': 'https://valtio.pmnd.rs/', 'category': 'Library'},
    {'name': 'TanStack Query', 'description': 'Powerful data fetching and caching library', 'url': 'https://tanstack.com/query/', 'category': 'Library', 'popular': True},
    {'name': 'SWR', 'description': 'React hooks for data fetching', 'url': 'https://swr.vercel.app/', 'category': 'Library', 'popular': True},
    
    # UI Components
    {'name': 'Tailwind CSS', 'description': 'Utility-first CSS framework', 'url': 'https://tailwindcss.com/', 'category': 'Library', 'popular': True},
    {'name': 'Bootstrap', 'description': 'Popular CSS framework for responsive design', 'url': 'https://getbootstrap.com/', 'category': 'Library', 'popular': True},
    {'name': 'Material UI', 'description': 'React components implementing Material Design', 'url': 'https://mui.com/', 'category': 'Library', 'popular': True},
    {'name': 'Chakra UI', 'description': 'Simple, modular React component library', 'url': 'https://chakra-ui.com/', 'category': 'Library', 'popular': True},
    {'name': 'Mantine', 'description': 'React components and hooks library', 'url': 'https://mantine.dev/', 'category': 'Library', 'popular': True},
    {'name': 'Ant Design', 'description': 'Enterprise-class React UI library', 'url': 'https://ant.design/', 'category': 'Library', 'popular': True},
    {'name': 'Radix UI', 'description': 'Unstyled, accessible React components', 'url': 'https://www.radix-ui.com/', 'category': 'Library', 'popular': True},
    {'name': 'shadcn/ui', 'description': 'Re-usable components built with Radix and Tailwind', 'url': 'https://ui.shadcn.com/', 'category': 'Library', 'popular': True},
    {'name': 'Headless UI', 'description': 'Unstyled, accessible UI components', 'url': 'https://headlessui.com/', 'category': 'Library'},
    {'name': 'DaisyUI', 'description': 'Tailwind CSS component library', 'url': 'https://daisyui.com/', 'category': 'Library'},
    {'name': 'PrimeReact', 'description': 'Rich UI component library for React', 'url': 'https://primereact.org/', 'category': 'Library'},
    {'name': 'Vuetify', 'description': 'Material Design component framework for Vue', 'url': 'https://vuetifyjs.com/', 'category': 'Library'},
    {'name': 'Quasar', 'description': 'Vue.js framework for building responsive apps', 'url': 'https://quasar.dev/', 'category': 'Library'},
    {'name': 'PrimeVue', 'description': 'UI component library for Vue.js', 'url': 'https://primevue.org/', 'category': 'Library'},
    {'name': 'Element Plus', 'description': 'Vue 3 UI library', 'url': 'https://element-plus.org/', 'category': 'Library'},
    {'name': 'Naive UI', 'description': 'Vue 3 component library', 'url': 'https://www.naiveui.com/', 'category': 'Library'},
    
    # Animation
    {'name': 'Framer Motion', 'description': 'Production-ready motion library for React', 'url': 'https://www.framer.com/motion/', 'category': 'Library', 'popular': True},
    {'name': 'GSAP', 'description': 'Professional-grade animation library', 'url': 'https://gsap.com/', 'category': 'Library', 'popular': True},
    {'name': 'Anime.js', 'description': 'Lightweight JavaScript animation library', 'url': 'https://animejs.com/', 'category': 'Library'},
    {'name': 'Lottie', 'description': 'Render After Effects animations in real-time', 'url': 'https://lottiefiles.com/', 'category': 'Library'},
    {'name': 'Three.js', 'description': '3D library for WebGL rendering', 'url': 'https://threejs.org/', 'category': 'Library', 'popular': True},
    {'name': 'React Spring', 'description': 'Spring-physics based animation library', 'url': 'https://react-spring.dev/', 'category': 'Library'},
    {'name': 'Motion One', 'description': 'Web Animations API-based animation library', 'url': 'https://motion.dev/', 'category': 'Library'},
    
    # Forms
    {'name': 'React Hook Form', 'description': 'Performant forms with easy validation', 'url': 'https://react-hook-form.com/', 'category': 'Library', 'popular': True},
    {'name': 'Formik', 'description': 'Build forms in React without tears', 'url': 'https://formik.org/', 'category': 'Library'},
    {'name': 'React Final Form', 'description': 'High-performance form state management', 'url': 'https://final-form.org/react', 'category': 'Library'},
    {'name': 'VeeValidate', 'description': 'Form validation for Vue.js', 'url': 'https://vee-validate.logaretm.com/', 'category': 'Library'},
    
    # Charts & Visualization
    {'name': 'Chart.js', 'description': 'Simple yet flexible JavaScript charting', 'url': 'https://www.chartjs.org/', 'category': 'Library', 'popular': True},
    {'name': 'D3.js', 'description': 'Data-driven documents for visualization', 'url': 'https://d3js.org/', 'category': 'Library', 'popular': True},
    {'name': 'Recharts', 'description': 'Composable charting library for React', 'url': 'https://recharts.org/', 'category': 'Library', 'popular': True},
    {'name': 'ECharts', 'description': 'Powerful charting and visualization library', 'url': 'https://echarts.apache.org/', 'category': 'Library'},
    {'name': 'Victory', 'description': 'React charting library by Formidable', 'url': 'https://formidable.com/open-source/victory/', 'category': 'Library'},
    {'name': 'Nivo', 'description': 'Data visualization components for React', 'url': 'https://nivo.rocks/', 'category': 'Library'},
    {'name': 'Visx', 'description': 'Collection of low-level visualization primitives', 'url': 'https://airbnb.io/visx/', 'category': 'Library'},
    {'name': 'ApexCharts', 'description': 'Modern charting library', 'url': 'https://apexcharts.com/', 'category': 'Library'},
    {'name': 'Plotly.js', 'description': 'Open-source graphing library', 'url': 'https://plotly.com/javascript/', 'category': 'Library'},
    
    # Tables
    {'name': 'TanStack Table', 'description': 'Headless UI for building tables and datagrids', 'url': 'https://tanstack.com/table/', 'category': 'Library', 'popular': True},
    {'name': 'AG Grid', 'description': 'High-performance JavaScript data grid', 'url': 'https://www.ag-grid.com/', 'category': 'Library', 'popular': True},
    {'name': 'Handsontable', 'description': 'Spreadsheet component for web apps', 'url': 'https://handsontable.com/', 'category': 'Library'},
    
    # Rich Text Editors
    {'name': 'TipTap', 'description': 'Headless editor framework based on ProseMirror', 'url': 'https://tiptap.dev/', 'category': 'Library', 'popular': True},
    {'name': 'Quill', 'description': 'Powerful rich text editor', 'url': 'https://quilljs.com/', 'category': 'Library'},
    {'name': 'Slate', 'description': 'Customizable rich text editor framework', 'url': 'https://www.slatejs.org/', 'category': 'Library'},
    {'name': 'ProseMirror', 'description': 'Toolkit for building rich text editors', 'url': 'https://prosemirror.net/', 'category': 'Library'},
    {'name': 'Lexical', 'description': 'Extensible text editor framework by Meta', 'url': 'https://lexical.dev/', 'category': 'Library'},
    {'name': 'Draft.js', 'description': 'Rich text editor framework for React', 'url': 'https://draftjs.org/', 'category': 'Library'},
    {'name': 'Editor.js', 'description': 'Block-styled editor for rich media stories', 'url': 'https://editorjs.io/', 'category': 'Library'},
    
    # Python Libraries
    {'name': 'NumPy', 'description': 'Fundamental package for scientific computing', 'url': 'https://numpy.org/', 'category': 'Library', 'popular': True},
    {'name': 'pandas', 'description': 'Data analysis and manipulation library', 'url': 'https://pandas.pydata.org/', 'category': 'Library', 'popular': True},
    {'name': 'Matplotlib', 'description': 'Comprehensive library for visualizations', 'url': 'https://matplotlib.org/', 'category': 'Library', 'popular': True},
    {'name': 'Seaborn', 'description': 'Statistical data visualization library', 'url': 'https://seaborn.pydata.org/', 'category': 'Library'},
    {'name': 'Plotly Python', 'description': 'Interactive graphing library for Python', 'url': 'https://plotly.com/python/', 'category': 'Library'},
    {'name': 'Requests', 'description': 'Simple HTTP library for Python', 'url': 'https://requests.readthedocs.io/', 'category': 'Library', 'popular': True},
    {'name': 'httpx', 'description': 'Next generation HTTP client for Python', 'url': 'https://www.python-httpx.org/', 'category': 'Library'},
    {'name': 'aiohttp', 'description': 'Async HTTP client/server framework', 'url': 'https://docs.aiohttp.org/', 'category': 'Library'},
    {'name': 'Beautiful Soup', 'description': 'HTML and XML parsing library', 'url': 'https://www.crummy.com/software/BeautifulSoup/', 'category': 'Library'},
    {'name': 'Scrapy', 'description': 'Web scraping framework for Python', 'url': 'https://scrapy.org/', 'category': 'Library'},
    {'name': 'SQLAlchemy', 'description': 'SQL toolkit and ORM for Python', 'url': 'https://www.sqlalchemy.org/', 'category': 'Library', 'popular': True},
    {'name': 'Pydantic', 'description': 'Data validation using Python type hints', 'url': 'https://pydantic.dev/', 'category': 'Library', 'popular': True},
    {'name': 'Celery', 'description': 'Distributed task queue for Python', 'url': 'https://docs.celeryq.dev/', 'category': 'Library'},
    {'name': 'Boto3', 'description': 'AWS SDK for Python', 'url': 'https://boto3.amazonaws.com/v1/documentation/api/latest/index.html', 'category': 'Library'},
    {'name': 'Click', 'description': 'Command line interface creation toolkit', 'url': 'https://click.palletsprojects.com/', 'category': 'Library'},
    {'name': 'Rich', 'description': 'Rich text and formatting in the terminal', 'url': 'https://rich.readthedocs.io/', 'category': 'Library'},
    {'name': 'Typer', 'description': 'CLI builder based on Python type hints', 'url': 'https://typer.tiangolo.com/', 'category': 'Library'},
    {'name': 'Polars', 'description': 'Fast DataFrame library for Rust and Python', 'url': 'https://www.pola.rs/', 'category': 'Library', 'popular': True},
    
    # Utilities
    {'name': 'Faker', 'description': 'Generate fake data for testing', 'url': 'https://fakerjs.dev/', 'category': 'Library'},
    {'name': 'Chance.js', 'description': 'Random generator helper library', 'url': 'https://chancejs.com/', 'category': 'Library'},
    {'name': 'validator.js', 'description': 'String validation and sanitization', 'url': 'https://github.com/validatorjs/validator.js', 'category': 'Library'},
    {'name': 'sanitize-html', 'description': 'Clean up user-submitted HTML', 'url': 'https://github.com/apostrophecms/sanitize-html', 'category': 'Library'},
    {'name': 'DOMPurify', 'description': 'XSS sanitizer for HTML and SVG', 'url': 'https://github.com/cure53/DOMPurify', 'category': 'Library'},
    {'name': 'marked', 'description': 'Fast Markdown parser and compiler', 'url': 'https://marked.js.org/', 'category': 'Library'},
    {'name': 'markdown-it', 'description': 'Markdown parser with plugins', 'url': 'https://markdown-it.github.io/', 'category': 'Library'},
    {'name': 'highlight.js', 'description': 'Syntax highlighting library', 'url': 'https://highlightjs.org/', 'category': 'Library'},
    {'name': 'Prism', 'description': 'Lightweight syntax highlighter', 'url': 'https://prismjs.com/', 'category': 'Library'},
    {'name': 'sharp', 'description': 'High-performance image processing for Node.js', 'url': 'https://sharp.pixelplumbing.com/', 'category': 'Library'},
    {'name': 'jimp', 'description': 'JavaScript Image Manipulation Program', 'url': 'https://jimp-dev.github.io/jimp/', 'category': 'Library'},
    {'name': 'pdf-lib', 'description': 'Create and modify PDF documents', 'url': 'https://pdf-lib.js.org/', 'category': 'Library'},
    {'name': 'ExcelJS', 'description': 'Excel workbook manager for Node.js', 'url': 'https://github.com/exceljs/exceljs', 'category': 'Library'},
    {'name': 'SheetJS', 'description': 'Spreadsheet data parser and writer', 'url': 'https://sheetjs.com/', 'category': 'Library'},
    {'name': 'Papa Parse', 'description': 'Fast and powerful CSV parser', 'url': 'https://www.papaparse.com/', 'category': 'Library'},
    {'name': 'Cheerio', 'description': 'Fast, flexible implementation of jQuery for server', 'url': 'https://cheerio.js.org/', 'category': 'Library'},
    {'name': 'Puppeteer', 'description': 'Headless Chrome Node.js API', 'url': 'https://pptr.dev/', 'category': 'Library'},
    {'name': 'Socket.IO', 'description': 'Real-time bidirectional event-based communication', 'url': 'https://socket.io/', 'category': 'Library', 'popular': True},
    {'name': 'ws', 'description': 'Simple WebSocket client and server', 'url': 'https://github.com/websockets/ws', 'category': 'Library'},
]

# Add all items
added_db = add_items(databases)
added_hosting = add_items(hosting)
added_auth = add_items(authentication)
added_libs = add_items(libraries)

print(f"\nAdded:")
print(f"  Databases: {added_db}")
print(f"  Hosting: {added_hosting}")
print(f"  Authentication: {added_auth}")
print(f"  Libraries: {added_libs}")
print(f"  Total new: {added_db + added_hosting + added_auth + added_libs}")

# Update category order in app.js awareness
print(f"\nFinal count: {len(data)} items")

# Summary by category
from collections import Counter
cats = Counter(i.get('category', '') for i in data)
print("\nCategory breakdown:")
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")

# Save
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nSaved to data.json")
