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
        const pageTitle = `${c.seo_title || c.name} | GOS Chemicals`;
        const pageDescription = c.seo_description || c.summary || `${c.name} supplied by GOS Chemicals India. Inquire for specifications and quotation.`;
        const pageUrl = `https://goschemicals.com/product-detail.html?slug=${encodeURIComponent(c.slug)}`;
        const pageImage = c.image_url || 'https://goschemicals.com/img/logo.png';

        document.title = pageTitle;

        // Update meta tags dynamically
        const metaDesc = document.getElementById('meta-description');
        if (metaDesc) metaDesc.setAttribute('content', pageDescription);

        const canonical = document.getElementById('canonical-link');
        if (canonical) canonical.setAttribute('href', pageUrl);

        const ogTitle = document.getElementById('og-title');
        if (ogTitle) ogTitle.setAttribute('content', pageTitle);

        const ogDesc = document.getElementById('og-description');
        if (ogDesc) ogDesc.setAttribute('content', pageDescription);

        const ogUrl = document.getElementById('og-url');
        if (ogUrl) ogUrl.setAttribute('content', pageUrl);

        const ogImg = document.getElementById('og-image');
        if (ogImg) ogImg.setAttribute('content', pageImage);

        const twTitle = document.getElementById('twitter-title');
        if (twTitle) twTitle.setAttribute('content', pageTitle);

        const twDesc = document.getElementById('twitter-description');
        if (twDesc) twDesc.setAttribute('content', pageDescription);

        const twUrl = document.getElementById('twitter-url');
        if (twUrl) twUrl.setAttribute('content', pageUrl);

        const twImg = document.getElementById('twitter-image');
        if (twImg) twImg.setAttribute('content', pageImage);

        // Update or inject JSON-LD Product Schema
        const schemaEl = document.getElementById('product-schema');
        if (schemaEl) {
            const productSchema = {
                "@context": "https://schema.org/",
                "@type": "Product",
                "name": c.name,
                "description": pageDescription,
                "category": c.category || "Specialty Chemicals",
                "image": [pageImage],
                "url": pageUrl,
                "brand": {
                    "@type": "Brand",
                    "name": "GOS Chemicals"
                },
                "manufacturer": {
                    "@type": "Corporation",
                    "name": "Gujarat Oleo & Specialty Chemicals (GOS Chemicals)"
                },
                "offers": {
                    "@type": "Offer",
                    "url": `https://goschemicals.com/contact.html?product=${encodeURIComponent(c.name)}`,
                    "priceCurrency": "USD",
                    "price": "0.00",
                    "priceSpecification": {
                        "@type": "PriceSpecification",
                        "priceCurrency": "USD",
                        "description": "B2B commercial pricing upon inquiry"
                    },
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition"
                }
            };
            schemaEl.textContent = JSON.stringify(productSchema, null, 2);
        }

        const apps = c.applications ? c.applications.split(',').map(a => a.trim()).filter(Boolean) : [];
        const descriptionHtml = c.description ? c.description.replace(/\n/g, '<br>') : '';
        const imageAltText = `${c.name} - Specialty Chemical Supplier India`;

        content.innerHTML = `
            <div class="container">
                <div style="margin-bottom: 1rem;">
                    <a href="products.html" style="font-size:0.85rem; color:var(--color-text-muted);">← Back to Products Portfolio</a>
                </div>
                <div style="display: grid; grid-template-columns: ${c.image_url ? '1fr 1fr' : '1fr'}; gap: 3rem; align-items: start;">
                    ${c.image_url ? `<img src="${c.image_url}" alt="${imageAltText}" class="product-image">` : ''}
                    <div>
                        <span class="section-eyebrow">${c.category || 'Specialty Chemical'}</span>
                        <h1>${c.name}</h1>
                        <p style="color:var(--color-text-muted); margin-top:0.75rem; line-height:1.7;">${c.summary || ''}</p>
                        <div style="margin-top:2rem;">
                            <a href="contact.html?product=${encodeURIComponent(c.name)}" class="btn btn-primary">${c.cta_label || 'Request a Commercial Quote'}</a>
                        </div>
                    </div>
                </div>

                <div class="product-meta" style="margin-top: 3rem;">
                    <div class="product-meta-item">
                        <h2>Product Overview & Description</h2>
                        <p>${descriptionHtml}</p>
                    </div>
                    <div class="product-meta-item">
                        <h2>Technical Specifications</h2>
                        <p>${c.specification || 'Technical specifications and Certificate of Analysis (COA) available upon request.'}</p>
                    </div>
                    ${apps.length ? `
                    <div class="product-meta-item">
                        <h2>Key Industrial Applications</h2>
                        <ul>${apps.map(a => `<li>${a}</li>`).join('')}</ul>
                    </div>` : ''}
                    <div class="product-meta-item">
                        <h2>Packaging & Export Options</h2>
                        <p>${c.packaging || 'Export-grade packaging options available: drums, flexi-tanks, IBCs, and bulk shipments.'}</p>
                    </div>
                </div>

                <!-- Internal linking & conversion card -->
                <div style="margin-top: 3.5rem; padding: 2rem; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-base); text-align: center;">
                    <h3>Need a Custom Grade or Modified Formulation?</h3>
                    <p style="color: var(--color-text-muted); margin: 0.75rem auto 1.5rem; max-width: 600px;">
                        GOS Chemicals provides toll synthesis and custom chemical manufacturing tailored to your exact process requirements.
                    </p>
                    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                        <a href="custom-manufacturing.html" class="btn btn-outline">Custom Manufacturing</a>
                        <a href="contact.html?product=${encodeURIComponent(c.name)}" class="btn btn-primary">Request Specification Sheet</a>
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
