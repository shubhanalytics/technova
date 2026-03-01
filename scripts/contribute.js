// Client-side validation and local storage for contributions
(function () {
  const form = document.getElementById('contribForm');
  const result = document.getElementById('result');

  function showMessage(msg, ok = true) {
    result.textContent = msg;
    result.style.color = ok ? '' : 'var(--accent)';
  }

  function validateUrl(value) {
    try {
      const url = new URL(value);
      return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (e) {
      return false;
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    result.textContent = '';

    const data = {
      siteName: form.siteName.value.trim(),
      siteUrl: form.siteUrl.value.trim(),
      category: form.category.value.trim(),
      description: form.description.value.trim(),
      owner: form.owner.value.trim(),
      email: form.email.value.trim(),
      notes: form.notes.value.trim(),
      submittedAt: new Date().toISOString()
    };

    if (!data.siteName) { showMessage('Please provide a site name.', false); return; }
    if (!data.siteUrl || !validateUrl(data.siteUrl)) { showMessage('Please enter a valid site URL (https://...).', false); return; }
    if (!data.category) { showMessage('Please select a category.', false); return; }
    if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) { showMessage('Please enter a valid email address.', false); return; }

    // Optional reachability check — attempt a HEAD fetch, but ignore CORS failures.
    try {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), 2500);
      await fetch(data.siteUrl, { method: 'HEAD', mode: 'no-cors', signal: controller.signal });
      clearTimeout(id);
    } catch (err) {
      // ignore network/CORS errors; just warn
      console.warn('Reachability check failed or blocked by CORS', err);
    }

    // Save to localStorage
    try {
      const key = 'technova_contributions';
      const existing = JSON.parse(localStorage.getItem(key) || '[]');
      existing.push(data);
      localStorage.setItem(key, JSON.stringify(existing, null, 2));
      showMessage('Saved locally. Copy the JSON from localStorage to submit a PR or contact the maintainers.');

      // If Formspree is configured (replace YOUR_FORM_ID), attempt to POST the data there as well.
      try {
        // populate hidden replyto
        const reply = document.getElementById('_replyto');
        if (reply) reply.value = data.email || '';

        const action = (form.getAttribute('action') || '').trim();
        if (action && action.includes('formspree.io') && !action.includes('YOUR_FORM_ID')) {
          const formData = new FormData(form);
          // also append fields we store
          formData.set('siteName', data.siteName);
          formData.set('siteUrl', data.siteUrl);
          formData.set('category', data.category);
          formData.set('description', data.description);
          formData.set('owner', data.owner);
          formData.set('email', data.email);
          formData.set('notes', data.notes);

          const resp = await fetch(action, { method: 'POST', body: formData, headers: { 'Accept': 'application/json' } });
          if (resp.ok) {
            showMessage('Saved locally and submitted via Formspree. Thank you!');
          } else {
            console.warn('Formspree response', resp.status);
            showMessage('Saved locally. Formspree submission failed (check configuration).', false);
          }
        }
      } catch (err) {
        console.warn('Formspree submission attempt failed', err);
      }

      form.reset();
    } catch (err) {
      console.error(err);
      showMessage('Failed to save locally. Check browser storage settings.', false);
    }
  });
})();
