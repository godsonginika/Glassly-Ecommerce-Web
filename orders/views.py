from django.shortcuts import render, redirect
from django.conf import settings
from .models import Order, OrderItem
from cart.cart import Cart
import urllib.parse


def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('cart_detail')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        delivery_area = request.POST.get('delivery_area')
        notes = request.POST.get('notes', '')

        shipping_costs = {
            'Lagos Island (Lekki, VI, Ajah)': 1500,
            'Lagos Mainland': 2500,
            'Others': 0,
        }
        shipping = shipping_costs.get(delivery_area, 0)
        subtotal = float(cart.get_total())
        grand_total = subtotal + shipping

        order = Order.objects.create(
            full_name=full_name,
            phone=phone,
            address=address,
            delivery_area=delivery_area,
            notes=notes,
            total=grand_total,
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
            )

        # Build WhatsApp message
        lines = []
        lines.append("Hello! I'd like to place an order 🛍️")
        lines.append("")
        lines.append("*ORDER DETAILS*")
        for item in cart:
            price = float(item['price']) * int(item['quantity'])
            lines.append(f"  • {item['name']} x{item['quantity']} — ₦{price:,.0f}")

        lines.append("")
        lines.append(f"*Subtotal:* ₦{subtotal:,.0f}")

        if shipping == 0:
            lines.append(f"Shipping ({delivery_area}): TBD on WhatsApp")
        else:
            lines.append(f"Shipping ({delivery_area}): ₦{shipping:,.0f}")

        if shipping > 0:
            lines.append(f" *Total: ₦{grand_total:,.0f}*")
        else:
            lines.append(f" *Total: ₦{subtotal:,.0f} + shipping*")

        lines.append("")
        lines.append("*DELIVERY INFO*")
        lines.append(f"*Name:* {full_name}")
        lines.append(f"*Phone:* {phone}")
        lines.append(f"*Address:* {address}")
        lines.append(f"*Area:* {delivery_area}")

        if notes:
            lines.append("")
            lines.append(f"*Notes:* {notes}")

        lines.append("")
        lines.append("Please confirm my order. Thank you!")

        message = "\n".join(lines)

        cart.clear()

        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={encoded_message}"

        return redirect(whatsapp_url)

    return render(request, 'checkout.html', {'cart': cart})