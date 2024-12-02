from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_coupon, name='apply_coupon'),
    path('deactivate/<coupon_code>', views.deactivate_coupon, name='deactivate'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
]