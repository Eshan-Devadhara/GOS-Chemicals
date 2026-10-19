/* ==========================================================================
   FAQ Page — GOS Chemicals
   Fetches all FAQs and renders accessible accordion.
   Maintains static FAQ fallback for search crawlers and resilience.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    const list = document.getElementById('faq-list');
    if (!list) return;

    try {
        const faqs = await apiGet('/faqs');
        if (faqs && faqs.length > 0) {
            list.innerHTML = faqs.map(f => `
                <div class="faq-item">
                    <button class="faq-question" aria-expanded="false" onclick="this.setAttribute('aria-expanded', this.parentElement.classList.toggle('open'))">
                        <span>${f.question}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer"><p>${f.answer}</p></div>
                </div>
            `).join('');
        }
    } catch (e) {
        console.warn('Dynamic FAQs load error, retaining static fallback:', e);
    }
});
