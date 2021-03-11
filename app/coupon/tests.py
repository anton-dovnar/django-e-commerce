from django.test import TestCase, tag
from django.urls import reverse
from django.utils import timezone
from model_mommy import mommy

from coupon.models import Coupon
from coupon.views import coupon_apply


@tag('coupon-models')
class ModelsTest(TestCase):
    def test_coupon_creation(self):
        coupon = mommy.make(Coupon)
        self.assertIsInstance(coupon, Coupon)
        self.assertEqual(coupon.__str__(), coupon.code)


@tag('coupon-views')
class ViewsTest(TestCase):
    def setUp(self):
        now = timezone.now()
        self.coupon = Coupon.objects.create(
            code='123', valid_from=now, valid_to=now + timezone.timedelta(days=1), discount=50, active=True)

    def test_valid_coupon(self):
        response = self.client.post(reverse('coupon:apply'), data={'code': self.coupon.code})
        session = response.client.session
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, coupon_apply)
        self.assertEqual(session['coupon_id'], self.coupon.id)

    def test_invalid_coupon(self):
        self.coupon.active = False
        self.coupon.save()
        response = self.client.post(reverse('coupon:apply'), data={'code': self.coupon.code})
        session = response.client.session
        self.assertEqual(session['coupon_id'], None)
