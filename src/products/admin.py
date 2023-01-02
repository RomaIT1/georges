import django
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
class ProductAdmin(admin.ModelAdmin):
   list_display = ('id', 'name', 'price', 'category', 'published', 'getPhoto', )
   list_display_links = ('id', 'name')
   search_fields = ('id', 'name')
   list_editable = ('price', 'category', 'published', )
   readonly_fields = ('getPhoto', )
   def getPhoto(self, obj):
      return mark_safe(f"<img src='{obj.image.url}' width='90px'>")

   getPhoto.short_description = 'Зображення'

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(AmountProduct)
admin.site.register(SizeProduct)
admin.site.register(VolumeProduct)
admin.site.register(CategoryProduct)
admin.site.register(Combo)