/* ==========================================================================
   Contact Form — GOS Chemicals
   Handles form submission via POST /api/contact, shows success/error.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contact-form');
    if (!form) return;

    // Pre-fill product field from URL param (from product detail CTA)
    const params = new URLSearchParams(window.location.search);
    const product = params.get('product');
    if (product) {
        const productInput = form.querySelector('[name="product"]');
        if (productInput) productInput.value = product;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const status = document.getElementById('form-status');
        const submitBtn = form.querySelector('button[type="submit"]');

        const nameInput = form.querySelector('[name="name"]');
        const emailInput = form.querySelector('[name="email"]');

        if (!nameInput.value.trim()) {
            status.className = 'form-status error';
            status.textContent = 'Please enter your contact person name.';
            status.style.display = 'block';
            nameInput.focus();
            return;
        }

        if (!emailInput.value.trim() || !emailInput.value.includes('@')) {
            status.className = 'form-status error';
            status.textContent = 'Please provide a valid business email address.';
            status.style.display = 'block';
            emailInput.focus();
            return;
        }

        submitBtn.disabled = true;
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Submitting Request...';
        status.className = 'form-status';
        status.style.display = 'none';

        const data = {};
        new FormData(form).forEach((val, key) => { data[key] = val; });

        try {
            const result = await apiPost('/contact', data);
            if (result && result.success) {
                status.className = 'form-status success';
                status.textContent = 'Thank you for your quotation request. Our commercial team will evaluate your requirements and contact you within 24 business hours.';
                status.style.display = 'block';
                form.reset();
            } else {
                throw new Error(result?.error || 'Submission failed. Please check your details and try again.');
            }
        } catch (err) {
            status.className = 'form-status error';
            status.textContent = err.message || 'Unable to transmit your request at this moment. Please email info@goschemicals.com directly.';
            status.style.display = 'block';
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText || 'Submit Quotation Request';
        }
    });
});
