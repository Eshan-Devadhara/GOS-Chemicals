/* ==========================================================================
   Industries Page — GOS Chemicals
   Fetches and renders all published industries.
   Maintains high-fidelity static fallback and cohesive icons.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('industries-page-grid');
    if (!grid) return;

    try {
        const industries = await apiGet('/industries');
        if (industries && industries.length > 0) {
            const icons = ['🎨', '💧', '⛏️', '📄', '🌻', '⚙️', '🏗️', '🧪'];
            grid.innerHTML = industries.map((i, idx) => `
                <div class="industry-card animate-in">
                    <h3><span class="industry-icon">${icons[idx % icons.length]}</span> ${i.name}</h3>
                    <p>${i.description || ''}</p>
                </div>
            `).join('');
        }
    } catch (e) {
        console.warn('Dynamic industries load error, retaining static fallback:', e);
    }
});
