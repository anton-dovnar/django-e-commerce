import braintree
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin

from order.models import Order
from payment.tasks import payment_completed
from shop.recommender import Recommender

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


class ProcessView(SingleObjectMixin, TemplateView):
    model = Order
    template_name = 'payment/process.html'

    def get_object(self):
        """
        Getting order by order id from the session variable.
        """

        order_id = self.request.session.get('order_id')
        return get_object_or_404(self.model, id=order_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_token'] = gateway.client_token.generate()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        If the payment process successful, we create an index for products with Redis.
        Add celery task, which sends email invoice with order information [[tasks.py]].
        """

        order = self.get_object()
        total_cost = order.get_total_cost()
        r = Recommender()
        nonce = self.request.POST.get('payment_method_nonce', None)
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            r.products_bought(order.items.all())
            payment_completed.apply_async([order.pk])
            return redirect('payment:done')

        return redirect('payment:canceled')


class ProcessMixin:
    """
    Display process status.
    """

    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id', None)

        if order_id:
            del request.session['order_id']
            return super().get(request, *args, **kwargs)

        raise Http404('Page does not exist')


class DoneTemplateView(ProcessMixin, TemplateView):
    template_name = 'payment/done.html'


class CanceledTemplateView(ProcessMixin, TemplateView):
    template_name = 'payment/canceled.html'
