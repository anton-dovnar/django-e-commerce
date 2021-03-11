import json
import random

from django.conf import settings
from django.core.management.base import BaseCommand

from shop.models import Category, Photo, Product, Size


class Command(BaseCommand):

    @staticmethod
    def random_size():
        sizes = [i for i in range(37, 47)]
        return str(random.choice(sizes))

    def handle(self, *args, **options):
        products = settings.BASE_DIR.joinpath('products.json')

        with open(products, encoding='utf-8') as f:
            data = json.load(f)

            for item in data:
                category, created = Category.objects.get_or_create(name=item['category'][0])

                if created:
                    category.save()

                try:
                    product = Product.objects.get(category=category, name=item['name'][0])
                except Product.DoesNotExist:
                    product = Product(category=category, name=item['name'][0])

                product.price = float(item['price'][0][1:])
                product.description = item['description'][0]
                product.save()

                photo, created = Photo.objects.get_or_create(
                    product=product, url=item['photo'][1])

                if created:
                    photo.save()

                size, created = Size.objects.get_or_create(product=product)

                if created:
                    size.size = self.random_size()
                    size.save()
