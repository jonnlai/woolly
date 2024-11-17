from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
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

    query = None
    # Search function taken from CodeInstitute's Boutique Ado walkthrough project
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    return render(
        request,
        'products/products.html',
        {'products': products,
         'search_term': query}
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