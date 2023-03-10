# Generated by Django 3.2 on 2022-07-27 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amountproduct',
            name='price',
        ),
        migrations.RemoveField(
            model_name='sizeproduct',
            name='price',
        ),
        migrations.RemoveField(
            model_name='volumeproduct',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='amount',
        ),
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.amountproduct', verbose_name='Кількість'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.sizeproduct', verbose_name='Розмір'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='volume',
        ),
        migrations.AddField(
            model_name='product',
            name='volume',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.volumeproduct', verbose_name="Об'єм"),
        ),
    ]
