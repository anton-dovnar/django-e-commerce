from django.test import TestCase, tag
from django.urls import reverse
from model_mommy import mommy

from cart.views import cart_add, cart_detail, cart_remove
from coupon.models import Coupon
from shop.models import Product


@tag('cart-views')
class ViewsTest(TestCase):
    def setUp(self):
        """
        Modify seession (add item to cart).
        Add coupon for discount test.
        """
        self.product = mommy.make(Product)
        self.coupon = mommy.make(Coupon)
        session = self.client.session
        session['cart'] = {str(self.product.id): {'quantity': 1, 'price': str(self.product.price)}}
        session.save()

    def test_cart_add_post(self):
        session = self.client.session
        session['cart'] = {}
        session.save()

        response = self.client.post(
            reverse('cart:cart-add', args=[self.product.id]), data={'quantity': 1})

        self.assertRedirects(
            response,
            reverse('cart:cart-detail'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertEqual(response.resolver_match.func, cart_add)

    def test_update_cart_quantity(self):
        response = self.client.post(
            reverse('cart:cart-add', args=[self.product.id]), data={'quantity': 3, 'override': True})

        self.assertRedirects(
            response,
            reverse('cart:cart-detail'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertEqual(response.resolver_match.func, cart_add)

    def test_cart_remove_post(self):
        response = self.client.post(reverse('cart:cart-remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, cart_remove)

    def test_cart_detail_get(self):
        """
        Testing non empty cart.
        If not empty, render cart detail page.
        """
        response = self.client.get(reverse('cart:cart-detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, cart_detail)
        self.assertTemplateUsed(response, 'cart/cart_detail.html')

    def test_empty_cart_detail_get(self):
        session = self.client.session
        session['cart'] = {}
        session.save()

        response = self.client.get(reverse('cart:cart-detail'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, cart_detail)

    def test_coupon_discount(self):
        session = self.client.session
        session['coupon_id'] = self.coupon.id
        session.save()

        response = self.client.get(reverse('cart:cart-detail'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_coupon(self):
        session = self.client.session
        session['coupon_id'] = 999
        session.save()

        response = self.client.get(reverse('cart:cart-detail'))
        self.assertEqual(response.status_code, 200)
