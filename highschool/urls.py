from django.urls import path

from highschool import views

app_name = 'highschool'
urlpatterns = [
    path('', views.search_highschool, name='high_school'),
    path('high_school_quiz', views.quiz_highschool, name='high_school_quiz')
]