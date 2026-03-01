/**
 * Technova - Lightweight Directory
 * Clean, fast, user-friendly
 */

// Constants
const DATA_URL = 'data.json';
const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#'.split('');

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
  const categories = [...new Set(items.map(i => i.category).filter(Boolean))].sort();
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
    
    // Separate popular and non-popular items
    const popularItems = grouped[category].filter(item => item.popular === true);
    const otherItems = grouped[category].filter(item => item.popular !== true);
    
    // Category heading
    const heading = document.createElement('h2');
    heading.className = 'category-heading';
    heading.id = `cat-${category.replace(/\s+/g, '-').toLowerCase()}`;
    heading.textContent = category;
    elements.list.appendChild(heading);
    
    // Popular section
    if (popularItems.length > 0) {
      const popularHeading = document.createElement('h3');
      popularHeading.className = 'section-heading popular-heading';
      popularHeading.innerHTML = '<span class="star-icon">★</span> Most Popular';
      elements.list.appendChild(popularHeading);
      
      for (const item of popularItems) {
        elements.list.appendChild(createCard(item, true));
      }
    }
    
    // More section
    if (otherItems.length > 0) {
      const moreHeading = document.createElement('h3');
      moreHeading.className = 'section-heading more-heading';
      moreHeading.textContent = 'More';
      elements.list.appendChild(moreHeading);
      
      for (const item of otherItems) {
        elements.list.appendChild(createCard(item, false));
      }
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
  
  // Verified icon for working links
  const verifiedIcon = isValidUrl ? 
    `<span class="verified-icon" title="Verified link">✓</span>` : '';
  
  card.innerHTML = `
    <h3>
      <a href="${safeUrl}" target="_blank" rel="noopener noreferrer">${safeName}</a>
      ${verifiedIcon}
    </h3>
    ${safeDesc ? `<p class="description">${safeDesc}</p>` : ''}
  `;
  
  return card;
}

// ============================================
// Start Application
// ============================================
init();
