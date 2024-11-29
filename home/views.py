from django.shortcuts import render
from products.views import Product

def index(request):
    """
    Returns the home page.

    **Context**

    ``products``
        All instances of :model:`products.Product`
    ``featured_products``
        Three instances of products that are on sale

    **Template**

    :template:`home/index.html`
    """
    products = Product.objects.all()
    featured_products = Product.objects.filter(on_sale=True)[:3]

    return render(
        request,
        'home/index.html',
        {"products": products,
         "featured_products": featured_products,
        })
