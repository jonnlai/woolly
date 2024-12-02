from django.db import models

from profiles.models import UserProfile
from products.models import Product


class wishlist(models.Model):
    """ 
    Stores a single user's wishlist related to :model:`profiles.UserProfile`
    and :model:`products.Product`
    """
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='wishlist'
    )
    wished_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    date_added_on = models.DateTimeField(
        auto_now_add=True
    )

