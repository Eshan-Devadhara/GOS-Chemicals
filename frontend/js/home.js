/* ==========================================================================
   Home Page — GOS Chemicals
   Populates hero, core products, industries, why-source, FAQ preview.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const [settings, chemicals, industries, faqs] = await Promise.all([
            apiGet('/settings'),
            apiGet('/chemicals?category=Core'),
            apiGet('/industries'),
            apiGet('/faqs'),
        ]);

        renderHero(settings);
        renderCoreProducts(chemicals);
        renderIndustries(industries);
        renderWhySource(settings);
        renderFaqPreview(faqs.slice(0, 4));
    } catch (e) {
        console.error('Home page load error:', e);
    }
});

function renderHero(s) {
    const el = document.getElementById('hero-content');
    if (!el) return;
    el.innerHTML = `
        <h1>${s.hero_headline || ''}</h1>
        <p class="hero-sub">${s.hero_subheadline || ''}</p>
        <p class="hero-intro">${s.hero_intro || ''}</p>
        <div class="hero-actions">
            <a href="contact.html" class="btn btn-primary">${s.cta_primary_label || 'Request a Quote'}</a>
            <a href="products.html" class="btn btn-outline">${s.cta_secondary_label || 'Explore Products'}</a>
        </div>
    `;
}

function renderCoreProducts(chemicals) {
    const el = document.getElementById('core-products');
    if (!el) return;
    if (!chemicals.length) {
        el.innerHTML = '<p class="empty-state">No products available yet.</p>';
        return;
    }
    el.innerHTML = chemicals.map(c => `
        <a href="product-detail.html?slug=${c.slug}" class="card-link">
            <div class="card">
                <h3>${c.name}</h3>
                <p>${c.summary || ''}</p>
            </div>
        </a>
    `).join('');
}

function renderIndustries(industries) {
    const el = document.getElementById('industries-grid');
    if (!el) return;
    if (!industries.length) return;
    el.innerHTML = industries.map(i => `
        <div class="industry-card">
            <h3>${i.name}</h3>
            <p>${i.description || ''}</p>
        </div>
    `).join('');
}

function renderWhySource(s) {
    const el = document.getElementById('why-grid');
    if (!el || !s.why_source_items) return;

    const items = s.why_source_items.split('|').filter(Boolean);
    el.innerHTML = items.map(item => {
        const colonIdx = item.indexOf(':');
        const title = colonIdx > -1 ? item.substring(0, colonIdx).trim() : '';
        const desc = colonIdx > -1 ? item.substring(colonIdx + 1).trim() : item.trim();
        return `<div class="why-item card"><h3>${title}</h3><p>${desc}</p></div>`;
    }).join('');
}

function renderFaqPreview(faqs) {
    const el = document.getElementById('faq-preview');
    if (!el) return;
    if (!faqs.length) return;
    el.innerHTML = faqs.map(f => `
        <div class="faq-item">
            <button class="faq-question" onclick="this.parentElement.classList.toggle('open')">
                <span>${f.question}</span>
                <span class="faq-icon">+</span>
            </button>
            <div class="faq-answer"><p>${f.answer}</p></div>
        </div>
    `).join('');
}
