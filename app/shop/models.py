"""
Shop constructed from 4 main objects:

1. **Category** - define a category for products ([[models.py#category]])
2. **Product** - contains all necessary information about the product ([[models.py#product]])
3. **Photo** - product photo ([[models.py#photo]])
4. **Size** - product size ([[models.py#size]])
"""
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

from shop.managers import ProductManager


def upload_to(instance, filename, img):
    """
    Defines path how we serve media files locally. (Images)
    It will look like / media / category name / file name
    """
    suffix = PurePath(filename).suffix
    file_path = settings.BASE_DIR.joinpath('media', f'{instance.product.category.name}')
    file_path.mkdir(parents=True, exist_ok=True)
    file_name = PurePath(f'{instance.product.name}').with_suffix(suffix)
    return PurePath(f'{instance.product.category.name}').joinpath(file_name).as_posix()


# === Category ===
class Category(models.Model):
    """
    Category contain two fileds:

    - **name** particular object name.
    - **slug** represented name for URL resolver.
    """
    name = models.CharField(max_length=50, db_index=True, unique=True)
    slug = models.SlugField(max_length=50, db_index=True, allow_unicode=True, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product-list-by-category', args=[self.slug])


# === Product ===
class Product(models.Model):
    """
    The product contains eight fields and one custom model manager:

    - **category** ManyToOne relationship to Category ([[models.py#category]])
    - **name** particular object name.
    - **slug** represented name for URL resolver.
    - **description** particular object description.
    - **price** decimal number with two places such as `100.55`.
    - **available** boolean value for checking object is available for selling or not.
    - **created** / ::updated:: represent date and time of editing object.
    - **objects** predefined custom model manager, which helps us optimize database query access ([[managers.py]])
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        index_together = (('id', 'slug'),)
        unique_together = ['category', 'name']
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product-detail', args=[self.id, self.slug])


# === Photo ===
class Photo(models.Model):
    """
    The photo contains five fields:

    - **product** ManyToOne relationship to Product ([[models.py#product]]).
    - **image** big resolution image for desktop users.
    - **image_tablet** resize image to (768, 960) for best practice.
    - **image_mobile** resize image to (540, 675) for bets mobile practice.
    - **url** if we don't have an image locally we also can set an external URL for downloading the image.

    Redefined methods:

    1. **clean** [[models.py#clean]]
    2. **save** [[models.py#save]]
    3. **delete** [[models.py#delete]]
    """
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

    # ==== clean ====
    def clean(self):
        """
        Validate image uploading.
        Image and URL fields cannot be both empty.
        """
        super().clean()
        if not self.image and self.url is None:
            raise ValidationError('Image and Url cannot be both null.')

    # ==== save ====
    def save(self, *args, **kwargs):
        """
        Downloading images from external URLs and serve them locally.
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

        super().save(*args, **kwargs)

    # ==== delete ====
    def delete(self, *args, **kwargs):
        """
        When a product is deleting from the database, we also remove images from local storage.
        """
        from django.core.files.storage import default_storage

        if self.image:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.image_tablet.path)
                default_storage.delete(self.image_mobile.path)
                default_storage.delete(self.image.path)

        super().delete(*args, **kwargs)


# === Size ===
class Size(models.Model):
    """
    Model size contains two fields:

    - **product** ManyToOne relationship to Product ([[models.py#product]]).
    - **size** particular product size.
    """
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return f'{self.product.name} - {self.size}'
