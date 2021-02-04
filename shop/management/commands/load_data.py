import json
from pathlib import PurePath
from io import BytesIO

from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
import requests

from shop.models import Category, Product, Photo, Size


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

                product, created = Product.objects.get_or_create(
                    category=category, name=item['name'][0],
                    price=float(item['price'][0][1:]), description=item['description'][0],
                )

                photo, created = Photo.objects.get_or_create(
                    product=product, url=item['photo'][1])

                if created:
                    photo.image = self.download(photo, item['photo'][1])
                    photo.save()

                size, created = Size.objects.get_or_create(
                    product=product, size='US 10')

                if created:
                    size.save()
