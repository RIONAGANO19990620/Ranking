from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_corporation, name='corporation'),
    path('corporation_quiz', views.quiz_corporation, name='corporation_quiz')
]