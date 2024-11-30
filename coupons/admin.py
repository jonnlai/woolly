from django.contrib import admin
from .models import CouponCode


class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'coupon_code',
        'discount_amount',
        'active',
    )

admin.site.register(CouponCode, CouponAdmin)
