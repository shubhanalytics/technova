// Simple client-side community discussions using localStorage.
// Data structure:
// { discussions: [ {id, title, body, author:{type,value}, createdAt, comments: [ {id,parentId,text,author,likes,createdAt,replies:[] } ], likes:0 } ] }

(function(){
  const KEY = 'technova_community_v1';
  function uid(prefix='id'){ return prefix + '_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2,8); }

  function load(){ try{ return JSON.parse(localStorage.getItem(KEY)) || {discussions:[]} } catch(e){ return {discussions:[]} } }
  function save(data){ localStorage.setItem(KEY, JSON.stringify(data)); }

  function render(){
    const data = load();
    const container = document.getElementById('discussions');
    container.innerHTML = '';
    if(!data.discussions.length){ container.innerHTML = '<p class="muted">No discussions yet. Start one!</p>'; return }
    data.discussions.slice().reverse().forEach(d => {
      const el = document.createElement('div'); el.className = 'card';
      const h = document.createElement('h3'); h.textContent = d.title;
      const meta = document.createElement('div'); meta.className='muted'; meta.style.marginBottom='8px';
      const author = d.author && d.author.type !== 'anonymous' ? (d.author.type==='twitter'? d.author.value : d.author.value) : 'Anonymous';
      meta.textContent = `Started by ${author} · ${new Date(d.createdAt).toLocaleString()}`;
      const body = document.createElement('div'); body.className='muted'; body.textContent = d.body || '';
      const controls = document.createElement('div'); controls.style.marginTop='10px';
      const openBtn = document.createElement('button'); openBtn.className='btn-secondary'; openBtn.textContent='Open';
      openBtn.addEventListener('click', ()=> openDiscussion(d.id));
      controls.appendChild(openBtn);
      // admin controls (edit/delete)
      if(window.__technova_admin_mode){
        const editBtn = document.createElement('button'); editBtn.className='btn-secondary'; editBtn.textContent='Edit';
        editBtn.addEventListener('click', ()=>{ openEditDiscussion(d.id); });
        const delBtn = document.createElement('button'); delBtn.className='btn-secondary'; delBtn.textContent='Delete';
        delBtn.addEventListener('click', ()=>{ if(confirm('Delete discussion?')){ deleteDiscussion(d.id); render(); } });
        controls.appendChild(editBtn); controls.appendChild(delBtn);
      }
      el.appendChild(h); el.appendChild(meta); el.appendChild(body); el.appendChild(controls);
      container.appendChild(el);
    });
  }

  function openDiscussion(id){
    const data = load();
    const d = data.discussions.find(x=>x.id===id);
    if(!d) return alert('Discussion not found');
    // render overlay-like area below the list (simple approach)
    const container = document.getElementById('discussions');
    container.innerHTML = '';
    const back = document.createElement('button'); back.className='btn-secondary'; back.textContent='Back to list'; back.addEventListener('click', render);
    container.appendChild(back);
    const el = document.createElement('div'); el.className='content';
    const h = document.createElement('h2'); h.textContent = d.title;
    const meta = document.createElement('div'); meta.className='muted'; meta.textContent = `Started by ${d.author && d.author.type!=='anonymous' ? d.author.value : 'Anonymous'} · ${new Date(d.createdAt).toLocaleString()}`;
    const body = document.createElement('div'); body.className='muted'; body.textContent = d.body || '';
    el.appendChild(h); el.appendChild(meta); el.appendChild(body);

    // comments section
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

    function refreshComments(){
      list.innerHTML = '';
      (d.comments || []).forEach(c => renderComment(c, list, d));
    }

    function renderComment(c, parent, discussion){
      const card = document.createElement('div'); card.className='card'; card.style.marginBottom='8px';
      const h = document.createElement('div'); h.innerHTML = `<strong>${c.author && c.author.type!=='anonymous'? c.author.value : 'Anonymous'}</strong> · <span class="muted">${new Date(c.createdAt).toLocaleString()}</span>`;
      const txt = document.createElement('div'); txt.className='muted'; txt.textContent = c.text;
      const actions = document.createElement('div'); actions.style.marginTop='8px';
      const likeBtn = document.createElement('button'); likeBtn.className='btn-secondary'; likeBtn.textContent = `Like (${c.likes||0})`;
      likeBtn.addEventListener('click', ()=>{ c.likes = (c.likes||0)+1; save(data); refreshComments(); });
      const replyBtn = document.createElement('button'); replyBtn.className='btn-secondary'; replyBtn.textContent='Reply';
      replyBtn.addEventListener('click', ()=>{ showReplyForm(c, card, discussion); });
      actions.appendChild(likeBtn); actions.appendChild(replyBtn);
      if(window.__technova_admin_mode){
        const editC = document.createElement('button'); editC.className='btn-secondary'; editC.textContent='Edit';
        editC.addEventListener('click', ()=>{ openEditComment(c.id, discussion); });
        const delC = document.createElement('button'); delC.className='btn-secondary'; delC.textContent='Delete';
        delC.addEventListener('click', ()=>{ if(confirm('Delete comment?')){ deleteComment(c.id, discussion); save(data); refreshComments(); } });
        actions.appendChild(editC); actions.appendChild(delC);
      }
      card.appendChild(h); card.appendChild(txt); card.appendChild(actions);
      // render replies
      if(c.replies && c.replies.length){
        const repWrap = document.createElement('div'); repWrap.style.marginLeft='18px'; repWrap.style.marginTop='8px';
        c.replies.forEach(r=>{
          const rcard = document.createElement('div'); rcard.className='card'; rcard.style.marginBottom='6px';
          const rh = document.createElement('div'); rh.innerHTML = `<strong>${r.author && r.author.type!=='anonymous'? r.author.value : 'Anonymous'}</strong> · <span class="muted">${new Date(r.createdAt).toLocaleString()}</span>`;
          const rtxt = document.createElement('div'); rtxt.className='muted'; rtxt.textContent = r.text;
          const ractions = document.createElement('div'); ractions.style.marginTop='6px';
          const rlike = document.createElement('button'); rlike.className='btn-secondary'; rlike.textContent = `Like (${r.likes||0})`;
          rlike.addEventListener('click', ()=>{ r.likes = (r.likes||0)+1; save(data); refreshComments(); });
          ractions.appendChild(rlike);
          rcard.appendChild(rh); rcard.appendChild(rtxt); rcard.appendChild(ractions);
          repWrap.appendChild(rcard);
        });
        card.appendChild(repWrap);
      }

      parent.appendChild(card);
    }

  // Admin helper functions for localStorage
  function deleteDiscussion(id){
    const data = load(); data.discussions = data.discussions.filter(d=>d.id!==id); save(data);
  }
  function deleteComment(cid, discussion){
    discussion.comments = (discussion.comments||[]).filter(c=>c.id!==cid);
  }
  function openEditDiscussion(id){
    const data = load(); const d = data.discussions.find(x=>x.id===id); if(!d) return;
    const title = prompt('Edit title', d.title); if(title===null) return; const body = prompt('Edit body', d.body||''); if(body===null) return; d.title = title; d.body = body; save(data); render();
  }
  function openEditComment(cid, discussion){
    const data = load(); const c = (discussion.comments||[]).find(x=>x.id===cid); if(!c) return; const text = prompt('Edit comment', c.text); if(text===null) return; c.text = text; save(data);
  }

    function showReplyForm(comment, container, discussion){
      // simple inline reply form
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
      form.querySelector('.btn').addEventListener('click', ()=>{
        const at = sel.value; const av = val.value.trim(); const text = form.querySelector('.rText').value.trim();
        if(!text) return alert('Reply cannot be empty');
        const r = { id: uid('r'), parentId: comment.id, text, author: { type: at, value: av }, likes:0, createdAt: Date.now() };
        comment.replies = comment.replies || [];
        comment.replies.push(r);
        save(data); refreshComments();
      });
    }

    document.getElementById('postComment').addEventListener('click', ()=>{
      const at = document.getElementById('cAuthorType').value;
      const av = document.getElementById('cAuthorValue').value.trim();
      const text = document.getElementById('cText').value.trim();
      if(!text) return alert('Comment cannot be empty');
      const c = { id: uid('c'), parentId: null, text, author: { type: at, value: av }, likes:0, createdAt: Date.now(), replies: [] };
      d.comments = d.comments || [];
      d.comments.push(c);
      save(data); refreshComments(); document.getElementById('cText').value='';
    });

    // wire author type visibility
    document.getElementById('cAuthorType').addEventListener('change', function(){
      const v = document.getElementById('cAuthorValue'); v.style.display = this.value === 'anonymous' ? 'none' : 'block';
    });

    refreshComments();
  }

  // creation
  document.addEventListener('DOMContentLoaded', ()=>{
    document.getElementById('authorType').addEventListener('change', function(){
      const v = document.getElementById('authorValue'); v.style.display = this.value === 'anonymous' ? 'none' : 'block';
    });

    document.getElementById('createDiscussion').addEventListener('click', ()=>{
      const title = document.getElementById('discussionTitle').value.trim();
      if(!title) return alert('Title required');
      const at = document.getElementById('authorType').value;
      const av = document.getElementById('authorValue').value.trim();
      const body = document.getElementById('discussionBody').value.trim();
      const data = load();
      const d = { id: uid('d'), title, body, author: { type: at, value: av }, createdAt: Date.now(), comments: [], likes:0 };
      data.discussions = data.discussions || [];
      data.discussions.push(d);
      save(data);
      // reset
      document.getElementById('discussionTitle').value=''; document.getElementById('discussionBody').value=''; document.getElementById('authorValue').value=''; document.getElementById('authorType').value='anonymous'; document.getElementById('authorValue').style.display='none';
      render();
    });

    render();

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
        window.__technova_admin_mode = true; adminPanel.style.display = 'block'; render();
      } else if(token && !cfg.adminToken){
        // no server token configured — enable admin mode for session
        if(confirm('No admin token configured — enable admin mode for this session?')){ window.__technova_admin_mode = true; adminPanel.style.display='block'; render(); }
      } else {
        alert('Invalid token');
      }
    });
    exitAdmin.addEventListener('click', ()=>{ window.__technova_admin_mode = false; adminPanel.style.display='none'; render(); });
    exportBtn.addEventListener('click', ()=>{
      const data = load(); const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'discussions.export.json'; a.click(); URL.revokeObjectURL(url);
    });
    importBtn.addEventListener('click', ()=>{
      const f = importFile.files[0]; if(!f) return alert('Select a JSON file to import');
      const reader = new FileReader(); reader.onload = (e)=>{
        try{ const incoming = JSON.parse(e.target.result); if(!incoming.discussions) return alert('Invalid file'); const data = load(); // merge by id (skip duplicates)
          const existing = new Set((data.discussions||[]).map(x=>x.id)); incoming.discussions.forEach(d=>{ if(!existing.has(d.id)) data.discussions.push(d); }); save(data); render(); alert('Import complete'); } catch(err){ alert('Failed to import: '+err.message); }
      }; reader.readAsText(f);
    });
  });

})();
