from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
from reviews.models import Review
from .views import all_products, product_detail


class TestProductViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testUserName",
            password="testPassword",
            email="test@email.com"
        )

        self.product = Product.objects.create(
            name='testProduct',
            description='This is a test product',
            price=25,
            in_stock=True,
            stock_amount=25,
        )

        self.review = Review.objects.create(
            review_title="Great product",
            review_content="Love this product",
            product_rating="5",
            review_author=self.user,
            product=self.product,
        )

    def test_render_all_products_page(self):
        response = self.client.get(reverse(
            'products'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"testProduct", response.content)
        self.assertIn(b"25", response.content)

    def test_render_product_detail_page(self):
        response = self.client.get(reverse(
            'product_detail',
            args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
