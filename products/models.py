from django.db import models
from django.db.models import Avg
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
        Return the product price taking into consideration
        whether it is on sale
        """
        if self.on_sale and self.sale_price < self.price:
            return self.sale_price
        else:
            return self.price


    @property
    def avg_rating(self):
        """ 
        Get the avarage rating for the selected product

        Related name `product_reviews` from :model:`reviews.Review`
        """
        # Check whether the product has been reviewed 
        # using the related name 'product_reviews'
        
        product_reviews = self.product_reviews.all()

        if product_reviews:
            # How to calculate average taken from
            # https://stackoverflow.com/questions/28607727/
            # how-to-calculate-average-in-django?rq=3
            avg_rating = self.product_reviews.all().aggregate(Avg("product_rating"))
            avg_rating_num = float(avg_rating['product_rating__avg'])
            return avg_rating_num
        else:
            return False

