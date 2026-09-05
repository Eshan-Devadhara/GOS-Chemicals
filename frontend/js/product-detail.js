/* ==========================================================================
   Product Detail Page — GOS Chemicals
   Reads ?slug= from URL, fetches single chemical, renders full detail.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    const content = document.getElementById('product-detail-content');
    if (!content) return;

    const params = new URLSearchParams(window.location.search);
    const slug = params.get('slug');

    if (!slug) {
        showNotFound(content);
        return;
    }

    content.innerHTML = '<div class="loading-state"><div class="loading-spinner"></div><p>Loading...</p></div>';

    try {
        const c = await apiGet(`/chemicals/${slug}`);
        document.title = `${c.seo_title || c.name} | GOS Chemicals`;

        const apps = c.applications ? c.applications.split(',').map(a => a.trim()).filter(Boolean) : [];
        const descriptionHtml = c.description ? c.description.replace(/\n/g, '<br>') : '';

        content.innerHTML = `
            <div class="container">
                <div style="margin-bottom: 1rem;">
                    <a href="products.html" style="font-size:0.85rem; color:var(--color-text-muted);">← Back to Products</a>
                </div>
                <div style="display: grid; grid-template-columns: ${c.image_url ? '1fr 1fr' : '1fr'}; gap: 3rem; align-items: start;">
                    ${c.image_url ? `<img src="${c.image_url}" alt="${c.name}" class="product-image">` : ''}
                    <div>
                        <span class="section-eyebrow">${c.category || ''}</span>
                        <h1>${c.name}</h1>
                        <p style="color:var(--color-text-muted); margin-top:0.75rem; line-height:1.7;">${c.summary || ''}</p>
                        <div style="margin-top:2rem;">
                            <a href="contact.html?product=${encodeURIComponent(c.name)}" class="btn btn-primary">${c.cta_label || 'Request a Quote'}</a>
                        </div>
                    </div>
                </div>

                <div class="product-meta" style="margin-top: 3rem;">
                    <div class="product-meta-item">
                        <h3>Description</h3>
                        <p>${descriptionHtml}</p>
                    </div>
                    <div class="product-meta-item">
                        <h3>Specification</h3>
                        <p>${c.specification || 'Contact us for specifications.'}</p>
                    </div>
                    ${apps.length ? `
                    <div class="product-meta-item">
                        <h3>Applications</h3>
                        <ul>${apps.map(a => `<li>${a}</li>`).join('')}</ul>
                    </div>` : ''}
                    <div class="product-meta-item">
                        <h3>Packaging</h3>
                        <p>${c.packaging || 'Contact us for packaging options.'}</p>
                    </div>
                </div>
            </div>
        `;
    } catch (e) {
        showNotFound(content);
    }
});

function showNotFound(el) {
    el.innerHTML = `
        <div class="not-found">
            <h2>Product Not Found</h2>
            <p>The product you're looking for doesn't exist or is no longer available.</p>
            <a href="products.html" class="btn btn-primary">Browse All Products</a>
        </div>
    `;
}
