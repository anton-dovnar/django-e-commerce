# Generated by Django 3.1.6 on 2021-02-16 22:40

from django.db import migrations, models

import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20210216_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image_mobile',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.upload_to),
        ),
        migrations.AddField(
            model_name='photo',
            name='image_tablet',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.upload_to),
        ),
    ]
