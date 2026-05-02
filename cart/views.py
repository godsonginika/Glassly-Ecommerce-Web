from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core import settings
from .cart import Cart
from store.models import Product

# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    # 🔹 Get discount from session
    discount = request.session.get('discount', 0)

    subtotal = cart.get_total()
    discount_percent = int(discount * 100)
    discount_amount = subtotal * discount
    discounted_total = subtotal - discount_amount

    # 🔹 WhatsApp message
    whatsapp_number = settings.WHATSAPP_NUMBER
    message = "Hello! I'd like to order the following:\n\n"

    for item in cart:
        message += f"- {item['name']} x{item['quantity']} @ ${item['price']}\n"

    message += f"\nSubtotal: ${subtotal}"

    if discount:
        message += f"\nDiscount: {int(discount * 100)}%"

    message += f"\nTotal: ${discounted_total}"

    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message}"

    return render(request, 'cart.html', {
        'cart': cart,
        'whatsapp_url': whatsapp_url,
        'subtotal': subtotal,
        'discount': discount,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'discounted_total': discounted_total,
    })

def add_to_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)

    quantity = int(request.POST.get('quantity', 1))

    # Do not allow adding more than available stock
    current_quantity = cart.cart.get(str(pk), {}).get('quantity', 0)
    available_quantity = product.stock - current_quantity

    if available_quantity <= 0:
        messages.error(request, f"{product.name} is already at maximum available stock.")
        return redirect('cart_detail')

    if quantity > available_quantity:
        quantity = available_quantity
        messages.warning(request, f"Only {product.stock} {product.name} available in stock.")

    cart.add(product=product, quantity=quantity)

    return redirect('cart_detail')

def remove_from_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect('cart_detail')

def update_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(product, quantity)
    return redirect('cart_detail')

def apply_promo(request):
    if request.method == "POST":

        VALID_PROMO_CODES = {
            "GLASS10": 0.10,
            "WELCOME5": 0.05,
        }

        code = request.POST.get("promo_code", "").upper()

        if code in VALID_PROMO_CODES:
            request.session['promo_code'] = code
            request.session['discount'] = VALID_PROMO_CODES[code]

            messages.success(request, f"Promo applied! {VALID_PROMO_CODES[code]*100}% off", extra_tags="promo")

        else:
            request.session['promo_code'] = None
            request.session['discount'] = 0

            messages.error(request, "Invalid promo code", extra_tags="promo")

    return redirect('cart_detail')