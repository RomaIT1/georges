# Generated by Django 3.2 on 2022-08-29 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_scheduletime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scheduletime',
            options={'verbose_name': 'Робочі години', 'verbose_name_plural': 'Робочі години'},
        ),
    ]
