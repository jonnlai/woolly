from django import forms
from .models import CouponCode


class CouponForm(forms.ModelForm):
    class Meta:
        model = CouponCode
        fields = '__all__'