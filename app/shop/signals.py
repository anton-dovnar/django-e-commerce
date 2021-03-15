from pathlib import PurePath

from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

from shop.models import Photo


@receiver(post_save, sender=Photo)
def convert_image(sender, instance, **kwargs):
    """
    - Trigger on Django admin upload image.
    - Resize an image for multiple devices.
    - Convert image to WEBP.
    - Improve load page performance.
    """

    if not instance.image_tablet:
        image_path = PurePath(instance.image.path)
        stem = image_path.stem
        category_path = image_path.parent
        category_name = instance.product.category.name

        with Image.open(instance.image.path) as img:
            img.convert('RGB')
            img.save(category_path.joinpath(f'{stem}.webp').as_posix())

            img.thumbnail((768, 960), Image.ANTIALIAS)
            img.save(category_path.joinpath(f'{stem}-md.webp').as_posix())

            img.thumbnail((540, 675), Image.ANTIALIAS)
            img.save(category_path.joinpath(f'{stem}-sm.webp').as_posix())

        instance.image = PurePath(f'{category_name}').joinpath(f'{stem}.webp').as_posix()
        instance.image_tablet = PurePath(f'{category_name}').joinpath(f'{stem}-md.webp').as_posix()
        instance.image_mobile = PurePath(f'{category_name}').joinpath(f'{stem}-sm.webp').as_posix()
        instance.save()
