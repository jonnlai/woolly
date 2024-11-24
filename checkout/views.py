from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    """
    Returns the checkout

    **Context**

    ``order_form``
        An instance of of :form:`checkout.OrderForm`

    **Template**

    :template:`checkout/checkout.html`
    """
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()

    return render(
        request,
        'checkout/checkout.html',
        {'order_form': order_form,
         'stripe_public_key': 'pk_test_51QOdM02NHaXwRfMSv0eYmmvXeObJWbfevDYVy9AOdgF03U3O0Yk2NSfUfdvpLOpa1EyfrTrfQBqwV52n4EKqcWK900smYyEhNm',
         'client_secret': 'test client secret',}
        )
