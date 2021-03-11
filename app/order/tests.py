from decimal import Decimal

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.test import TestCase, tag
from django.urls import reverse
from model_mommy import mommy

from coupon.models import Coupon
from order.models import Order, OrderItem
from order.views import OrderFormView, admin_order_detail, admin_order_pdf
from shop.models import Product


@tag('order-models')
class ModelsTest(TestCase):
    def setUp(self):
        self.order = mommy.make(Order)
        self.order_item = mommy.make(OrderItem)

    def test_order_creation(self):
        self.assertIsInstance(self.order, Order)
        self.assertEqual(self.order.__str__(), f'Order {self.order.id}')
        self.assertIsInstance(self.order.get_total_cost(), Decimal)

    def test_order_item_creation(self):
        self.assertIsInstance(self.order_item, OrderItem)
        self.assertEqual(self.order_item.__str__(), str(self.order_item.id))
        self.assertIsInstance(self.order_item.get_cost(), Decimal)


@tag('order-views')
class ViewsTest(TestCase):
    def setUp(self):
        self.order = mommy.make(Order)
        self.product = mommy.make(Product)
        self.coupon = mommy.make(Coupon)
        session = self.client.session
        session['cart'] = {str(self.product.id): {'quantity': 1, 'price': str(self.product.price)}}
        session['coupon_id'] = self.coupon.id
        session.save()
        self.client.force_login(User.objects.create_superuser(username='test'))

    def test_order_form_post(self):
        data = model_to_dict(self.order)
        data.pop('coupon')
        response = self.client.post(reverse('order:order-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func.__name__, OrderFormView.as_view().__name__)

    def test_admin_order_detail_get(self):
        response = self.client.get(reverse('order:admin-order-detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, admin_order_detail)

    def test_admin_order_pdf(self):
        response = self.client.get(reverse('order:admin-order-pdf', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, admin_order_pdf)
