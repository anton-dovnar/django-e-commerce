# Generated by Django 3.1.6 on 2021-02-16 13:27

from django.db import migrations, models

import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210216_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(null=True, upload_to=shop.models.upload_to),
        ),
        migrations.AlterField(
            model_name='photo',
            name='url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
