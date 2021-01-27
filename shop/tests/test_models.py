from django.test import TestCase, tag
from django.utils.text import slugify

from shop.models import Category


@tag('shop-models')
class ModelsTest(TestCase):
    def test_category_creation(self):
        category = Category(name='Shoes', slug='shoes')

        self.assertIsInstance(category, Category)
        self.assertEqual(category.slug, slugify(category.slug))
        self.assertEqual(category.__str__(), category.name)
