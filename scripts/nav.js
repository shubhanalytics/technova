document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('main-nav');
  const root = document.documentElement;
  if (!toggle || !nav) return;

  function closeNav() {
    nav.classList.remove('open');
    root.classList.remove('nav-open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  toggle.addEventListener('click', (e) => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('open', !expanded);
    root.classList.toggle('nav-open', !expanded);
  });

  // click outside to close
  document.addEventListener('click', (e) => {
    if (!nav.classList.contains('open')) return;
    if (nav.contains(e.target) || toggle.contains(e.target)) return;
    closeNav();
  });

  // close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      closeNav();
      toggle.focus();
    }
  });

  // ensure nav is hidden on resize to large screens
  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) {
      nav.classList.remove('open');
      root.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
});
