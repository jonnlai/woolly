from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Review
from products.models import Product


@login_required
def reviews(request, product_id):
    """
    Returns all reviews from :model:`reviews.Review`
    for the selected product

    **Context**

    ``products``
        All instances of :model:`products.Product`

    **Template**

    :template:`products/all_products.html`

    """
    product = Product.objects.filter(id=product_id)
    reviews = Review.objects.filter(product=product)

    context = {
        'reviews': reviews,
    }

    return render(request, template, context)
