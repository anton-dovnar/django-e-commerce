from django.conf import settings
from django.test import override_settings
from model_mommy import mommy

from shop.models import Category, Photo, Product, Size


class SetUpMixin:
    """
    Create Fixtures for testing.
    """

    @override_settings(MEDIA_ROOT=str(settings.BASE_DIR.joinpath('test_media')))
    def setUp(self):
        self.category = mommy.make(Category)
        self.product = mommy.make(Product)
        self.shoe_size = mommy.make(Size)
        self.photo = Photo.objects.create(product=self.product, image='model.jpeg')

    def tearDown(self):
        self.photo.delete()
