# Generated by Django 3.2 on 2022-08-13 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_published'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CategoryCombo',
        ),
    ]
