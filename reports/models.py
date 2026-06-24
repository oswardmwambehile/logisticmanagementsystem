from django.db import models

class DailyReport(models.Model):
    date = models.DateField(auto_now_add=True, unique=True)

    total_orders = models.IntegerField(default=0)
    delivered_orders = models.IntegerField(default=0)
    pending_orders = models.IntegerField(default=0)

    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return str(self.date)