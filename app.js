/**
 * Technova - Main Application
 * Clean, modern, secure implementation
 */

// Constants
const DATA_URL = 'data.json';

// State
let items = [];
let filteredItems = [];

// DOM Elements
const elements = {
  list: document.getElementById('list'),
  search: document.getElementById('search'),
  sectorSelect: document.getElementById('sectorSelect'),
  countrySelect: document.getElementById('countrySelect'),
  ownerSelect: document.getElementById('ownerSelect'),
  sortSelect: document.getElementById('sortSelect'),
  tabsContainer: document.getElementById('categoryTabs'),
  resetFilters: document.getElementById('resetFilters'),
};

// ============================================
// Security: URL Sanitization
// ============================================
function sanitizeUrl(url) {
  if (!url) return '#';
  
  try {
    const parsed = new URL(url, window.location.origin);
    // Only allow http and https protocols
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
      return parsed.href;
    }
  } catch (e) {
    // Invalid URL
  }
  
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
    
    populateFilters();
    buildTabs();
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
  const counts = items.reduce((acc, item) => {
    const cat = item.category || 'Uncategorized';
    acc[cat] = (acc[cat] || 0) + 1;
    return acc;
  }, {});
  
  elements.tabsContainer.innerHTML = '';
  
  // All tab
  const allBtn = document.createElement('button');
  allBtn.className = 'tab active';
  allBtn.dataset.category = 'All';
  allBtn.textContent = `All (${items.length})`;
  allBtn.type = 'button';
  allBtn.setAttribute('role', 'tab');
  allBtn.setAttribute('aria-selected', 'true');
  elements.tabsContainer.appendChild(allBtn);
  
  // Category tabs
  for (const category of categories) {
    const btn = document.createElement('button');
    btn.className = 'tab';
    btn.dataset.category = category;
    btn.textContent = `${category} (${counts[category] || 0})`;
    btn.type = 'button';
    btn.setAttribute('role', 'tab');
    btn.setAttribute('aria-selected', 'false');
    elements.tabsContainer.appendChild(btn);
  }
}

// ============================================
// Update Tab Counts Based on Filters
// ============================================
function updateTabCounts(filteredForCounts) {
  const counts = filteredForCounts.reduce((acc, item) => {
    const cat = item.category || 'Uncategorized';
    acc[cat] = (acc[cat] || 0) + 1;
    return acc;
  }, {});
  
  const tabs = elements.tabsContainer.querySelectorAll('.tab');
  tabs.forEach(tab => {
    const cat = tab.dataset.category;
    if (cat === 'All') {
      tab.textContent = `All (${filteredForCounts.length})`;
    } else {
      const count = counts[cat] || 0;
      tab.textContent = `${cat} (${count})`;
      tab.disabled = count === 0;
      tab.style.opacity = count ? '1' : '0.4';
    }
  });
}

// ============================================
// Populate Filter Dropdowns
// ============================================
function populateFilters() {
  const sectors = [...new Set(items.map(i => i.sector).filter(Boolean))].sort();
  const countries = [...new Set(items.map(i => i.country).filter(Boolean))].sort();
  const owners = [...new Set(items.map(i => i.owner).filter(Boolean))].sort();
  
  // Sectors
  sectors.forEach(sector => {
    const option = document.createElement('option');
    option.value = sector;
    option.textContent = sector;
    elements.sectorSelect.appendChild(option);
  });
  
  // Countries
  countries.forEach(country => {
    const option = document.createElement('option');
    option.value = country;
    option.textContent = country;
    elements.countrySelect.appendChild(option);
  });
  
  // Owners - only show dropdown if there are owners
  if (owners.length > 0) {
    elements.ownerSelect.hidden = false;
    owners.forEach(owner => {
      const option = document.createElement('option');
      option.value = owner;
      option.textContent = owner;
      elements.ownerSelect.appendChild(option);
    });
    
    // Special "Unowned items" option
    const othersOption = document.createElement('option');
    othersOption.value = '__UNOWNED__';
    othersOption.textContent = 'Unowned items';
    elements.ownerSelect.appendChild(othersOption);
  } else {
    // Hide if no owners
    elements.ownerSelect.hidden = true;
  }
}

// ============================================
// Reset All Filters
// ============================================
function resetAllFilters() {
  // Reset search
  elements.search.value = '';
  
  // Reset dropdowns
  elements.sectorSelect.value = '';
  elements.countrySelect.value = '';
  elements.ownerSelect.value = '';
  elements.sortSelect.value = 'name_asc';
  
  // Reset to All tab
  elements.tabsContainer.querySelectorAll('.tab').forEach(t => {
    t.classList.remove('active');
    t.setAttribute('aria-selected', 'false');
  });
  const allTab = elements.tabsContainer.querySelector('[data-category="All"]');
  if (allTab) {
    allTab.classList.add('active');
    allTab.setAttribute('aria-selected', 'true');
  }
  
  // Re-render
  render();
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
  
  // Filters
  elements.sectorSelect.addEventListener('change', render);
  elements.countrySelect.addEventListener('change', render);
  elements.ownerSelect.addEventListener('change', render);
  elements.sortSelect.addEventListener('change', render);
  
  // Reset filters
  elements.resetFilters.addEventListener('click', resetAllFilters);
  
  // Tab clicks (delegation)
  elements.tabsContainer.addEventListener('click', (e) => {
    const tab = e.target.closest('.tab');
    if (!tab || tab.disabled) return;
    
    // Update active state
    elements.tabsContainer.querySelectorAll('.tab').forEach(t => {
      t.classList.remove('active');
      t.setAttribute('aria-selected', 'false');
    });
    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');
    
    render();
  });
}

// ============================================
// Main Render Function
// ============================================
function render() {
  const query = (elements.search.value || '').trim().toLowerCase();
  const sector = elements.sectorSelect.value;
  const country = elements.countrySelect.value;
  const owner = elements.ownerSelect.value;
  const sort = elements.sortSelect.value;
  const activeTab = document.querySelector('.tab.active')?.dataset?.category || 'All';
  
  // Filter items (excluding category for tab counts)
  const filteredForCounts = items.filter(item => {
    // Sector filter
    if (sector && item.sector !== sector) return false;
    
    // Country filter
    if (country && item.country !== country) return false;
    
    // Owner filter
    if (owner) {
      if (owner === '__UNOWNED__') {
        if (item.owner) return false;
      } else {
        if (item.owner !== owner) return false;
      }
    }
    
    // Search filter
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
  
  // Sort
  switch (sort) {
    case 'name_asc':
      filteredItems.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
      break;
    case 'name_desc':
      filteredItems.sort((a, b) => (b.name || '').localeCompare(a.name || ''));
      break;
    case 'country_asc':
      filteredItems.sort((a, b) => (a.country || '').localeCompare(b.country || ''));
      break;
  }
  
  // Render
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
        No results found. Try adjusting your filters.
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
    heading.textContent = category;
    elements.list.appendChild(heading);
    
    // Popular section
    if (popularItems.length > 0) {
      const popularHeading = document.createElement('h3');
      popularHeading.className = 'section-heading popular-heading';
      popularHeading.innerHTML = '<span class="star-icon">★</span> Most Popular';
      elements.list.appendChild(popularHeading);
      
      for (const item of popularItems) {
        const card = createCard(item, true);
        elements.list.appendChild(card);
      }
    }
    
    // More section
    if (otherItems.length > 0) {
      const moreHeading = document.createElement('h3');
      moreHeading.className = 'section-heading more-heading';
      moreHeading.textContent = 'More';
      elements.list.appendChild(moreHeading);
      
      for (const item of otherItems) {
        const card = createCard(item, false);
        elements.list.appendChild(card);
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
  
  // Clean up name (remove quotes)
  const displayName = (item.name || '')
    .replace(/^['"\u201C\u201D`]+|['"\u201C\u201D`]+$/g, '')
    .trim() || 'Unnamed';
  
  // Build card HTML
  const safeUrl = sanitizeUrl(item.url);
  const safeName = escapeHtml(displayName);
  const safeDesc = escapeHtml(item.description || '');
  const yearHtml = item.year ? `<span class="year">· ${escapeHtml(String(item.year))}</span>` : '';
  
  card.innerHTML = `
    <h3>
      <a href="${safeUrl}" target="_blank" rel="noopener noreferrer">${safeName}</a>
      ${yearHtml}
    </h3>
    ${safeDesc ? `<div class="muted">${safeDesc}</div>` : ''}
  `;
  
  return card;
}

// ============================================
// Start Application
// ============================================
init();
