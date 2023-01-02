from django.db import models


class InfoCompany(models.Model):
   instagram_link = models.CharField(max_length=400, verbose_name='Інстаграм (лінк)', blank=True)
   tiktok_link = models.CharField(max_length=400, verbose_name='Тік-ток (лінк)', blank=True)
   facebook_link = models.CharField(max_length=400, verbose_name='Фейсбук (лінк)', blank=True)
   logo_image= models.FileField(upload_to='logo/', verbose_name='Логотип')

   def __str__(self):
      return self.logo_image.url

   class Meta:
      verbose_name = 'Загальна інформація'
      verbose_name_plural = 'Загальна інформація'

class Address(models.Model):
   name = models.CharField(max_length=400, verbose_name='Адреса')
   link = models.CharField(max_length=500, verbose_name='Лінк на google map')

   def __str__(self):
      return self.name

   class Meta:
      verbose_name = 'Адреса'
      verbose_name_plural = 'Адреси'
      
class ScheduleTime(models.Model):
  start_day_time = models.IntegerField(verbose_name='Початок робочого дня') 
  end_day_time = models.IntegerField(verbose_name='Кінець робочого дня') 
  
  def __str__(self):
      return f"З {self.start_day_time} до {self.end_day_time}. (Редагувати)"
      
  class Meta:
      verbose_name = 'Робочі години'
      verbose_name_plural = 'Робочі години'

class Numbers(models.Model):
   value = models.CharField(max_length=50, verbose_name='Номер телефону')

   def __str__(self):
      return self.value

   class Meta:
      verbose_name = 'Номер'
      verbose_name_plural = 'Номери'

class WelcomeSection(models.Model):
   image = models.FileField(upload_to='welcome/', verbose_name='Зображення')
   item_title = models.CharField(max_length=100, verbose_name='Верхній заголовок', blank=True)
   title = models.CharField(max_length=200, verbose_name='Головний заголовок')
   sub_title = models.TextField(verbose_name='Під заголовок', blank=True)

   def __str__(self):
      return self.title

   class Meta:
      verbose_name = 'Головна сторінка'
      verbose_name_plural = 'Головна сторінка'

class MenuSection(models.Model):
   item_title = models.CharField(max_length=100, verbose_name='Верхній заголовок', blank=True)
   title = models.CharField(max_length=200, verbose_name='Головний заголовок')
   sub_title = models.TextField(verbose_name='Під заголовок', blank=True)

   def __str__(self):
      return self.title

   class Meta:
      verbose_name = 'Сторінка меню'
      verbose_name_plural = 'Сторінка меню'

class CategorySection(models.Model):
   item_title = models.CharField(max_length=100, verbose_name='Верхній заголовок', blank=True)
   title = models.CharField(max_length=200, verbose_name='Головний заголовок')
   sub_title = models.TextField(verbose_name='Під заголовок', blank=True)

   def __str__(self):
      return self.title

   class Meta:
      verbose_name = 'Сторінка категорій'
      verbose_name_plural = 'Сторінка категорій'

class ComboSection(models.Model):
   item_title = models.CharField(max_length=100, verbose_name='Верхній заголовок', blank=True)
   title = models.CharField(max_length=200, verbose_name='Головний заголовок')
   sub_title = models.TextField(verbose_name='Під заголовок', blank=True)

   def __str__(self):
      return self.title

   class Meta:
      verbose_name = 'Сторінка комбо'
      verbose_name_plural = 'Сторінка комбо'