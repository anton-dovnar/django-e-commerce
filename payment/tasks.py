from io import BytesIO

import weasyprint
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from order.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notifications when an order is successfully created.
    """

    order = Order.objects.get(pk=order_id)

    # create invoice e-main
    subject = f'Shoe store - EE Invoice no. {order_id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])

    # generate PDF
    html = render_to_string('order/pdf.html', {'order': order})
    out = BytesIO()
    css_path = settings.BASE_DIR.joinpath('order', 'static', 'order', 'css', 'pdf.css')
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=[weasyprint.CSS(css_path)])

    # attach PDF file / send
    email.attach(f'order_{order_id}.pdf', out.getvalue(), 'application/pdf')
    email.send()
