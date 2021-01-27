from django.test import TestCase, tag
from django.urls import reverse


@tag('shop-views')
class ViewsTest(TestCase):
    def test_product_list_get(self):
        response = self.client.get(reverse('shop:product-list'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('category', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('product_list', response.context)
        self.assertTemplateUsed(response, 'shop/product_list.html')
