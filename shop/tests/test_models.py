from django.test import TestCase, tag
from django.utils.text import slugify

from shop.models import Category, Product


@tag('shop-models')
class ModelsTest(TestCase):
    def test_category_creation(self):
        category = Category(name='Shoes', slug='shoes')

        self.assertIsInstance(category, Category)
        self.assertEqual(category.slug, slugify(category.name))
        self.assertEqual(category.__str__(), category.name)

    def test_product_creation(self):
        category = Category(name='Shoes', slug='shoes')
        product = Product(
            category=category, name='Nike SB Zoom Blazer Mid Edge',
            slug='nike-sb-zoom-blazer-mid-edge',
            description="""Want a custom look without the elbow grease?
            The Nike SB Zoom Blazer Mid Edge adds that something extra
            to your kicks with DIY details like frayed stitching, cut-out
            eyestays and patches of extra material in high-wear areas.""",
            price=89.95, available=True
        )

        self.assertIsInstance(product, Product)
        self.assertIsInstance(product.category, Category)
        self.assertEqual(product.category.name, category.name)
        self.assertEqual(product.slug, slugify(product.name))
        self.assertEqual(product.__str__(), product.name)
