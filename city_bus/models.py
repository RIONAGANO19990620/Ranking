from django.db import models


class Sale(models.Model):
    sale = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.sale)


class CityBus(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
