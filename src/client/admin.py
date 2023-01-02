from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
import requests
from requests.exceptions import Timeout


class OrderAdmin(admin.ModelAdmin):
   list_display = ('id', 'name', 'phone', 'is_working', 'completed', 'rejected', 'created_at', )
   fields = ('name', 'phone', 'districts', 'address', 'restaurant', 'amount', 'details', 'comment_client', 'getPaymentStatus', 'invoice_id', 'self_pickup', 'user_agent', 'is_working', 'completed', 'rejected', 'comment_agent', 'created_at', 'update_at')
   list_display_links = ('id', 'name')
   search_fields = ('id', 'name', 'phone', 'created_at', 'update_at')
   list_editable = ('is_working', 'completed', 'rejected')
   readonly_fields = ('name', 'phone', 'districts', 'address', 'comment_client', 'amount', 'details', 'self_pickup', 'user_agent', 'created_at', 'update_at', 'invoice_id', 'getPaymentStatus')
   list_filter = ('is_working', 'completed', 'rejected', 'restaurant', 'created_at', 'update_at')

   def getPaymentStatus(self, note):
      try:
         response = requests.get(f'https://api.monobank.ua/api/merchant/invoice/status?invoiceId={note.invoice_id}', headers={"X-Token": "mfvrzEkIfEu3vNrKm6DJhjQ",}, timeout=10,)

         if response.status_code == 200:
            status = response.json()['status']
            if status == 'created':
               return 'Створений'
            elif status == 'processing':
               return 'В процесі'
            elif status == 'hold':
               return 'Заблоковано'
            elif status == 'success':
               return mark_safe("<img src='https://georges.com.ua/static/admin/img/icon-yes.svg'>Оплачено")
            elif status == 'failure':
               return 'Помилка'
            elif status == 'expired':
               return 'Час пройшов'
         else:
            return 'Не створений (готівка)'

      except Timeout:
         return 'Час на запит вичерпано'
   
   getPaymentStatus.short_description = 'Статус оплати'

admin.site.register(Order, OrderAdmin)
admin.site.register(Districts)
admin.site.register(Restaurant)