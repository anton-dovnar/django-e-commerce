from django.test import SimpleTestCase, tag
from django.urls import resolve, reverse

from shop.views import ProductDetailView, ProductListView


@tag('shop-urls')
class UrlsTest(SimpleTestCase):
    def test_product_list_url_resolves(self):
        url = reverse('shop:product-list')

        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_list_by_category_url_resolves(self):
        url = reverse(
            'shop:product-list-by-category',
            args=['nike-sb-zoom-blazer-mid-edge']
        )

        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_detail_url_resolves(self):
        url = reverse(
            'shop:product-detail',
            args=[1, 'nike-sb-zoom-blazer-mid-edge']
        )

        self.assertEqual(resolve(url).func.view_class, ProductDetailView)
