from decimal import Decimal

from django.test import TestCase, tag
from model_mommy import mommy

from order.models import Order, OrderItem


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
