from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_corporation, name='home')
]