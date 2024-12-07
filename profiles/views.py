from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order
from wishlist.models import Wishlist
from reviews.models import Review


@login_required
def profile(request):
    """
    Renders profile information about the selected user.

    **Context**

    ``profile``
        An instance of :model:`profiles.Profile`
    ``wishlist``
        An instace of :model:`wishlist.Wishlist`
    ``form``
        An instance of :form:`profiles.UserProfileForm`
    ``orders``
        All orders of the request user
    ``on_profile_page``
        Confirm that user is on profile page

    **Template**

    :template:`profiles/profile.html`
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist = list(Wishlist.objects.filter(user_profile=profile))
    form = UserProfileForm(instance=profile)
    orders = profile.orders.all().order_by('-date')
    reviews = Review.objects.filter(review_author = request.user)


    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    



    template = 'profiles/profile.html'
    context = {'profile': profile,
               'form': form,
               'orders': orders,
               'wishlist': wishlist,
               'reviews': reviews,
               'on_profile_page': True}

    return render(request, template, context)


def order_history(request, order_number):
    """
    Displays details of registered user's selected
    previous order

    **Context**

    ``order``
        An instance of :model:`checkout.Order`

    **Template**

    :template:`checkout/checkout_success.html`

    """
    order = get_object_or_404(Order, order_number=order_number)
    
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    return render(
        request,
        'checkout/checkout_success.html',
        {'order': order,
        'from_profile': True,}
    )