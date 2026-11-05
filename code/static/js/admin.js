(() => {
    'use strict';
    const key = 'eventa-theme';
    const modes = ['auto', 'light', 'dark'];
    const system = window.matchMedia('(prefers-color-scheme: dark)');
    let mode = 'auto';
    try { mode = localStorage.getItem(key) || 'auto'; } catch (_) {}
    if (!modes.includes(mode)) mode = 'auto';

    function apply() {
        const dark = mode === 'dark' || (mode === 'auto' && system.matches);
        document.documentElement.dataset.theme = dark ? 'dark' : 'light';
        const stylesheet = document.getElementById('jazzmin-dark-mode-theme');
        if (stylesheet) stylesheet.media = dark ? 'all' : 'not all';
        const lightStylesheet = document.getElementById('jazzmin-theme');
        if (lightStylesheet) lightStylesheet.media = dark ? 'not all' : 'all';
        if (document.body) {
            document.body.classList.toggle('dark-mode', dark);
            document.body.classList.toggle('theme-dark', dark);
            document.body.classList.toggle('theme-darkly', dark);
            document.body.classList.toggle('theme-flatly', !dark);
            const navbar = document.getElementById('jazzy-navbar');
            if (navbar) {
                navbar.classList.toggle('navbar-dark', dark);
                navbar.classList.toggle('navbar-light', !dark);
                navbar.classList.toggle('navbar-white', !dark);
            }
            const sidebar = document.getElementById('jazzy-sidebar');
            if (sidebar) {
                sidebar.classList.toggle('sidebar-dark-primary', dark);
                sidebar.classList.toggle('sidebar-light-primary', !dark);
            }
            document.querySelectorAll('.login-logo source').forEach((source) => {
                source.media = dark ? 'all' : 'not all';
            });
        }
        document.querySelectorAll('#eventa-theme button').forEach((button) => {
            const selected = button.dataset.mode === mode;
            button.classList.toggle('active', selected);
            button.setAttribute('aria-pressed', String(selected));
        });
    }
    apply();
    system.addEventListener('change', apply);
    window.addEventListener('storage', (event) => {
        if (event.key === key || event.key === null) {
            mode = modes.includes(event.newValue) ? event.newValue : 'auto';
            apply();
        }
    });
    function initialize() {
        const container = document.querySelector('#jazzy-navbar .navbar-nav.ml-auto') || document.querySelector('.login-box');
        if (container && !document.getElementById('eventa-theme')) {
            const control = document.createElement(container.tagName === 'UL' ? 'li' : 'div');
            control.className = 'eventa-theme-control';
            const group = document.createElement('div');
            group.id = 'eventa-theme';
            group.className = 'eventa-theme-buttons';
            group.setAttribute('role', 'group');
            group.setAttribute('aria-label', 'Alternar tema');
            [['auto', 'Automático', 'desktop'], ['light', 'Claro', 'sun'], ['dark', 'Escuro', 'moon']].forEach(([value, text, icon]) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'eventa-theme-button';
                button.dataset.mode = value;
                button.title = `Tema ${text.toLowerCase()}`;
                button.setAttribute('aria-label', `Tema ${text.toLowerCase()}`);
                const symbol = document.createElement('i');
                symbol.className = `fas fa-${icon}`;
                symbol.setAttribute('aria-hidden', 'true');
                button.append(symbol);
                button.addEventListener('click', () => {
                    mode = value;
                    try { localStorage.setItem(key, mode); } catch (_) {}
                    apply();
                });
                group.append(button);
            });
            control.append(group);
            container.prepend(control);
        }
        apply();
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize, { once: true });
    } else {
        initialize();
    }
})();
