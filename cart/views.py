from django.shortcuts import render, redirect, get_object_or_404
from core import settings
from .cart import Cart
from store.models import Product

# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    
    # Build WhatsApp message
    whatsapp_number = settings.WHATSAPP_NUMBER
    message = "Hello! I'd like to order the following:\n\n"
    for item in cart:
        message += f"- {item['name']} x{item['quantity']} @ ${item['price']}\n"
    message += f"\nTotal: ${cart.get_total()}"
    
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message}"
    
    return render(request, 'cart.html', {
        'cart': cart,
        'whatsapp_url': whatsapp_url,
    })

def add_to_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.add(product)
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