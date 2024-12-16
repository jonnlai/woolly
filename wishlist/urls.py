from django.urls import path
from . import views

urlpatterns = [
    path('wishlist/<product_id>', views.wishlist, name='wishlist')
]
