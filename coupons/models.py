from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Inspiration taken from https://www.youtube.com/watch?v=otoKdW-lYc8 and
# https://medium.com/@ayoubennaoui20/
# integrating-a-coupon-system-into-our-e-commerce-website-700a9e699f2a
class CouponCode(models.Model):
    """
    Stores a single coupon code
    """
    coupon_code = models.CharField(
        max_length=20,
        unique=True,
        null=False)
    discount_amount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.coupon_code)
