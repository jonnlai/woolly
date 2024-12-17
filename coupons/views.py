from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import CouponCode
from .forms import CouponForm


def apply_coupon(request):
    """
    Handle applying coupon codes
    """
    if request.method == 'POST':
        code = request.POST.get('coupon-code')
        try:
            # Check whether the code is a valid, active code
            code = CouponCode.objects.get(coupon_code=code, active=True)
            discount_amount = code.discount_amount
            coupon_code = code.coupon_code
            # Store the discount amount and coupon code in the session
            request.session['discount_amount'] = discount_amount
            request.session['coupon_code'] = coupon_code
            messages.success(
                request,
                'Valid code! The discount has been applied if your \
                    order total was at least £10 + discount amount.')
        except ObjectDoesNotExist:
            messages.error(request, 'You have entered an invalid code.')
    return redirect('checkout')


@login_required
def deactivate_coupon(request, coupon_code):
    """
    View to allow admin to deactive a coupon
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, only store owners can access this page'
        )
        return redirect('home')

    try:
        coupon = get_object_or_404(CouponCode, coupon_code=coupon_code)
        coupon.active = False
        coupon.save()
        messages.success(request, 'This coupon has been deactivated.')
    except ObjectDoesNotExist:
        messages.error(request, 'This code does not exist')
    return HttpResponseRedirect(reverse('dashboard'))


@login_required
def add_coupon(request):
    """
    View to allow admin to create new coupon codes
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, only store owners can access this page'
        )
        return redirect('home')

    form = CouponForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon successfully added.')
            return redirect('dashboard')
        else:
            messages.error(
                request,
                'Coupon could not be added. Please try again.')

    return render(
        request,
        'coupons/add_coupon.html',
        {'form': form}
    )
