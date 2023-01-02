from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ім'я")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    districts = models.ForeignKey('Districts', verbose_name='Район', on_delete=models.PROTECT)
    address = models.CharField(max_length=400, verbose_name='Вулиця, будинок')
    amount = models.IntegerField(verbose_name='Вартість замовлення', null=True,)
    invoice_id = models.CharField(max_length=200, verbose_name='Ідентифікатор рахунку', null=True, blank=True)
    details = models.TextField(verbose_name="Деталі")
    restaurant = models.ForeignKey('Restaurant', verbose_name="Заклад", on_delete=models.PROTECT, null=True, blank=True)
    self_pickup = models.BooleanField(verbose_name='Самовивіз', blank=True, default=False)
    comment_client = models.TextField(verbose_name="Коментар від клієнта", blank=True)
    is_working = models.BooleanField(verbose_name='Взято в роботу', default=False)
    completed = models.BooleanField(verbose_name='Завершено', default=False)
    rejected = models.BooleanField(verbose_name='Відхилено', default=False)
    comment_agent = models.TextField(verbose_name="Коментар від агента", blank=True)
    user_agent = models.CharField(max_length=300, verbose_name='UserAgent', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата зміни')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    
class Restaurant(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заклад'
        verbose_name_plural = 'Заклади'

class Districts(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район доставки'
        verbose_name_plural = 'Райони доставки'
