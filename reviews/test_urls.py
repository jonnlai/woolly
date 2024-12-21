from django.test import TestCase
from django.urls import reverse, resolve
from .views import edit_review


class TestUrls(TestCase):

    def test_edit_review_resolves(self):
        url = reverse('edit_review', args=['1', '2'])
        self.assertEqual(resolve(url).func, edit_review)
