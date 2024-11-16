from django.shortcuts import render, get_object_or_404
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

    return render(
        request,
        'products/products.html',
        {'products': products,}
        )


def product_detail(request, product_id):
    """ 
    Display an individual :model:`products.Product`

    **Context**

    **Template**

    :template:`products/product_detail.html`
    """
    product = get_object_or_404(Product, pk=product_id)

    return render(
        request,
        'products/product_detail.html',
        {"product": product,}
    )