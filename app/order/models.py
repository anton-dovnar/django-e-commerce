"""
Order constructed from 2 main objects:

1. **Order** - order credentials.
2. **Order Item** - ordered products.
"""

from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Order(models.Model):
    """
    The order contains twelve fields:

    - **coupon** - ManyToOne relationship to Coupon.
    - **fist name** - first name such as `Ivan`.
    - **last name** - last name such as `Ivanov`.
    - **email** - email address `ivan.ivanov@gmail.com`.
    - **address** - shipping address `Champ de Mars, 5 Avenue Anatole France`.
    - **postal code** - postal code such as `75007 Paris, France`.
    - **city** - city such as `Paris`.
    - **created** / **updated** - represent date and time of editing object.
    - **paid** - a boolean value that defines paid or not.
    - **braintree id** - keep paid id.
    - **discount** - discount percent, accept integer value, example `25`.
    """

    coupon = models.ForeignKey(
        'coupon.Coupon', related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))


class OrderItem(models.Model):
    """
    The order item contains four fields:

    - **order** - ManyToOne relationship to Order.
    - **prodcut** - ManyToOne relationship to Product.
    - **price** - decimal number with two places such as `100.55`.
    - **quantity** - quantity of particular product.
    """

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
