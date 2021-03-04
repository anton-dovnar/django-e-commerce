from model_mommy import mommy

from shop.models import Category, Product, Size


class SetUpMixin:
    """
    Create Fixtures for testing.
    """

    def setUp(self):
        self.category = mommy.make(Category)
        self.product = mommy.make(Product)
        self.shoe_size = mommy.make(Size)
