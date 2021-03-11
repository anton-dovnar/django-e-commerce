from django.test import TestCase, tag
from django.urls import reverse

from shop.tests.mixins import SetUpMixin
from shop.views import ProductDetailView, ProductListView


@tag('shop-views')
class ViewsTest(SetUpMixin, TestCase):
    def test_product_list_get(self):
        response = self.client.get(reverse('shop:product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, ProductListView.as_view().__name__)
        self.assertIn('category', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('product_list', response.context)
        self.assertTemplateUsed(response, 'shop/product_list.html')

    def test_product_list_by_category_get(self):
        response = self.client.get(reverse('shop:product-list-by-category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_get(self):
        response = self.client.get(reverse('shop:product-detail', args=[self.product.pk, self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, ProductDetailView.as_view().__name__)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
