/*
  Supabase-backed community client with fallback to localStorage.
  If `window.SUPABASE_CONFIG.url` and `.anonKey` are set, this script will use Supabase.
  Otherwise it dynamically loads `scripts/community.js` (localStorage implementation).

  Requires modern browsers (ES modules) when using Supabase client via CDN.
*/
(async function(){
  const cfg = window.SUPABASE_CONFIG || {};
  if(!cfg.url || !cfg.anonKey){
    // fallback: load local community.js (already present)
    const s = document.createElement('script');
    s.src = 'scripts/community.js'; s.defer = true; document.body.appendChild(s);
    return;
  }

  // Use Supabase client via CDN ESM
  const { createClient } = await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm');
  const supabase = createClient(cfg.url, cfg.anonKey);

  function uid(pref='id'){ return pref + '_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2,8); }

  async function fetchDiscussions(){
    const { data, error } = await supabase.from('discussions').select('*').order('created_at', { ascending: false });
    if(error) throw error;
    return data || [];
  }

  async function createDiscussion(d){
    const { error } = await supabase.from('discussions').insert([d]);
    if(error) throw error;
  }

  async function fetchComments(discussionId){
    const { data, error } = await supabase.from('comments').select('*').eq('discussion_id', discussionId).order('created_at', { ascending: true });
    if(error) throw error;
    return data || [];
  }

  async function deleteDiscussion(id){
    const { error } = await supabase.from('discussions').delete().eq('id', id);
    if(error) throw error;
  }
  async function deleteComment(id){
    const { error } = await supabase.from('comments').delete().eq('id', id);
    if(error) throw error;
  }
  async function updateDiscussion(id, patch){
    const { error } = await supabase.from('discussions').update(patch).eq('id', id);
    if(error) throw error;
  }
  async function updateComment(id, patch){
    const { error } = await supabase.from('comments').update(patch).eq('id', id);
    if(error) throw error;
  }

  async function exportAll(){
    const d = await supabase.from('discussions').select('*');
    const c = await supabase.from('comments').select('*');
    return { discussions: d.data||[], comments: c.data||[] };
  }
  async function importAll(payload){
    // payload {discussions:[], comments:[]}
    if(payload.discussions && payload.discussions.length){
      await supabase.from('discussions').insert(payload.discussions, { upsert: false });
    }
    if(payload.comments && payload.comments.length){
      await supabase.from('comments').insert(payload.comments, { upsert: false });
    }
  }

  async function createComment(c){
    const { error } = await supabase.from('comments').insert([c]);
    if(error) throw error;
  }

  // Basic UI wiring — mirror structure from local implementation
  function renderList(discussions){
    const container = document.getElementById('discussions');
    container.innerHTML = '';
    if(!discussions.length){ container.innerHTML = '<p class="muted">No discussions yet. Start one!</p>'; return }
    discussions.forEach(d=>{
      const el = document.createElement('div'); el.className='card';
      const h = document.createElement('h3'); h.textContent = d.title;
      const meta = document.createElement('div'); meta.className='muted'; meta.style.marginBottom='8px';
      const author = d.author_value ? d.author_value : 'Anonymous';
      meta.textContent = `Started by ${author} · ${new Date(+d.created_at).toLocaleString()}`;
      const body = document.createElement('div'); body.className='muted'; body.textContent = d.body || '';
      const controls = document.createElement('div'); controls.style.marginTop='10px';
      const openBtn = document.createElement('button'); openBtn.className='btn-secondary'; openBtn.textContent='Open';
      openBtn.addEventListener('click', ()=> openDiscussion(d.id));
      controls.appendChild(openBtn);
      // admin controls (visible after enabling admin mode)
      if(window.__technova_admin_mode){
        const editBtn = document.createElement('button'); editBtn.className='btn-secondary'; editBtn.textContent='Edit';
        editBtn.addEventListener('click', async ()=>{
          const newTitle = prompt('Edit title', d.title); if(newTitle===null) return; const newBody = prompt('Edit body', d.body||''); if(newBody===null) return; await updateDiscussion(d.id, { title: newTitle, body: newBody }); loadAndRender();
        });
        const delBtn = document.createElement('button'); delBtn.className='btn-secondary'; delBtn.textContent='Delete';
        delBtn.addEventListener('click', async ()=>{ if(confirm('Delete discussion?')){ await deleteDiscussion(d.id); loadAndRender(); } });
        controls.appendChild(editBtn); controls.appendChild(delBtn);
      }
      el.appendChild(h); el.appendChild(meta); el.appendChild(body); el.appendChild(controls);
      container.appendChild(el);
    });
  }

  async function openDiscussion(id){
    const container = document.getElementById('discussions');
    container.innerHTML = '';
    const back = document.createElement('button'); back.className='btn-secondary'; back.textContent='Back to list'; back.addEventListener('click', loadAndRender);
    container.appendChild(back);
    const d = (await supabase.from('discussions').select('*').eq('id', id).single()).data;
    if(!d) return alert('Not found');
    const el = document.createElement('div'); el.className='content';
    const h = document.createElement('h2'); h.textContent = d.title;
    const meta = document.createElement('div'); meta.className='muted'; meta.textContent = `Started by ${d.author_value || 'Anonymous'} · ${new Date(+d.created_at).toLocaleString()}`;
    const body = document.createElement('div'); body.className='muted'; body.textContent = d.body || '';
    el.appendChild(h); el.appendChild(meta); el.appendChild(body);

    const commentsWrap = document.createElement('div'); commentsWrap.style.marginTop='14px';
    const appendCommentForm = document.createElement('div');
    appendCommentForm.innerHTML = `
      <h3>Post a comment</h3>
      <select id="cAuthorType"><option value="anonymous">Anonymous</option><option value="name">Your Name</option><option value="twitter">Twitter</option></select>
      <input id="cAuthorValue" placeholder="Name or @twitter" style="display:none;margin-top:8px;" />
      <textarea id="cText" placeholder="Write a comment"></textarea>
      <div class="form-actions"><button class="btn" id="postComment">Post comment</button></div>
    `;
    commentsWrap.appendChild(appendCommentForm);
    const list = document.createElement('div'); list.id='commentList'; list.style.marginTop='12px';
    commentsWrap.appendChild(list);
    el.appendChild(commentsWrap);
    container.appendChild(el);

    async function refresh(){
      list.innerHTML = '';
      const comments = await fetchComments(id);
      for(const c of comments.filter(x=>!x.parent_id)){
        renderComment(c, list, comments);
      }
    }

    function renderComment(c, parent, allComments){
      const card = document.createElement('div'); card.className='card'; card.style.marginBottom='8px';
      const h = document.createElement('div'); h.innerHTML = `<strong>${c.author_value || 'Anonymous'}</strong> · <span class="muted">${new Date(+c.created_at).toLocaleString()}</span>`;
      const txt = document.createElement('div'); txt.className='muted'; txt.textContent = c.text;
      const actions = document.createElement('div'); actions.style.marginTop='8px';
      const likeBtn = document.createElement('button'); likeBtn.className='btn-secondary'; likeBtn.textContent = `Like (${c.likes||0})`;
      likeBtn.addEventListener('click', async ()=>{ await supabase.from('comments').update({ likes: (c.likes||0)+1 }).eq('id', c.id); refresh(); });
      const replyBtn = document.createElement('button'); replyBtn.className='btn-secondary'; replyBtn.textContent='Reply';
      replyBtn.addEventListener('click', ()=> showReplyForm(c, card));
      if(window.__technova_admin_mode){
        const editC = document.createElement('button'); editC.className='btn-secondary'; editC.textContent='Edit';
        editC.addEventListener('click', async ()=>{ const text = prompt('Edit comment', c.text); if(text===null) return; await updateComment(c.id, { text }); refresh(); });
        const delC = document.createElement('button'); delC.className='btn-secondary'; delC.textContent='Delete';
        delC.addEventListener('click', async ()=>{ if(confirm('Delete comment?')){ await deleteComment(c.id); refresh(); } });
        actions.appendChild(editC); actions.appendChild(delC);
      }
      actions.appendChild(likeBtn); actions.appendChild(replyBtn);
      card.appendChild(h); card.appendChild(txt); card.appendChild(actions);

      // replies
      const replies = allComments.filter(x=>x.parent_id === c.id);
      if(replies.length){
        const repWrap = document.createElement('div'); repWrap.style.marginLeft='18px'; repWrap.style.marginTop='8px';
        replies.forEach(r=>{
          const rcard = document.createElement('div'); rcard.className='card'; rcard.style.marginBottom='6px';
          const rh = document.createElement('div'); rh.innerHTML = `<strong>${r.author_value || 'Anonymous'}</strong> · <span class="muted">${new Date(+r.created_at).toLocaleString()}</span>`;
          const rtxt = document.createElement('div'); rtxt.className='muted'; rtxt.textContent = r.text;
          const ractions = document.createElement('div'); ractions.style.marginTop='6px';
          const rlike = document.createElement('button'); rlike.className='btn-secondary'; rlike.textContent = `Like (${r.likes||0})`;
          rlike.addEventListener('click', async ()=>{ await supabase.from('comments').update({ likes: (r.likes||0)+1 }).eq('id', r.id); refresh(); });
          ractions.appendChild(rlike);
          rcard.appendChild(rh); rcard.appendChild(rtxt); rcard.appendChild(ractions);
          repWrap.appendChild(rcard);
        });
        card.appendChild(repWrap);
      }

      parent.appendChild(card);
    }

    function showReplyForm(comment, container){
      const form = document.createElement('div'); form.style.marginTop='8px';
      form.innerHTML = `
        <select class="rAuthorType"><option value="anonymous">Anonymous</option><option value="name">Your Name</option><option value="twitter">Twitter</option></select>
        <input class="rAuthorValue" placeholder="Name or @twitter" style="display:none;margin-top:8px;" />
        <textarea class="rText" placeholder="Reply"></textarea>
        <div class="form-actions"><button class="btn">Reply</button> <button class="btn-secondary">Cancel</button></div>
      `;
      container.appendChild(form);
      const sel = form.querySelector('.rAuthorType'); const val = form.querySelector('.rAuthorValue');
      sel.addEventListener('change', ()=>{ val.style.display = sel.value === 'anonymous' ? 'none' : 'block'; });
      form.querySelector('.btn-secondary').addEventListener('click', ()=>{ form.remove(); });
      form.querySelector('.btn').addEventListener('click', async ()=>{
        const at = sel.value; const av = val.value.trim(); const text = form.querySelector('.rText').value.trim();
        if(!text) return alert('Reply cannot be empty');
        const r = { id: uid('c'), discussion_id: id, parent_id: comment.id, text, author_type: at, author_value: av, likes:0, created_at: Date.now() };
        await createComment(r);
        refresh();
      });
    }

    document.getElementById('postComment').addEventListener('click', async ()=>{
      const at = document.getElementById('cAuthorType').value;
      const av = document.getElementById('cAuthorValue').value.trim();
      const text = document.getElementById('cText').value.trim();
      if(!text) return alert('Comment cannot be empty');
      const c = { id: uid('c'), discussion_id: id, parent_id: null, text, author_type: at, author_value: av, likes:0, created_at: Date.now() };
      await createComment(c); refresh(); document.getElementById('cText').value='';
    });

    document.getElementById('cAuthorType').addEventListener('change', function(){ const v = document.getElementById('cAuthorValue'); v.style.display = this.value === 'anonymous' ? 'none' : 'block'; });

    refresh();
  }

  async function loadAndRender(){
    const list = document.getElementById('discussions');
    list.innerHTML = '<p class="muted">Loading...</p>';
    const ds = await fetchDiscussions();
    renderList(ds);
  }

  // Wire creation
  document.addEventListener('DOMContentLoaded', ()=>{
    document.getElementById('createDiscussion').addEventListener('click', async ()=>{
      const title = document.getElementById('discussionTitle').value.trim(); if(!title) return alert('Title required');
      const at = document.getElementById('authorType').value; const av = document.getElementById('authorValue').value.trim(); const body = document.getElementById('discussionBody').value.trim();
      const d = { id: uid('d'), title, body, author_type: at, author_value: av, created_at: Date.now() };
      await createDiscussion(d);
      document.getElementById('discussionTitle').value=''; document.getElementById('discussionBody').value=''; document.getElementById('authorValue').value=''; document.getElementById('authorType').value='anonymous'; document.getElementById('authorValue').style.display='none';
      loadAndRender();
    });
    loadAndRender();

    // admin wiring
    const adminToggle = document.getElementById('adminToggle');
    const adminPanel = document.getElementById('adminPanel');
    const exportBtn = document.getElementById('exportData');
    const importBtn = document.getElementById('importData');
    const importFile = document.getElementById('importFile');
    const exitAdmin = document.getElementById('exitAdmin');
    window.__technova_admin_mode = false;
    adminToggle.addEventListener('click', ()=>{
      const token = prompt('Enter admin token (configured on site)');
      const cfg = window.SUPABASE_CONFIG || {};
      if(token && cfg.adminToken && token === cfg.adminToken){
        window.__technova_admin_mode = true; adminPanel.style.display = 'block'; loadAndRender();
      } else {
        alert('Invalid token');
      }
    });
    exitAdmin.addEventListener('click', ()=>{ window.__technova_admin_mode = false; adminPanel.style.display='none'; loadAndRender(); });
    exportBtn.addEventListener('click', async ()=>{
      const payload = await exportAll(); const blob = new Blob([JSON.stringify(payload, null, 2)], {type:'application/json'}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'discussions.export.json'; a.click(); URL.revokeObjectURL(url);
    });
    importBtn.addEventListener('click', async ()=>{
      const f = importFile.files[0]; if(!f) return alert('Select a JSON file to import');
      const reader = new FileReader(); reader.onload = async (e)=>{
        try{ const payload = JSON.parse(e.target.result); await importAll(payload); alert('Import complete'); loadAndRender(); } catch(err){ alert('Import failed: '+err.message); }
      }; reader.readAsText(f);
    });
  });

})();
