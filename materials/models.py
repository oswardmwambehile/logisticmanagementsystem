# materials/models.py

from django.db import models


class MaterialCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

from django.db import models


class Material(models.Model):
    UNIT_CHOICES = (
        ('BAG', 'Bag'),
        ('TON', 'Ton'),
        ('KG', 'Kilogram'),
        ('PCS', 'Pieces'),
        ('TRUCK', 'Truck Load'),
        ('M3', 'Cubic Meter'),
    )


    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
        related_name="materials"
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='BAG'
    )
    image = models.ImageField(
        upload_to="materials/",
        blank=True,
        null=True
    )

    stock_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class StockMovement(models.Model):

    MOVEMENT_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="movements"
    )

    movement_type = models.CharField(
        max_length=10,
        choices=MOVEMENT_TYPES
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:

            if self.movement_type == "IN":
                self.material.stock_quantity += self.quantity

            elif self.movement_type == "OUT":
                self.material.stock_quantity -= self.quantity

            self.material.save()