from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        messages.error(request,
        'Sorry, only store owners can access this page')
        return redirect('home')

    products = Product.objects.all().order_by('name')
    orders = Order.objects.all().order_by('-date')
    coupon_codes = CouponCode.objects.all().order_by('-active')

    context = {
        'products': products,
        'orders': orders,
        'coupon_codes': coupon_codes,
        'on_dashboard_page': True,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)