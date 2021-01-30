# Generated by Django 3.1.5 on 2021-01-30 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_productsize'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductPhoto',
            new_name='Photo',
        ),
        migrations.RenameModel(
            old_name='ProductSize',
            new_name='Size',
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name': 'Size', 'verbose_name_plural': 'Sizes'},
        ),
    ]
