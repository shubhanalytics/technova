// Client-side validation and local storage for contributions
(function () {
  const form = document.getElementById('contribForm');
  const result = document.getElementById('result');
  const clearBtn = document.getElementById('clearBtn');

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

  function validateTwitter(url) {
    if (!url) return true;
    try {
      const u = new URL(url);
      return /twitter.com$/i.test(u.hostname) || /t.co$/i.test(u.hostname);
    } catch (e) { return false; }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    result.textContent = '';

    const data = {
      siteName: form.siteName.value.trim(),
      siteUrl: form.siteUrl.value.trim(),
      category: form.category.value.trim(),
      subcategory: form.subcategory.value.trim(),
      owner: form.owner.value.trim(),
      email: form.email.value.trim(),
      twitter: form.twitter.value.trim(),
      notes: form.notes.value.trim(),
      submittedAt: new Date().toISOString()
    };

    if (!data.siteName) { showMessage('Please provide a site name.', false); return; }
    if (!data.siteUrl || !validateUrl(data.siteUrl)) { showMessage('Please enter a valid site URL (https://...).', false); return; }
    if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) { showMessage('Please enter a valid email address.', false); return; }
    if (!validateTwitter(data.twitter)) { showMessage('Twitter URL appears invalid.', false); return; }

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
      form.reset();
    } catch (err) {
      console.error(err);
      showMessage('Failed to save locally. Check browser storage settings.', false);
    }
  });

  clearBtn.addEventListener('click', () => form.reset());
})();
