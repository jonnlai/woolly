from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from products.models import Product
from checkout.models import Order
from coupons.models import CouponCode


@login_required
def admin_dashboard(request):
    """
    Admin dashboard to view products and orders.

    **Context**

    ``orders``
        All instances of :model:`checkout.Order`
    ``products``
        All instances of :model:`products.Product`

    **Template**

    :template:`dashboard/admin_dashboard.html`
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, only store owners can access this page'
        )
        return redirect('home')

    products = Product.objects.all().order_by('name')
    orders = Order.objects.all().order_by('-date')
    coupon_codes = CouponCode.objects.all().order_by('-active')

    # Create a dictionary of product names and amounts each product has sold
    # How to use dictionary comprehension to achieve that taken from:
    # https://stackoverflow.com/questions/42198558/
    # django-query-to-list-the-count-of-field-values-distinctly
    sold_amount = {
        i[
            "lineitems__product__name"]: i[
                "count"] for i in Order.objects.values(
                'lineitems__product__name').annotate(count=Count(
                    'lineitems__product__name')).order_by("-count")
    }

    context = {
        'products': products,
        'orders': orders,
        'coupon_codes': coupon_codes,
        'on_dashboard_page': True,
        'sold_amount': sold_amount,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)
