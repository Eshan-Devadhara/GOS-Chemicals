/* ==========================================================================
   Nav & Footer — GOS Chemicals
   Renders shared header/nav and footer from /api/settings on every page.
   Provides mobile nav accessibility, keyboard trap/close, and scroll state.
   ========================================================================== */

const DEFAULT_SETTINGS = {
    site_name: 'GOS Chemicals',
    site_tagline: 'Specialty Chemicals Manufactured & Exported from India',
    cta_primary_label: 'Request a Quote',
    contact_email: 'info@goschemicals.com',
    contact_phone: '+91-XXXXXXXXXX',
    contact_address: 'Gujarat, India'
};

document.addEventListener('DOMContentLoaded', async () => {
    // Render immediately from cached settings or defaults (0ms visual delay)
    const initialSettings = (typeof apiGetCachedSync === 'function' ? apiGetCachedSync('/settings') : null) || DEFAULT_SETTINGS;
    renderHeader(initialSettings);
    renderFooter(initialSettings);
    initHeaderScroll();

    // Revalidate settings in background
    try {
        const freshSettings = await apiGet('/settings');
        if (freshSettings && JSON.stringify(freshSettings) !== JSON.stringify(initialSettings)) {
            renderHeader(freshSettings);
            renderFooter(freshSettings);
        }
    } catch (e) {
        // Fallback already rendered
    }
});

function initHeaderScroll() {
    const header = document.getElementById('site-header');
    if (!header) return;

    const onScroll = () => {
        if (window.scrollY > 8) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}

function renderHeader(s) {
    const header = document.getElementById('site-header');
    if (!header) return;

    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    const navLinks = [
        { href: 'index.html', label: 'Home' },
        { href: 'products.html', label: 'Products' },
        { href: 'custom-manufacturing.html', label: 'Custom Manufacturing' },
        { href: 'industries.html', label: 'Industries' },
        { href: 'faq.html', label: 'FAQ' },
        { href: 'contact.html', label: s.cta_primary_label || 'Request a Quote', isCta: true },
    ];

    header.innerHTML = `
        <div class="container">
            <a href="index.html" class="site-logo" aria-label="${s.site_name || 'GOS Chemicals'} Home">
                <img src="img/logo-emblem.png" alt="${s.site_name || 'GOS Chemicals'} - Specialty Chemical Manufacturer India" class="site-logo-img">
                <span class="site-logo-text">${s.site_name || 'GOS Chemicals'}</span>
            </a>
            <button class="nav-toggle" id="nav-toggle" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="site-nav">
                <span></span><span></span><span></span>
            </button>
            <nav class="site-nav" id="site-nav" aria-label="Primary Navigation">
                ${navLinks.map(l => `<a href="${l.href}" class="${l.isCta ? 'nav-cta' : ''} ${currentPage === l.href ? 'active' : ''}">${l.label}</a>`).join('')}
            </nav>
        </div>
    `;

    // Mobile nav toggle and accessibility
    const toggle = document.getElementById('nav-toggle');
    const nav = document.getElementById('site-nav');
    if (toggle && nav) {
        const closeNav = () => {
            nav.classList.remove('open');
            toggle.classList.remove('open');
            toggle.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        };

        const toggleNav = () => {
            const isOpen = nav.classList.toggle('open');
            toggle.classList.toggle('open', isOpen);
            toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            // Prevent body scroll when mobile menu is full overlay
            if (window.innerWidth <= 768) {
                document.body.style.overflow = isOpen ? 'hidden' : '';
            }
        };

        toggle.addEventListener('click', toggleNav);

        // Close on link click
        nav.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', closeNav);
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && nav.classList.contains('open')) {
                closeNav();
                toggle.focus();
            }
        });

        // Close on window resize to desktop
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && nav.classList.contains('open')) {
                closeNav();
            }
        });
    }
}

function renderFooter(s) {
    const footer = document.getElementById('site-footer');
    if (!footer) return;

    footer.innerHTML = `
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <a href="index.html" class="site-logo site-logo--footer">
                        <img src="img/logo-emblem.png" alt="${s.site_name || 'GOS Chemicals'} - Specialty Chemical Manufacturer India" class="site-logo-img">
                        <span class="site-logo-text">${s.site_name || 'GOS Chemicals'}</span>
                    </a>
                    <p>${s.site_tagline || 'Specialty Chemicals Manufactured & Exported from India'}</p>
                </div>
                <div class="footer-links">
                    <h4>Quick Links</h4>
                    <a href="products.html">Products</a>
                    <a href="custom-manufacturing.html">Custom Manufacturing</a>
                    <a href="industries.html">Industries</a>
                    <a href="faq.html">FAQ</a>
                    <a href="contact.html">Request a Quote</a>
                </div>
                <div class="footer-links footer-contact">
                    <h4>Contact &amp; Export</h4>
                    ${s.contact_email ? `<p>Email: <a href="mailto:${s.contact_email}" style="color:inherit; text-decoration:underline;">${s.contact_email}</a></p>` : ''}
                    ${s.contact_address ? `<p>Location: ${s.contact_address}</p>` : ''}
                    <p>Origin Ports: Mundra, Kandla, Nhava Sheva (JNPT)</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; ${new Date().getFullYear()} ${s.site_name || 'GOS Chemicals'}. All rights reserved.</p>
            </div>
        </div>
    `;
}
