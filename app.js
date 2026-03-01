/**
 * Technova - Lightweight Directory
 * Clean, fast, user-friendly
 */

// Constants
const DATA_URL = 'data.json';
const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

// Category Descriptions
const CATEGORY_DESCRIPTIONS = {
  'AI/ML': 'Artificial Intelligence and Machine Learning tools help build intelligent systems that can learn from data, recognize patterns, and make predictions. Used for chatbots, image recognition, recommendation engines, and automation.',
  'API': 'Application Programming Interfaces enable different software applications to communicate with each other. APIs let developers access external services, data, and functionality without building everything from scratch.',
  'Analytics': 'Analytics tools collect, measure, and analyze data to provide insights about user behavior, business performance, and system metrics. Essential for data-driven decision making.',
  'Authentication': 'Authentication services verify user identity and manage secure access to applications. They handle login, signup, password management, and multi-factor authentication.',
  'Backend': 'Backend frameworks and tools power the server-side of applications. They handle data processing, business logic, database operations, and API endpoints.',
  'Blockchain': 'Blockchain platforms enable decentralized, tamper-proof record keeping. Used for cryptocurrencies, smart contracts, NFTs, and secure transaction systems.',
  'Build Tool': 'Build tools automate the process of compiling, bundling, and optimizing code for production. They transform source files into deployable applications.',
  'Business': 'Business tools help organizations manage operations, finances, customer relationships, and internal processes more efficiently.',
  'CDN': 'Content Delivery Networks distribute content across global servers to deliver web pages, images, and media faster to users based on their geographic location.',
  'CLI': 'Command Line Interface tools let developers interact with systems through text commands. They automate tasks, manage files, and control applications from the terminal.',
  'CMS': 'Content Management Systems let users create, edit, and publish digital content without coding. Popular for websites, blogs, and documentation portals.',
  'Cloud': 'Cloud platforms provide on-demand computing resources including servers, storage, databases, and services over the internet, eliminating the need for physical infrastructure.',
  'Code Quality': 'Code quality tools analyze source code to find bugs, enforce coding standards, and improve maintainability. They help teams write cleaner, more reliable code.',
  'Collaboration': 'Collaboration tools help teams communicate, share files, manage projects, and work together effectively, whether in-office or remote.',
  'Container': 'Container technologies package applications with their dependencies into isolated units that run consistently across different environments.',
  'Data Engineering': 'Data engineering tools build and maintain systems for collecting, storing, and processing large volumes of data. They power data pipelines and ETL processes.',
  'Data Science': 'Data science tools help analyze and visualize complex datasets, build statistical models, and extract actionable insights from raw data.',
  'Database': 'Databases store, organize, and retrieve structured data efficiently. They range from relational SQL databases to NoSQL document stores and graph databases.',
  'Debugging': 'Debugging tools help developers find and fix errors in code. They provide breakpoints, variable inspection, stack traces, and performance profiling.',
  'Design': 'Design tools help create user interfaces, graphics, prototypes, and visual assets. Used by designers and developers to build beautiful, user-friendly products.',
  'DevOps': 'DevOps tools bridge development and operations, automating software delivery, infrastructure management, and deployment pipelines for faster releases.',
  'Documentation': 'Documentation tools help create, organize, and publish technical docs, user guides, and knowledge bases. Essential for onboarding and reference.',
  'Email': 'Email services handle sending, receiving, and managing electronic mail. They include transactional email APIs, marketing platforms, and email clients.',
  'Feature Flags': 'Feature flag tools let teams toggle features on/off without deploying new code. Used for gradual rollouts, A/B testing, and quick rollbacks.',
  'Frontend': 'Frontend frameworks and libraries build the user-facing part of web applications. They handle UI components, state management, and browser interactions.',
  'Game Engine': 'Game engines provide the core technology for building video games, including rendering, physics, audio, and input handling across platforms.',
  'Hardware': 'Hardware platforms and tools for physical computing devices, microcontrollers, and embedded systems development.',
  'Hosting': 'Hosting services provide servers and infrastructure to make websites and applications accessible on the internet.',
  'IDE/Editor': 'Integrated Development Environments and code editors provide features like syntax highlighting, autocomplete, debugging, and version control integration for writing code.',
  'IoT': 'Internet of Things platforms connect physical devices to the internet, enabling remote monitoring, control, and data collection from sensors and appliances.',
  'Library': 'Code libraries provide pre-written, reusable functions and components that developers can import into their projects to save time and effort.',
  'Low-Code': 'Low-code platforms let users build applications with minimal hand-coding through visual interfaces and drag-and-drop components.',
  'Message Queue': 'Message queues enable asynchronous communication between services by storing and forwarding messages. Essential for scalable, distributed systems.',
  'Mobile': 'Mobile development tools and frameworks build applications for iOS and Android devices, from native apps to cross-platform solutions.',
  'Monitoring': 'Monitoring tools track application health, performance metrics, and infrastructure status. They alert teams to issues before they impact users.',
  'ORM': 'Object-Relational Mappers let developers interact with databases using programming language objects instead of raw SQL queries.',
  'Operating System': 'Operating systems manage computer hardware and provide services for running applications. They\'re the foundation layer of any computing device.',
  'Package Manager': 'Package managers automate installing, updating, and managing software libraries and dependencies in development projects.',
  'Payment': 'Payment platforms process financial transactions, handle subscriptions, and manage billing for online businesses and applications.',
  'Programming Language': 'Programming languages are formal languages with specific syntax and rules used to write instructions that computers can execute.',
  'Runtime': 'Runtime environments execute code and provide the necessary services for programs to run, like memory management and system calls.',
  'Search': 'Search tools index and retrieve information from large datasets. They power everything from website search bars to enterprise knowledge discovery.',
  'Security': 'Security tools protect applications and data from threats. They handle vulnerability scanning, encryption, penetration testing, and compliance.',
  'Serverless': 'Serverless platforms run code without managing servers. They automatically scale based on demand and charge only for actual compute time used.',
  'Startup': 'Startup tools help founders launch and grow new businesses, from incorporation services to funding platforms and growth analytics.',
  'Storage': 'Storage services provide scalable solutions for saving files, media, backups, and application data in the cloud or on-premises.',
  'Testing': 'Testing tools help verify that software works correctly. They automate unit tests, integration tests, and end-to-end testing scenarios.',
  'VR/AR': 'Virtual Reality and Augmented Reality tools create immersive digital experiences that overlay or replace the physical world.',
  'Version Control': 'Version control systems track changes to code over time, enable collaboration, and let teams manage different versions of their projects.'
};

// State
let items = [];
let filteredItems = [];

// DOM Elements
const elements = {
  list: document.getElementById('list'),
  search: document.getElementById('search'),
  tabsContainer: document.getElementById('categoryTabs'),
  azBar: document.getElementById('azBar'),
  itemCount: document.getElementById('itemCount'),
  backToTop: document.getElementById('backToTop'),
};

// ============================================
// Security: URL Sanitization
// ============================================
function sanitizeUrl(url) {
  if (!url) return '#';
  try {
    const parsed = new URL(url, window.location.origin);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
      return parsed.href;
    }
  } catch (e) {}
  return '#';
}

// ============================================
// Escape HTML to prevent XSS
// ============================================
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ============================================
// Initialize Application
// ============================================
async function init() {
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    
    items = await response.json();
    if (!Array.isArray(items)) throw new Error('Invalid data format');
    
    buildTabs();
    buildAZBar();
    attachEvents();
    render();
  } catch (error) {
    console.error('Failed to load data:', error);
    elements.list.innerHTML = `
      <p class="muted" style="grid-column: 1 / -1; text-align: center; padding: 40px;">
        Failed to load data. Please ensure you're running a local server.
      </p>
    `;
  }
}

// ============================================
// Build Category Tabs
// ============================================
function buildTabs() {
  const allCategories = [...new Set(items.map(i => i.category).filter(Boolean))];
  
  // Sort categories alphabetically
  const categories = allCategories.sort((a, b) => a.localeCompare(b));
  
  const counts = {};
  items.forEach(item => {
    const cat = item.category || 'Uncategorized';
    counts[cat] = (counts[cat] || 0) + 1;
  });
  
  elements.tabsContainer.innerHTML = '';
  
  // All tab
  const allBtn = document.createElement('button');
  allBtn.className = 'tab active';
  allBtn.dataset.category = 'All';
  allBtn.innerHTML = `All <span class="tab-count">${items.length}</span>`;
  allBtn.type = 'button';
  allBtn.setAttribute('role', 'tab');
  allBtn.setAttribute('aria-selected', 'true');
  elements.tabsContainer.appendChild(allBtn);
  
  // Category tabs
  for (const category of categories) {
    const btn = document.createElement('button');
    btn.className = 'tab';
    btn.dataset.category = category;
    btn.innerHTML = `${category} <span class="tab-count">${counts[category] || 0}</span>`;
    btn.type = 'button';
    btn.setAttribute('role', 'tab');
    btn.setAttribute('aria-selected', 'false');
    elements.tabsContainer.appendChild(btn);
  }
}

// ============================================
// Build A-Z Quick Jump Bar
// ============================================
function buildAZBar() {
  elements.azBar.innerHTML = '';
  
  for (const letter of ALPHABET) {
    const btn = document.createElement('button');
    btn.className = 'az-letter';
    btn.textContent = letter;
    btn.type = 'button';
    btn.dataset.letter = letter;
    btn.setAttribute('aria-label', `Jump to ${letter === '#' ? 'numbers and symbols' : letter}`);
    elements.azBar.appendChild(btn);
  }
}

// ============================================
// Update A-Z Bar Active Letters
// ============================================
function updateAZBar() {
  const activeLetters = new Set();
  
  filteredItems.forEach(item => {
    const name = (item.name || '').trim();
    if (name) {
      const firstChar = name[0].toUpperCase();
      if (/[A-Z]/.test(firstChar)) {
        activeLetters.add(firstChar);
      } else {
        activeLetters.add('#');
      }
    }
  });
  
  elements.azBar.querySelectorAll('.az-letter').forEach(btn => {
    const letter = btn.dataset.letter;
    const hasItems = activeLetters.has(letter);
    btn.disabled = !hasItems;
    btn.classList.toggle('has-items', hasItems);
  });
}

// ============================================
// Update Tab Counts Based on Search
// ============================================
function updateTabCounts(filteredForCounts) {
  const counts = {};
  filteredForCounts.forEach(item => {
    const cat = item.category || 'Uncategorized';
    counts[cat] = (counts[cat] || 0) + 1;
  });
  
  elements.tabsContainer.querySelectorAll('.tab').forEach(tab => {
    const cat = tab.dataset.category;
    const countSpan = tab.querySelector('.tab-count');
    if (cat === 'All') {
      countSpan.textContent = filteredForCounts.length;
    } else {
      const count = counts[cat] || 0;
      countSpan.textContent = count;
      tab.disabled = count === 0;
    }
  });
}

// ============================================
// Update Item Count Display
// ============================================
function updateItemCount() {
  const total = items.length;
  const showing = filteredItems.length;
  
  if (showing === total) {
    elements.itemCount.textContent = `Showing ${total} items`;
  } else {
    elements.itemCount.textContent = `Showing ${showing} of ${total} items`;
  }
}

// ============================================
// Attach Event Listeners
// ============================================
function attachEvents() {
  // Search with debounce
  let searchTimeout;
  elements.search.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(render, 150);
  });
  
  // Tab clicks (delegation)
  elements.tabsContainer.addEventListener('click', (e) => {
    const tab = e.target.closest('.tab');
    if (!tab || tab.disabled) return;
    
    elements.tabsContainer.querySelectorAll('.tab').forEach(t => {
      t.classList.remove('active');
      t.setAttribute('aria-selected', 'false');
    });
    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');
    
    render();
  });
  
  // A-Z bar clicks
  elements.azBar.addEventListener('click', (e) => {
    const btn = e.target.closest('.az-letter');
    if (!btn || btn.disabled) return;
    
    const letter = btn.dataset.letter;
    jumpToLetter(letter);
  });
  
  // Back to top button
  elements.backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  
  // Show/hide back to top on scroll
  let scrollTimeout;
  window.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      elements.backToTop.hidden = window.scrollY < 400;
    }, 100);
  }, { passive: true });
}

// ============================================
// Jump to Letter
// ============================================
function jumpToLetter(letter) {
  const cards = elements.list.querySelectorAll('.card');
  
  for (const card of cards) {
    const name = card.querySelector('h3 a')?.textContent || '';
    const firstChar = name.trim()[0]?.toUpperCase() || '';
    
    let matches = false;
    if (letter === '#') {
      matches = !/[A-Z]/.test(firstChar);
    } else {
      matches = firstChar === letter;
    }
    
    if (matches) {
      card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      card.classList.add('highlight');
      setTimeout(() => card.classList.remove('highlight'), 1500);
      break;
    }
  }
}

// ============================================
// Main Render Function
// ============================================
function render() {
  const query = (elements.search.value || '').trim().toLowerCase();
  const activeTab = document.querySelector('.tab.active')?.dataset?.category || 'All';
  
  // Filter by search
  const filteredForCounts = items.filter(item => {
    if (query) {
      const searchText = `${item.name || ''} ${item.description || ''}`.toLowerCase();
      if (!searchText.includes(query)) return false;
    }
    return true;
  });
  
  // Update tab counts
  updateTabCounts(filteredForCounts);
  
  // Apply category filter
  filteredItems = filteredForCounts.filter(item => {
    if (activeTab !== 'All' && item.category !== activeTab) return false;
    return true;
  });
  
  // Sort alphabetically
  filteredItems.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
  
  // Update UI
  updateItemCount();
  updateAZBar();
  renderItems(activeTab);
}

// ============================================
// Render Items to DOM
// ============================================
function renderItems(activeTab) {
  elements.list.innerHTML = '';
  
  if (!filteredItems.length) {
    elements.list.innerHTML = `
      <p class="muted" style="grid-column: 1 / -1; text-align: center; padding: 40px;">
        No items found. Try a different search.
      </p>
    `;
    return;
  }
  
  // Show category description if viewing a specific category
  if (activeTab !== 'All' && CATEGORY_DESCRIPTIONS[activeTab]) {
    const descDiv = document.createElement('div');
    descDiv.className = 'category-description';
    descDiv.innerHTML = `
      <p>${escapeHtml(CATEGORY_DESCRIPTIONS[activeTab])}</p>
    `;
    elements.list.appendChild(descDiv);
  }
  
  // Group by category
  const grouped = {};
  for (const item of filteredItems) {
    const cat = item.category || 'Uncategorized';
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(item);
  }
  
  // Determine categories to render
  const categoriesToRender = activeTab === 'All' 
    ? Object.keys(grouped).sort() 
    : [activeTab];
  
  // Render each category
  for (const category of categoriesToRender) {
    if (!grouped[category]) continue;
    
    // Get all items and sort alphabetically
    const categoryItems = grouped[category].sort((a, b) => 
      (a.name || '').localeCompare(b.name || '')
    );
    
    // Category heading
    const heading = document.createElement('h2');
    heading.className = 'category-heading';
    heading.id = `cat-${category.replace(/\s+/g, '-').toLowerCase()}`;
    heading.textContent = category;
    elements.list.appendChild(heading);
    
    // Render all items alphabetically
    for (const item of categoryItems) {
      elements.list.appendChild(createCard(item, item.popular === true));
    }
  }
}

// ============================================
// Create Item Card
// ============================================
function createCard(item, isPopular = false) {
  const card = document.createElement('article');
  card.className = isPopular ? 'card popular' : 'card';
  
  // Clean up name
  const displayName = (item.name || '')
    .replace(/^['"\u201C\u201D`]+|['"\u201C\u201D`]+$/g, '')
    .trim() || 'Unnamed';
  
  const safeUrl = sanitizeUrl(item.url);
  const safeName = escapeHtml(displayName);
  const safeDesc = escapeHtml(item.description || '');
  const isValidUrl = safeUrl !== '#';
  
  // Status indicator (blinking dot)
  const isActive = item.status !== 'inactive';
  const statusDot = isActive
    ? `<span class="status-dot active" title="Active - Link verified"></span>`
    : `<span class="status-dot inactive" title="Inactive - Historical/Legacy project"></span>`;
  
  // External link icon
  const linkIcon = isValidUrl ? `<span class="link-icon" aria-hidden="true">↗</span>` : '';
  
  card.innerHTML = `
    <h3>
      ${statusDot}
      <a href="${safeUrl}" target="_blank" rel="noopener noreferrer" class="item-link">
        ${safeName}
        ${linkIcon}
      </a>
    </h3>
    ${safeDesc ? `<p class="description">${safeDesc}</p>` : ''}
  `;
  
  return card;
}

// ============================================
// Start Application
// ============================================
init();
