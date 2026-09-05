/* ==========================================================================
   Products Page — GOS Chemicals
   Fetches and renders all published chemicals as a card grid.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('products-grid');
    if (!grid) return;

    grid.innerHTML = '<div class="loading-state"><div class="loading-spinner"></div><p>Loading products...</p></div>';

    try {
        const chemicals = await apiGet('/chemicals');
        if (!chemicals.length) {
            grid.innerHTML = '<p class="empty-state">No products available yet.</p>';
            return;
        }
        grid.innerHTML = chemicals.map(c => `
            <a href="product-detail.html?slug=${c.slug}" class="card-link">
                <div class="card">
                    ${c.image_url ? `<img src="${c.image_url}" alt="${c.name}" style="border-radius:var(--radius-base); margin-bottom:1rem; height:180px; object-fit:cover; width:100%;">` : ''}
                    <span class="section-eyebrow">${c.category || ''}</span>
                    <h3>${c.name}</h3>
                    <p>${c.summary || ''}</p>
                </div>
            </a>
        `).join('');
    } catch (e) {
        grid.innerHTML = '<p class="error-state">Failed to load products. Please try again later.</p>';
    }
});
