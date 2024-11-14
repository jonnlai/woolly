from django.shortcuts import render
from .models import Product

def all_products(request):
    """
    Returns all products in :model:`products.Product`

    **Context**

    ``products``
        All instances of :model:`products.Product`

    **Template**

    :template:`products/all_products.html`

    """
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)
