
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("plus")) {
        const control = e.target.closest(".quantity-control");
        const input = control.querySelector(".qty-input");
        const stock = parseInt(e.target.dataset.stock);

        let current = parseInt(input.value);

        if (current < stock) {
            input.value = current + 1;
        }
    }

    if (e.target.classList.contains("minus")) {
        const control = e.target.closest(".quantity-control");
        const input = control.querySelector(".qty-input");

        let current = parseInt(input.value);

        if (current > 1) {
            input.value = current - 1;
        }
    }
});