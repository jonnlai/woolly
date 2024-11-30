from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import CouponCode
from .forms import ApplyCouponForm


def apply_coupon(request):
    """
    Handle applying coupon codes

    **Context**
        ``code``
            
    """
    if request.method == 'POST':
        code = request.POST.get('coupon-code')
        try:
            code = CouponCode.objects.get(coupon_code=code, active=True)
            discount_amount = code.discount_amount
            # Store the discount amount
            request.session['discount_amount'] = discount_amount
            messages.success(request, 'Coupon code applied!')
        except ObjectDoesNotExist:
            messages.error(request, 'You have entered an invalid code.')
    return redirect('checkout')