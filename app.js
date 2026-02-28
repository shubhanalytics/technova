const DATA_URL = 'data.json';

let items = [];
const listEl = document.getElementById('list');
const searchEl = document.getElementById('search');
const sectorSelect = document.getElementById('sectorSelect');
const countrySelect = document.getElementById('countrySelect');
const sortSelect = document.getElementById('sortSelect');
const tabsContainer = document.getElementById('categoryTabs');
let tabs = [];
const domainSelect = document.getElementById('domainSelect');

async function init(){
  const res = await fetch(DATA_URL);
  items = await res.json();
  initTheme();
  initMotionToggle();
  populateFilters(items);
  buildTabs(items);
  attachEvents();
  render();
}

// Theme toggle: light/dark with localStorage
function initTheme(){
  const btn = document.getElementById('themeToggle');
  const saved = localStorage.getItem('technova:theme');
  if(saved === 'light') document.documentElement.classList.add('light');
  btn?.addEventListener('click', ()=>{
    const isLight = document.documentElement.classList.toggle('light');
    btn.setAttribute('aria-pressed', String(isLight));
    localStorage.setItem('technova:theme', isLight ? 'light' : 'dark');
  });
}

// reduce-motion toggle
function initMotionToggle(){
  const key = 'technova:reduced-motion';
  const saved = localStorage.getItem(key) === '1';
  if(saved) document.documentElement.classList.add('reduced-motion');
  // respect prefers-reduced-motion by default
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) document.documentElement.classList.add('reduced-motion');
  // expose a global toggle via data attribute for now
  window.toggleReducedMotion = ()=>{
    const is = document.documentElement.classList.toggle('reduced-motion');
    localStorage.setItem(key, is ? '1' : '0');
  };
}

// sanitize URLs to avoid javascript: or data: XSS
function safeUrl(u){
  try{
    const url = new URL(u, location.origin);
    if(['http:','https:'].includes(url.protocol)) return url.href;
  }catch(e){ /* ignore */ }
  return '#';
}

function buildTabs(data){
  const cats = Array.from(new Set(data.map(i=>i.category).filter(Boolean))).sort();
  tabsContainer.innerHTML = '';
  const counts = data.reduce((acc,it)=>{ const k = it.category||'Uncategorized'; acc[k]=(acc[k]||0)+1; return acc },{});
  const total = data.length;
  const allBtn = document.createElement('button'); allBtn.className='tab active'; allBtn.dataset.category='All'; allBtn.textContent=`All (${total})`; tabsContainer.appendChild(allBtn);
  for(const c of cats){
    const count = counts[c] || 0;
    const b = document.createElement('button'); b.className='tab'; b.dataset.category = c; b.textContent = `${c} (${count})`; tabsContainer.appendChild(b);
  }
  tabs = Array.from(tabsContainer.querySelectorAll('.tab'));
}

function updateTabCounts(filtered){
  const counts = filtered.reduce((acc,it)=>{ const k = it.category||'Uncategorized'; acc[k]=(acc[k]||0)+1; return acc },{});
  const total = filtered.length;
  tabs.forEach(t=>{
    const cat = t.dataset.category;
    if(!cat) return;
    if(cat === 'All'){
      t.textContent = `All (${total})`;
    } else {
      const cnt = counts[cat] || 0;
      t.textContent = `${cat} (${cnt})`;
      t.disabled = cnt === 0;
      t.style.opacity = cnt ? '1' : '0.5';
    }
  });
}

function populateFilters(data){
  const sectors = Array.from(new Set(data.map(i=>i.sector).filter(Boolean))).sort();
  const countries = Array.from(new Set(data.map(i=>i.country).filter(Boolean))).sort();
  const domains = Array.from(new Set((data.map(i=>i.domains||[])).flat().filter(Boolean))).sort();
  for(const s of sectors){
    const o = document.createElement('option'); o.value = s; o.textContent = s; sectorSelect.appendChild(o);
  }
  for(const c of countries){
    const o = document.createElement('option'); o.value = c; o.textContent = c; countrySelect.appendChild(o);
  }
  for(const d of domains){
    const o = document.createElement('option'); o.value = d; o.textContent = d; domainSelect.appendChild(o);
  }
}

function attachEvents(){
  searchEl.addEventListener('input', render);
  sectorSelect.addEventListener('change', render);
  countrySelect.addEventListener('change', render);
  sortSelect.addEventListener('change', render);
  domainSelect.addEventListener('change', render);
  // use event delegation on the tabs container so clicks always work
  tabsContainer.addEventListener('click', onTabContainerClick);
}

function onTabClick(e){
  tabs.forEach(t=>t.classList.remove('active'));
  e.currentTarget.classList.add('active');
  render();
}

function onTabContainerClick(e){
  const btn = e.target.closest('.tab');
  if(!btn || !tabsContainer.contains(btn)) return;
  if(btn.disabled) return;
  tabs.forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  render();
}

function render(){
  const q = (searchEl.value||'').trim().toLowerCase();
  const sector = sectorSelect.value;
  const country = countrySelect.value;
  const activeTab = document.querySelector('.tab.active')?.dataset?.category || 'All';
  const sort = sortSelect.value;
  const domain = domainSelect?.value;
  // items filtered by all controls except category (used to compute tab counts)
  const filteredForCounts = items.filter(it=>{
    if(sector && it.sector !== sector) return false;
    if(country && it.country !== country) return false;
    if(domain && !(it.domains||[]).includes(domain)) return false;
    if(q){
      const hay = (it.name + ' ' + (it.description||'')).toLowerCase();
      if(!hay.includes(q)) return false;
    }
    return true;
  });

  // apply category filter on top of the other filters for the visible list
  let filtered = filteredForCounts.filter(it=>{
    if(activeTab !== 'All' && it.category !== activeTab) return false;
    return true;
  });

  // update tab counts based on filters excluding the active category so tabs remain selectable
  updateTabCounts(filteredForCounts);

  if(sort === 'name_asc') filtered.sort((a,b)=>a.name.localeCompare(b.name));
  else if(sort === 'name_desc') filtered.sort((a,b)=>b.name.localeCompare(a.name));
  else if(sort === 'country_asc') filtered.sort((a,b)=> (a.country||'').localeCompare(b.country||''));
  else if(sort === 'domain_asc') filtered.sort((a,b)=> {
    const da = (a.domains && a.domains[0])||'';
    const db = (b.domains && b.domains[0])||'';
    return da.localeCompare(db);
  });

  listEl.innerHTML = '';
  if(!filtered.length){ listEl.innerHTML = '<p class="muted">No results</p>'; return }
  // group items by category -> subcategory
  function getSubcategory(it){
    if(it.domains && it.domains.length){
      const d = it.domains[0];
      if(d === 'AI/ML' && it.category === 'Framework') return 'ML frameworks';
      return d;
    }
    if(it.subcategory) return it.subcategory;
    return 'General';
  }

  const grouped = {};
  for(const it of filtered){
    const cat = it.category || 'Uncategorized';
    const sub = getSubcategory(it) || 'General';
    grouped[cat] = grouped[cat] || {};
    grouped[cat][sub] = grouped[cat][sub] || [];
    grouped[cat][sub].push(it);
  }

  // render grouped structure. If activeTab !== 'All' we only show that category
  const catsToRender = (activeTab === 'All') ? Object.keys(grouped).sort() : [activeTab];
  for(const catName of catsToRender){
    if(!grouped[catName]) continue;
    if(activeTab === 'All'){
      const catH = document.createElement('h2'); catH.textContent = catName; catH.style.marginTop = '18px'; listEl.appendChild(catH);
    }
    const subs = Object.keys(grouped[catName]).sort();
    for(const subName of subs){
      const subHeading = document.createElement('h3'); subHeading.textContent = subName; subHeading.className='muted'; subHeading.style.marginTop = '12px'; listEl.appendChild(subHeading);
      for(const it of grouped[catName][subName]){
        const card = document.createElement('article'); card.className='card';
        const h = document.createElement('h3');
        const a = document.createElement('a'); a.href = safeUrl(it.url || ''); a.target='_blank'; a.rel='noopener noreferrer';
        const displayName = (it.name||'').replace(/^['"\u201C\u201D`]+|['"\u201C\u201D`]+$/g,'').trim();
        a.textContent = displayName || it.name;
        h.appendChild(a);
        const desc = document.createElement('div'); desc.className='muted'; desc.textContent = it.description || '';
        const meta = document.createElement('div'); meta.className='meta';
        const cspan = document.createElement('span'); cspan.className='pill'; cspan.textContent = it.category;
        meta.appendChild(cspan);
        if(it.sector){ const s = document.createElement('span'); s.className='muted'; s.textContent = it.sector; meta.appendChild(s); }
        if(it.country){ const c = document.createElement('span'); c.className='muted'; c.textContent = it.country; meta.appendChild(c); }
        if(it.domains && it.domains.length){ const ds = document.createElement('span'); ds.className='pill domain'; ds.textContent = it.domains.join(', '); meta.appendChild(ds); }
        card.appendChild(h); card.appendChild(desc); card.appendChild(meta);
        listEl.appendChild(card);
      }
    }
  }
}

init().catch(err=>{
  console.error(err);
  listEl.innerHTML = '<p class="muted">Failed to load data.json. Run a local server and reopen the page.</p>';
});
