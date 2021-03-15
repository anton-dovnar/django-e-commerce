from django import forms
from django.db import transaction

from order.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """
    Order model form.
    Redefined save method.
    """

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Get discount.
        Create order items and set related to the current order.
        At the end clear the cart.
        """

        instance = super().save(commit=False)

        if self.cart.coupon:
            instance.coupon = self.cart.coupon
            instance.discount = self.cart.coupon.discount

        if commit:
            with transaction.atomic():
                instance.save()

                for item in self.cart:
                    OrderItem.objects.create(
                        order=instance, product=item['product'], price=item['price'], quantity=item['quantity'])

        self.cart.clear()
        return instance.id
