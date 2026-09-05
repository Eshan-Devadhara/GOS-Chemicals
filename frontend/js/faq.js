/* ==========================================================================
   FAQ Page — GOS Chemicals
   Fetches all FAQs, renders accordion.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    const list = document.getElementById('faq-list');
    if (!list) return;

    list.innerHTML = '<div class="loading-state"><div class="loading-spinner"></div><p>Loading FAQs...</p></div>';

    try {
        const faqs = await apiGet('/faqs');
        if (!faqs.length) {
            list.innerHTML = '<p class="empty-state">No FAQs available yet.</p>';
            return;
        }
        list.innerHTML = faqs.map(f => `
            <div class="faq-item">
                <button class="faq-question" onclick="this.parentElement.classList.toggle('open')">
                    <span>${f.question}</span>
                    <span class="faq-icon">+</span>
                </button>
                <div class="faq-answer"><p>${f.answer}</p></div>
            </div>
        `).join('');
    } catch (e) {
        list.innerHTML = '<p class="error-state">Failed to load FAQs.</p>';
    }
});
