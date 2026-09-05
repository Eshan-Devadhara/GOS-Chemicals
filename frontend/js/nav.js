/* ==========================================================================
   Nav & Footer — GOS Chemicals
   Renders shared header/nav and footer from /api/settings on every page.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    let settings = {};
    try {
        settings = await apiGet('/settings');
    } catch (e) {
        console.error('Failed to load settings:', e);
    }

    renderHeader(settings);
    renderFooter(settings);
});

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
            <a href="index.html" class="site-logo">
                <img src="img/logo.svg" alt="${s.site_name || 'GOS Chemicals'} Logo" class="site-logo-img">
                <span class="site-logo-text">${s.site_name || 'GOS Chemicals'}</span>
            </a>
            <button class="nav-toggle" id="nav-toggle" aria-label="Toggle menu">
                <span></span><span></span><span></span>
            </button>
            <nav class="site-nav" id="site-nav">
                ${navLinks.map(l => `<a href="${l.href}" class="${l.isCta ? 'nav-cta' : ''} ${currentPage === l.href ? 'active' : ''}">${l.label}</a>`).join('')}
            </nav>
        </div>
    `;

    // Mobile nav toggle
    const toggle = document.getElementById('nav-toggle');
    const nav = document.getElementById('site-nav');
    if (toggle && nav) {
        toggle.addEventListener('click', () => nav.classList.toggle('open'));
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
                        <img src="img/logo.svg" alt="${s.site_name || 'GOS Chemicals'} Logo" class="site-logo-img">
                        <span class="site-logo-text">${s.site_name || 'GOS Chemicals'}</span>
                    </a>
                    <p>${s.site_tagline || ''}</p>
                </div>
                <div class="footer-links">
                    <h4>Quick Links</h4>
                    <a href="products.html">Products</a>
                    <a href="custom-manufacturing.html">Custom Manufacturing</a>
                    <a href="industries.html">Industries</a>
                    <a href="faq.html">FAQ</a>
                    <a href="contact.html">Contact</a>
                </div>
                <div class="footer-links footer-contact">
                    <h4>Contact</h4>
                    ${s.contact_email ? `<p>${s.contact_email}</p>` : ''}
                    ${s.contact_phone ? `<p>${s.contact_phone}</p>` : ''}
                    ${s.contact_address ? `<p>${s.contact_address}</p>` : ''}
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; ${new Date().getFullYear()} ${s.site_name || 'GOS Chemicals'}. All rights reserved.</p>
            </div>
        </div>
    `;
}
