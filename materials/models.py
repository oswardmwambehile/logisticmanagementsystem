# materials/models.py

from django.db import models


class Material(models.Model):

    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)

    stock_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name