(() => {
    const root = document.documentElement;
    const system = window.matchMedia('(prefers-color-scheme: dark)');
    let preference = null;
    try {
        const saved = localStorage.getItem('theme');
        if (saved === 'dark' || saved === 'light') preference = saved;
    } catch (_) { /* Keep the toggle usable when storage is unavailable. */ }

    function applyTheme() {
        const dark = preference ? preference === 'dark' : system.matches;
        root.dataset.theme = dark ? 'dark' : 'light';
        const button = document.getElementById('theme-toggle');
        if (button) {
            button.hidden = false;
            button.textContent = dark ? 'Light mode' : 'Dark mode';
            button.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} mode`);
            button.setAttribute('aria-pressed', String(dark));
        }
    }

    applyTheme();
    system.addEventListener('change', applyTheme);
    window.addEventListener('storage', (event) => {
        if (event.key === 'theme' || event.key === null) {
            preference = event.newValue === 'dark' || event.newValue === 'light' ? event.newValue : null;
            applyTheme();
        }
    });
    document.addEventListener('DOMContentLoaded', () => {
        applyTheme();
        document.getElementById('theme-toggle')?.addEventListener('click', () => {
            preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
            try { localStorage.setItem('theme', preference); } catch (_) {}
            applyTheme();
        });
    });
})();
