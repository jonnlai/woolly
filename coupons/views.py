from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import CouponCode
from .forms import ApplyCouponForm


def apply_coupon(request):
    """
    Handle applying coupon codes     
    """
    if request.method == 'POST':
        code = request.POST.get('coupon-code')
        try:
            #Check whether the code is a valid, active code
            code = CouponCode.objects.get(coupon_code=code, active=True)
            discount_amount = code.discount_amount
            coupon_code = code.coupon_code
            # Store the discount amount and coupon code in the session
            request.session['discount_amount'] = discount_amount
            request.session['coupon_code'] = coupon_code
            messages.success(request, 'Coupon code applied!')
        except ObjectDoesNotExist:
            messages.error(request, 'You have entered an invalid code.')
    return redirect('checkout')