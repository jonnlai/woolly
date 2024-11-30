from django import forms
from .models import CouponCode


class ApplyCouponForm(forms.Form):
    class Meta:
        model: CouponCode
        fields = ('coupon_code', 'discount_amount', 'active')