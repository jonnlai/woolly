from django.test import TestCase
from .forms import ProductForm
from .models import Category


class TestProductForm(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Homeware",
        )

    def test_form_is_valid(self):
        product_form = ProductForm({
            'category': self.category,
            'name': 'Product',
            'sku': '',
            'description': 'A new test product',
            'price': 15.99,
            'on_sale': False,
            'sale_price': '',
            'image': '',
            'in_stock': True,
            'stock_amount': 25
        })
        self.assertTrue(
            product_form.is_valid(),
            msg="Form is invalid")
    
    def test_name_is_required(self):
        product_form = ProductForm({
            'category': self.category,
            'name': '',
            'sku': '',
            'description': 'A new test product',
            'price': 15.99,
            'on_sale': False,
            'sale_price': '',
            'image': '',
            'in_stock': True,
            'stock_amount': 25
        })
        self.assertFalse(
            product_form.is_valid(),
            msg="Name is missing but form is valid")
    
    def test_description_is_required(self):
        product_form = ProductForm({
            'category': self.category,
            'name': 'Product',
            'sku': '',
            'description': '',
            'price': 15.99,
            'on_sale': False,
            'sale_price': '',
            'image': '',
            'in_stock': True,
            'stock_amount': 25
        })
        self.assertFalse(
            product_form.is_valid(),
            msg="Description itle is missing but form is valid")

    def test_price_is_required(self):
        product_form = ProductForm({
            'category': self.category,
            'name': 'Product',
            'sku': '',
            'description': 'This a test product',
            'price': '',
            'on_sale': False,
            'sale_price': '',
            'image': '',
            'in_stock': True,
            'stock_amount': 25
        })
        self.assertFalse(
            product_form.is_valid(),
            msg="Price is missing but form is valid")
