from django.shortcuts import render
from products.views import Product

def index(request):
    """
    Returns the home page.

    **Context**

    ``products``
        All instances of :model:`products.Product`

    **Template**

    :template:`home/index.html`
    """
    products = Product.objects.all()

    return render(
        request,
        'home/index.html',
        {"products": products,
        })
