# Generated by Django 3.1.6 on 2021-02-16 12:36

from django.db import migrations, models

import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210205_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to=shop.models.upload_to),
        ),
    ]
