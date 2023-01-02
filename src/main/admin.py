from django.contrib import admin
from .models import *

class InfoCompanyAdmin(admin.ModelAdmin):
   list_display = ('id', 'instagram_link', 'tiktok_link', 'facebook_link', )
   list_editable = ('instagram_link', 'tiktok_link', 'facebook_link', )
   
class ScheduleTimeAdmin(admin.ModelAdmin):
   list_display = ('start_day_time', 'end_day_time') 
   list_editable = ('start_day_time', 'end_day_time') 

admin.site.register(InfoCompany, InfoCompanyAdmin)
admin.site.register(Address)
admin.site.register(Numbers)
admin.site.register(WelcomeSection)
admin.site.register(MenuSection)
admin.site.register(CategorySection)
admin.site.register(ComboSection)
admin.site.register(ScheduleTime)

admin.site.site_title = "George's"
admin.site.site_header = "GEORGE'S"