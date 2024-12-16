from django.db import models

from products.models import Product
from django.contrib.auth.models import User

STAR_RATING = (
    ("", "How many stars would you give this product?"),
    (1, "★ (Poor)"),
    (2, "★★ (Fair)"),
    (3, "★★★ (Average)"),
    (4, "★★★★ (Good)"),
    (5, "★★★★★ (Great)")
)


class Review(models.Model):
    """
    Stores a single product review
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )
    review_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_reviews'
    )
    review_title = models.CharField(max_length=150)
    review_content = models.TextField()
    product_rating = models.IntegerField(choices=STAR_RATING, default=None)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.product} review by {self.review_author}'
