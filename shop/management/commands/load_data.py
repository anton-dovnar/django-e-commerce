import json
from io import BytesIO
from pathlib import PurePath

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image

from shop.models import Category, Photo, Product, Size


class Command(BaseCommand):
    def download(self, instance, url):
        suffix = PurePath(url).suffix
        file_path = settings.BASE_DIR.joinpath(
            'media', f'{instance.product.name}{suffix}')
        req = requests.get(url)

        if req.status_code == 200:
            with Image.open(BytesIO(req.content)) as img:
                img.save(file_path)

            print(f'Dowloading form: {url} saving to: {file_path}')

            return f'{instance.product.name}{suffix}'

    def handle(self, *args, **options):
        products = settings.BASE_DIR.joinpath('products.json')

        with open(products, encoding='utf-8') as f:
            data = json.load(f)

            for item in data:
                category, created = Category.objects.get_or_create(
                    name=item['category'][0])

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
                    photo.image = self.download(photo, item['photo'][1])
                    photo.save()

                size, created = Size.objects.get_or_create(
                    product=product, size='US 10')

                if created:
                    size.save()
