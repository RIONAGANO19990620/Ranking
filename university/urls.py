from django.urls import path
from university import views


app_name = 'university'
urlpatterns = [
    path('', views.search_university, name='university')
]