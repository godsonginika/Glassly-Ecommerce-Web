from django.conf import settings
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'image': product.image.url if product.image else None,
            }
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def save(self):
        self.session.modified = True

    def get_total(self):
        return sum(
            float(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def __iter__(self):
        for product_id, item in self.cart.items():
            item['product_id'] = product_id
            item['subtotal'] = float(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return self.get_total_items()