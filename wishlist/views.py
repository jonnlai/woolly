from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Wishlist
from .models import Product


@login_required
def wishlist(request, product_id):
    """
    View to allow user to add and remove
    a product from their wishlist

    **Context**

    ``product``
        An instance of :model:`products.Product`
    ``profile``
        Profile of the request user
        from :model:`profiles.UserProfile`

    **Template**

    """
    product = get_object_or_404(Product, id=product_id)
    profile = request.user.userprofile

    # Check whether the product is on the user's wishlist and
    # if so, remove it from the wishlist
    try:
        Wishlist.objects.get(
            user_profile=profile,
            wished_product=product).delete()
        messages.success(
            request,
            f'{product.name} has been removed from your wishlist')
        return redirect('profile')
    # If the Wishlist does not exist, create it
    except Wishlist.DoesNotExist:
        Wishlist.objects.create(
            user_profile=profile,
            wished_product=product)
        messages.success(
            request,
            f'{product.name} has been added to your wishlist!')
    return redirect('product_detail', product_id)
