/* ==========================================================================
   Home Page — GOS Chemicals
   Populates hero, core products, industries, why-source, FAQ preview.
   Maintains premium industrial B2B styling and progressive enhancement.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const [settings, chemicals, industries, faqs] = await Promise.all([
            apiGet('/settings').catch(() => null),
            apiGet('/chemicals?category=Core').catch(() => null),
            apiGet('/industries').catch(() => null),
            apiGet('/faqs').catch(() => null),
        ]);

        if (settings) renderHero(settings);
        if (chemicals && chemicals.length > 0) renderCoreProducts(chemicals);
        if (industries && industries.length > 0) renderIndustries(industries);
        if (settings) renderWhySource(settings);
        if (faqs && faqs.length > 0) renderFaqPreview(faqs.slice(0, 4));
    } catch (e) {
        console.warn('Home page dynamic load error, retaining static content:', e);
    }
});

function renderHero(s) {
    const el = document.getElementById('hero-content');
    if (!el || !s || !s.hero_headline) return;
    el.innerHTML = `
        <p class="hero-sub">${s.hero_subheadline || 'Castor Oil &amp; Derivatives · Chlorinated Paraffin Wax · Bleaching Clay'}</p>
        <h1>${s.hero_headline}</h1>
        <p class="hero-intro">${s.hero_intro || ''}</p>
        <div class="hero-actions">
            <a href="contact.html" class="btn btn-primary-light">${s.cta_primary_label || 'Request a Quote'}</a>
            <a href="products.html" class="btn btn-outline-light">${s.cta_secondary_label || 'Explore Products'}</a>
        </div>
    `;
}

function renderCoreProducts(chemicals) {
    const el = document.getElementById('core-products');
    if (!el || !chemicals || !chemicals.length) return;
    el.innerHTML = chemicals.map(c => `
        <a href="product-detail.html?slug=${c.slug}" class="card-link">
            <div class="card card--accent animate-in">
                ${c.image_url ? `<img src="${c.image_url}" alt="${c.name} - GOS Chemicals" class="card-image" loading="lazy">` : ''}
                <span class="section-eyebrow">${c.category || 'Core Manufacturing'}</span>
                <h3>${c.name}</h3>
                <p>${c.summary || ''}</p>
                <span class="card-arrow">View Details &rarr;</span>
            </div>
        </a>
    `).join('');
}

function renderIndustries(industries) {
    const el = document.getElementById('industries-grid');
    if (!el || !industries || !industries.length) return;
    const icons = ['🎨', '💧', '⛏️', '📄', '🌻', '⚙️', '🏗️', '🧪'];
    el.innerHTML = industries.map((i, idx) => `
        <div class="industry-card animate-in">
            <h3><span class="industry-icon">${icons[idx % icons.length]}</span> ${i.name}</h3>
            <p>${i.description || ''}</p>
        </div>
    `).join('');
}

function renderWhySource(s) {
    const el = document.getElementById('why-grid');
    if (!el || !s || !s.why_source_items) return;

    const items = s.why_source_items.split('|').filter(Boolean);
    if (!items.length) return;
    el.innerHTML = items.map(item => {
        const colonIdx = item.indexOf(':');
        const title = colonIdx > -1 ? item.substring(0, colonIdx).trim() : '';
        const desc = colonIdx > -1 ? item.substring(colonIdx + 1).trim() : item.trim();
        return `<div class="why-item card animate-in"><h3>${title}</h3><p>${desc}</p></div>`;
    }).join('');
}

function renderFaqPreview(faqs) {
    const el = document.getElementById('faq-preview');
    if (!el || !faqs || !faqs.length) return;
    el.innerHTML = faqs.map(f => `
        <div class="faq-item">
            <button class="faq-question" aria-expanded="false" onclick="this.setAttribute('aria-expanded', this.parentElement.classList.toggle('open'))">
                <span>${f.question}</span>
                <span class="faq-icon">+</span>
            </button>
            <div class="faq-answer"><p>${f.answer}</p></div>
        </div>
    `).join('');
}
