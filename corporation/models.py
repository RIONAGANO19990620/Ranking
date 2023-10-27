from django.db import models


# Create your models here.

class Corporation(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return self.name


class QuizHistory(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)  # クイズの正解
    user_answer = models.CharField(max_length=255)  # ユーザーの回答
    is_correct = models.BooleanField()  # クイズの正誤

    created_at = models.DateTimeField(auto_now_add=True)