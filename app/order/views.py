import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView

from cart.cart import Cart
from order.forms import OrderForm
from order.models import Order


class OrderFormView(FormView):
    form_class = OrderForm
    template_name = 'order/order_create.html'
    success_url = reverse_lazy('payment:process')

    def get_form_kwargs(self):
        """
        Put a cart to the form kwargs for getting cart items when saving order.
        """

        kwargs = super().get_form_kwargs()
        kwargs['cart'] = Cart(self.request)
        return kwargs

    def form_valid(self, form):
        """
        Define order id to the session for future manipulations.
        If the customer paid the order successfully, we will be sending a mail message.
        For getting email address we need an order id thats why we putting order id to the seession.
        """

        order_id = form.save()
        self.request.session['order_id'] = order_id
        return super().form_valid(form)


@staff_member_required
def admin_order_detail(request, order_id):
    """
    Add custom order detail page for administrator.
    This page contains a list of order items and order credentials.
    """

    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/order_detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Generate invoice pdf.
    """

    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    css_path = settings.BASE_DIR.joinpath('order', 'static', 'order', 'css', 'pdf.css')
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(css_path)])
    return response
