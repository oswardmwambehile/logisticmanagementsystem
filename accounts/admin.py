from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    # =========================
    # LIST DISPLAY
    # =========================
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "phone",
        "is_verified",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
    )

    ordering = ("email",)

    # =========================
    # FIELD LAYOUT (VIEW USER)
    # =========================
    fieldsets = (
        ("Login Info", {
            "fields": ("email", "password")
        }),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "phone")
        }),
        ("Role Management", {
            "fields": ("role", "is_verified", "is_active", "is_staff", "is_superuser")
        }),
        ("Driver Details", {
            "fields": ("license_number", "vehicle_number", "is_available")
        }),
        ("System Info", {
            "fields": ("last_login", "date_joined")
        }),
    )

    # =========================
    # ADD USER FORM (ADMIN PANEL)
    # =========================
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "role",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )