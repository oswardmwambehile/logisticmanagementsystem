from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    # ❌ remove username (we use email login)
    username = None

    # =========================
    # BASIC AUTH FIELDS
    # =========================
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    phone = models.CharField(max_length=20, blank=True, null=True)

    # =========================
    # ROLE SYSTEM
    # =========================
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('CUSTOMER', 'Customer'),
        ('DRIVER', 'Driver'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CUSTOMER'
    )

    # =========================
    # DRIVER FIELDS
    # =========================
    license_number = models.CharField(max_length=100, blank=True, null=True)
    vehicle_number = models.CharField(max_length=100, blank=True, null=True)

    vehicle_name = models.CharField(
            max_length=150,
            blank=True,
            null=True
        )

    VEHICLE_TYPES = (
        ("TRUCK", "Truck"),
        ("PICKUP", "Pickup"),
        ("TRAILER", "Trailer"),
        ("VAN", "Van"),
        ("MOTORCYCLE", "Motorcycle"),
    )

    vehicle_type = models.CharField(
        max_length=30,
        choices=VEHICLE_TYPES,
        blank=True,
        null=True
    )

    
    vehicle_model = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    vehicle_color = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )



    vehicle_capacity = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Example: 5 Tons"
    )

   
    address = models.TextField(
        blank=True,
        null=True
    )

    is_available = models.BooleanField(default=True)

    # =========================
    # SYSTEM SETTINGS
    # =========================
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()