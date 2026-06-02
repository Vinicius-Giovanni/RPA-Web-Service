const sidebarScrollTimeouts = new WeakMap();

document.querySelectorAll('.liquid-sidebar').forEach((sidebar) => {
    sidebar.addEventListener('scroll', () => {
        sidebar.classList.add('is-scrolling');
        clearTimeout(sidebarScrollTimeouts.get(sidebar));

        const timeout = setTimeout(() => {
            sidebar.classList.remove('is-scrolling');
            sidebarScrollTimeouts.delete(sidebar);
        }, 700);

        sidebarScrollTimeouts.set(sidebar, timeout);
    }, { passive: true });
});

document.querySelectorAll('.liquid-sidebar-layout').forEach((layout) => {
    const toggle = layout.querySelector('.liquid-sidebar-toggle');

    if (!toggle) {
        return;
    }

    toggle.addEventListener('click', () => {
        const isCollapsed = layout.classList.toggle('is-sidebar-collapsed');
        toggle.setAttribute('aria-expanded', String(!isCollapsed));
        toggle.setAttribute('aria-label', isCollapsed ? 'Mostrar menu lateral' : 'Esconder menu lateral',
        );
    })
})