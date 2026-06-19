# tracking/models.py

from django.db import models


class Tracking(models.Model):

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)

    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    updated_at = models.DateTimeField(auto_now=True)