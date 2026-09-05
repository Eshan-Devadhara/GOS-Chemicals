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

        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
        status.className = 'form-status';
        status.style.display = 'none';

        const data = {};
        new FormData(form).forEach((val, key) => { data[key] = val; });

        try {
            const result = await apiPost('/contact', data);
            if (result.success) {
                status.className = 'form-status success';
                status.textContent = 'Thank you for your enquiry. We will get back to you shortly.';
                status.style.display = 'block';
                form.reset();
            } else {
                throw new Error(result.error || 'Submission failed');
            }
        } catch (err) {
            status.className = 'form-status error';
            status.textContent = err.message || 'Something went wrong. Please try again.';
            status.style.display = 'block';
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Enquiry';
        }
    });
});
