const checkoutForm = document.getElementById('checkout-form');
const subtotal = parseFloat(checkoutForm.dataset.subtotal) || 0;

const shippingCosts = {
    'Lagos Island (Lekki, VI, Ajah)': 1500,
    'Lagos Mainland': 2500,
    'Others': null,
};

const selectEl = document.querySelector('select[name="delivery_area"]');
const shippingEl = document.getElementById('shipping-cost');
const totalEl = document.getElementById('order-total');
const infoEl = document.getElementById('shipping-info');

// hide info initially
infoEl.style.display = 'none';

selectEl.addEventListener('change', function () {
    const area = this.value;
    const shipping = shippingCosts[area];

    if (!area) {
        shippingEl.textContent = 'Select area';
        totalEl.textContent = '₦' + subtotal.toLocaleString();
        infoEl.style.display = 'none';
    } else if (shipping === null) {
        shippingEl.textContent = 'TBD on WhatsApp';
        totalEl.textContent = '₦' + subtotal.toLocaleString() + ' + shipping';
        infoEl.style.display = 'block';
    } else {
        const total = subtotal + shipping;
        shippingEl.textContent = '₦' + shipping.toLocaleString();
        totalEl.textContent = '₦' + total.toLocaleString();
        infoEl.style.display = 'none';
    }
});
