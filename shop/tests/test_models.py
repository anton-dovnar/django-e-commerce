from django.test import TestCase, tag

from shop.models import Category, Product, Size
from shop.tests.mixins import SetUpMixin


@tag('shop-models')
class ModelsTest(SetUpMixin, TestCase):
    def test_category_creation(self):
        self.assertIsInstance(self.category, Category)
        self.assertEqual(self.category.__str__(), self.category.name)

    def test_product_creation(self):
        self.assertIsInstance(self.product, Product)
        self.assertEqual(self.product.__str__(), self.product.name)

    def test_size_creation(self):
        self.assertIsInstance(self.shoe_size, Size)
        self.assertEqual(self.shoe_size.__str__(), f'{self.shoe_size.product.name} - {self.shoe_size.size}')
