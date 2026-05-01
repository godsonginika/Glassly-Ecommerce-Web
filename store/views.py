from django.shortcuts import get_object_or_404, render
from .models import Category, Product

# Create your views here.
def home(request):
    featured_products = Product.objects.all().order_by('-date_added')[:8]
    return render(request, 'home.html', {
        'featured_products': featured_products,
    })

def shop(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('q', '')

    products = Product.objects.all()

    if selected_category:
        products = products.filter(category__id=selected_category)
    
    if search_query:
        products = products.filter(name__icontains=search_query)
        
    
    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    related = Product.objects.filter(category=product.category).exclude(id=pk)[:4]
    return render(request, 'product_detail.html', {
        'product': product,
        'related': related,
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')