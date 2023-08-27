from django.db import models


# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=100)
    rank = models.TextField()

    def __str__(self):
        return self.name
