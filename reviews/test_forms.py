from django.test import TestCase
from .forms import ReviewForm


class TestReviewForm(TestCase):
    """
    Check review is valid when submitted
    """

    def test_form_is_valid(self):
        review_form = ReviewForm({
            'review_title': 'A really good product',
            'review_content': 'A lovely product',
            'product_rating': '5',
        })
        self.assertTrue(
            review_form.is_valid(),
            msg="Form is invalid")

    def test_title_is_required(self):
        review_form = ReviewForm({
            'review_title': '',
            'review_content': 'A lovely product',
            'product_rating': '5',
        })
        self.assertFalse(
            review_form.is_valid(),
            msg="Title is missing but form is valid")

    def test_content_is_required(self):
        review_form = ReviewForm({
            'review_title': 'A really good product',
            'review_content': '',
            'product_rating': '5',
        })
        self.assertFalse(
            review_form.is_valid(),
            msg="Content is missing but form is valid")

    def test_rating_is_required(self):
        review_form = ReviewForm({
            'review_title': 'A really good product',
            'review_content': 'A lovely product',
            'product_rating': '',
        })
        self.assertFalse(
            review_form.is_valid(),
            msg="Rating is missing but form is valid")
