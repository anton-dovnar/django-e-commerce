from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    """
    Coupon contains five fields:

    - **code** - coupon keyword for discount, example `big sale`.
    - **valid from** - when start discount (date/time).
    - **valid to** - when end discount (date/time).
    - **discount** - discount percent, accept integer value, example `25`.
    - **active** - a boolean value that check code is active or not.
    """

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code
