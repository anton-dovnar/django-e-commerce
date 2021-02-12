from django import forms

from cart.cart import Cart
from order.models import Order, OrderItem


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        cart = Cart(self.request)

        if commit:
            instance.save()

        for item in cart:
            OrderItem.objects.create(
                order=instance, product=item['product'], price=item['price'], quantity=item['quantity'])

        cart.clear()
        self.request.session['order_id'] = instance.id
