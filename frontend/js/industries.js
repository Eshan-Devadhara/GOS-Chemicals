/* ==========================================================================
   Industries Page — GOS Chemicals
   Fetches and renders all published industries.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('industries-page-grid');
    if (!grid) return;

    grid.innerHTML = '<div class="loading-state"><div class="loading-spinner"></div><p>Loading industries...</p></div>';

    try {
        const industries = await apiGet('/industries');
        if (!industries.length) {
            grid.innerHTML = '<p class="empty-state">No industries listed yet.</p>';
            return;
        }
        grid.innerHTML = industries.map(i => `
            <div class="industry-card">
                <h3>${i.name}</h3>
                <p>${i.description || ''}</p>
            </div>
        `).join('');
    } catch (e) {
        grid.innerHTML = '<p class="error-state">Failed to load industries.</p>';
    }
});
