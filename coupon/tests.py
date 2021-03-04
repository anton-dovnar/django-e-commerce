from django.test import TestCase, tag
from model_mommy import mommy

from coupon.models import Coupon


@tag('coupon-models')
class ModelsTest(TestCase):
    def test_coupon_creation(self):
        coupon = mommy.make(Coupon)
        self.assertIsInstance(coupon, Coupon)
        self.assertEqual(coupon.__str__(), coupon.code)
