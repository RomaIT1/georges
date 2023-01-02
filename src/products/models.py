from django.db import models
from django.urls import reverse


class Product(models.Model):
   name = models.CharField(max_length=200, verbose_name='Назва')
   price = models.IntegerField(verbose_name='Ціна')
   category = models.ForeignKey('CategoryProduct', verbose_name='Категорія', on_delete=models.PROTECT)
   size = models.ForeignKey('SizeProduct', verbose_name="Розмір", blank=True, on_delete=models.PROTECT, null=True)
   volume = models.ForeignKey('VolumeProduct', verbose_name="Об'єм", blank=True, on_delete=models.PROTECT, null=True)
   amount = models.ForeignKey('AmountProduct', verbose_name="Кількість", blank=True, on_delete=models.PROTECT, null=True)
   description = models.TextField(verbose_name='Опис', blank=True)
   image = models.ImageField(upload_to='products/', verbose_name='Картинка')
   image_mobile = models.ImageField(upload_to='products/mobile', verbose_name='Картинка для mobile', blank=True, null=True)
   published = models.BooleanField(verbose_name="Опублікований", default=False)

   def __str__(self):
      return self.name

   class Meta:
      verbose_name = 'Продукт'
      verbose_name_plural = 'Продукти'

class Combo(models.Model):
   product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.PROTECT)
   price = models.IntegerField(verbose_name="Ціна")

   def __str__(self):
      return self.product.name

   class Meta:
      verbose_name = 'Комбо меню'
      verbose_name_plural = 'Комбо меню'

class SizeProduct(models.Model):
   value = models.CharField(max_length=100, verbose_name='Значення')

   def __str__(self):
      return f'{self.value}'

   class Meta:
      verbose_name = 'Розмір'
      verbose_name_plural = 'Розміри'

class VolumeProduct(models.Model):
   value = models.CharField(max_length=100, verbose_name='Значення')

   def __str__(self):
      return f'{self.value}'
   
   class Meta:
      verbose_name = "Об'єм"
      verbose_name_plural = "Об'єми"

class AmountProduct(models.Model):
   value = models.CharField(max_length=100, verbose_name='Значення')

   def __str__(self):
      return f'{self.value}'

   class Meta:
      verbose_name = "Кількість"
      verbose_name_plural = "Кількості"

class CategoryProduct(models.Model):
   name = models.CharField(max_length=200, verbose_name='Категорія')
   image = models.ImageField(upload_to='categories/', verbose_name='Зображення')
   slug = models.SlugField(max_length = 200, verbose_name='Слаг')

   def get_absolute_url(self):
      return reverse('category', kwargs={'slug_category': self.slug})

   def __str__(self):
      return self.name

   class Meta:
      verbose_name = "Категорія"
      verbose_name_plural = "Категорії"