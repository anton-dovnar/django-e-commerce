from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupon.forms import CouponApplyForm
from coupon.models import Coupon


@require_POST
def coupon_apply(request):
    """
    Check coupon for availability.
    If available, add coupon id into user session.
    """

    now = timezone.now()
    form = CouponApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart:cart-detail')
