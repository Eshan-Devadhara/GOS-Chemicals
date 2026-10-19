/* ==========================================================================
   Products Page — GOS Chemicals
   Fetches and renders all published chemicals as an enhanced card grid.
   Maintains SEO fallback content and cohesive design tokens.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    // If a product query parameter exists, update canonical URL to self-reference
    const params = new URLSearchParams(window.location.search);
    const productParam = params.get('product') || params.get('slug');
    if (productParam) {
        const canonical = document.querySelector('link[rel="canonical"]');
        if (canonical) {
            canonical.setAttribute('href', `https://goschemicals.com/products.html?product=${encodeURIComponent(productParam)}`);
        }
    }

    const grid = document.getElementById('products-grid');
    if (!grid) return;

    try {
        const chemicals = await apiGet('/chemicals');
        if (chemicals && chemicals.length > 0) {
            grid.innerHTML = chemicals.map(c => `
                <a href="product-detail.html?slug=${c.slug}" class="card-link">
                    <div class="card card--accent animate-in">
                        ${c.image_url ? `<img src="${c.image_url}" alt="${c.name} - Specialty Chemical Supplier India" loading="lazy" class="card-image">` : ''}
                        <span class="section-eyebrow">${c.category || 'Specialty Chemical'}</span>
                        <h3>${c.name}</h3>
                        <p>${c.summary || ''}</p>
                        <span class="card-arrow">View Product Details &rarr;</span>
                    </div>
                </a>
            `).join('');
        }
    } catch (e) {
        console.warn('Dynamic products load error, keeping static portfolio fallback:', e);
    }
});
