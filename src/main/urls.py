from django.urls import path
from . import views

urlpatterns = [
   path('', views.main, name='home'),
   path('combos/', views.combo, name='combo'),
   path('thanks/', views.thanks, name='thanks'),
   path('<slug:slug_category>/', views.category, name='category'),
]
