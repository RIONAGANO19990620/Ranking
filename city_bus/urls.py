from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_city_bus, name='city_bus'),
]