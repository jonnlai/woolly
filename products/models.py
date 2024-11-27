from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """
    Stores a single category
    """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    Stores a single product related to :model:`products.Category`
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    sku = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # Inspiration for creating sale prices taken from Codemy:
    # https://www.youtube.com/watch?v=w7pnR408jVU
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(
        decimal_places=2, max_digits=6, null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    stock_amount = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(500)])

    def __str__(self):
        return self.name

    # How to use property decorator taken from:
    #https://stackoverflow.com/questions/58558989/what-does-djangos-property-do
    @property
    def product_price(self):
        """
        Return the product price taking into considaration
        whether it is on sale
        """
        if self.on_sale and self.sale_price < self.price:
            return self.sale_price
        else:
            return self.price
