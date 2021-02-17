from django.db import models


class ProductManager(models.Manager):
    def list(self):
        first_photo = models.Prefetch('images', to_attr='first_photo')
        qs = self.only(
            'id',
            'slug',
            'category',
            'name',
            'price',
        )
        return qs.filter(available=True).prefetch_related(first_photo)
