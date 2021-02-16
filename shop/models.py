import contextlib
from io import BytesIO
from pathlib import PurePath

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image


def upload_to(instance, filename, img):
    suffix = PurePath(filename).suffix
    file_path = settings.BASE_DIR.joinpath('media', f'{instance.product.category.name}')
    file_path.mkdir(parents=True, exist_ok=True)
    file_name = PurePath(f'{instance.product.name}').with_suffix(suffix)

    return PurePath(f'{instance.product.category.name}').joinpath(file_name).as_posix()


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, allow_unicode=True, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product-list-by-category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        index_together = (('id', 'slug'),)
        unique_together = ['category', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product-detail', args=[self.id, self.slug])


class Photo(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image_tablet = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image_mobile = models.ImageField(upload_to=upload_to, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return f'{self.product.name} - {self.image}'

    def clean(self):
        super().clean()
        if self.image is None and self.url is None:
            raise ValidationError('Image and Url cannot be both null.')

    def save(self, *args, **kwargs):
        """
        Downloading image from url.
        """

        if self.url and not self.image:
            category_name = self.product.category.name
            category_path = settings.BASE_DIR.joinpath('media', f'{category_name}')
            category_path.mkdir(parents=True, exist_ok=True)
            stem = PurePath(f'{self.product.name}')

            response = requests.get(self.url)
            if response.status_code == 200:
                with Image.open(BytesIO(response.content)) as img:
                    img.convert('RGB')
                    img.save(category_path.joinpath(f'{stem}.webp').as_posix())

                self.image = PurePath(f'{category_name}').joinpath(f'{stem}.webp').as_posix()

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage

        if self.image:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.image_tablet.path)
                default_storage.delete(self.image_mobile.path)
                default_storage.delete(self.image.path)

        return super().delete(*args, **kwargs)


class Size(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return f'{self.product.name} - {self.size}'
