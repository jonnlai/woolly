from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from products.models import Product

@login_required
def admin_dashboard(request):
    """
    Admin dashboard to view products and orders.
    """
    if not request.user.is_superuser:
        messages.error(request,
        'Sorry, only store owners can access this page')
        return redirect('home')

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)