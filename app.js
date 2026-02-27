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
  populateFilters(items);
  buildTabs(items);
  attachEvents();
  render();
}

function buildTabs(data){
  const cats = Array.from(new Set(data.map(i=>i.category).filter(Boolean))).sort();
  tabsContainer.innerHTML = '';
  const total = data.length;
  const allBtn = document.createElement('button'); allBtn.className='tab active'; allBtn.dataset.category='All'; allBtn.textContent=`All (${total})`; tabsContainer.appendChild(allBtn);
  for(const c of cats){
    const b = document.createElement('button'); b.className='tab'; b.dataset.category = c; b.textContent = c; tabsContainer.appendChild(b);
  }
  tabs = Array.from(tabsContainer.querySelectorAll('.tab'));
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
  tabs.forEach(t=>t.addEventListener('click', onTabClick));
}

function onTabClick(e){
  tabs.forEach(t=>t.classList.remove('active'));
  e.currentTarget.classList.add('active');
  render();
}

function render(){
  const q = (searchEl.value||'').trim().toLowerCase();
  const sector = sectorSelect.value;
  const country = countrySelect.value;
  const activeTab = document.querySelector('.tab.active')?.dataset?.category || 'All';
  const sort = sortSelect.value;
  const domain = domainSelect?.value;

  let filtered = items.filter(it=>{
    if(activeTab !== 'All' && it.category !== activeTab) return false;
    if(sector && it.sector !== sector) return false;
    if(country && it.country !== country) return false;
    if(q){
      const hay = (it.name + ' ' + (it.description||'')).toLowerCase();
      if(!hay.includes(q)) return false;
    }
    return true;
  });

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

  for(const it of filtered){
    const card = document.createElement('article'); card.className='card';
    const h = document.createElement('h3');
    const a = document.createElement('a'); a.href = it.url; a.target='_blank'; a.rel='noopener noreferrer';
    const displayName = (it.name||'').replace(/^["\u201C\u201D'`]+|["\u201C\u201D'`]+$/g,'').trim();
    a.textContent = displayName || it.name;
    h.appendChild(a);
    const desc = document.createElement('div'); desc.className='muted'; desc.textContent = it.description || '';
    const meta = document.createElement('div'); meta.className='meta';
    const cat = document.createElement('span'); cat.className='pill'; cat.textContent = it.category;
    meta.appendChild(cat);
    if(it.sector){ const s = document.createElement('span'); s.className='muted'; s.textContent = it.sector; meta.appendChild(s); }
    if(it.country){ const c = document.createElement('span'); c.className='muted'; c.textContent = it.country; meta.appendChild(c); }
    if(it.domains && it.domains.length){ const ds = document.createElement('span'); ds.className='pill domain'; ds.textContent = it.domains.join(', '); meta.appendChild(ds); }
    card.appendChild(h); card.appendChild(desc); card.appendChild(meta);
    listEl.appendChild(card);
  }
}

init().catch(err=>{
  console.error(err);
  listEl.innerHTML = '<p class="muted">Failed to load data.json. Run a local server and reopen the page.</p>';
});
