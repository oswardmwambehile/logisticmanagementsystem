from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


# =========================
# LOGIN FORM
# =========================
class LoginForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Enter your email address'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Enter your password'
    }))


# =========================
# REGISTER FORM (CUSTOMER ONLY)
# =========================
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone',
            'password1',
            'password2'
        ]

    # =========================
    # EMAIL
    # =========================
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'example@gmail.com'
        })
    )

    # =========================
    # FIRST NAME
    # =========================
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your first name'
        })
    )

    # =========================
    # LAST NAME
    # =========================
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your last name'
        })
    )

    # =========================
    # PHONE
    # =========================
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'e.g. +255 712 345 678'
        })
    )

    # =========================
    # PASSWORD 1
    # =========================
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Create a strong password'
        })
    )

    # =========================
    # PASSWORD 2
    # =========================
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirm your password'
        })
    )

    # =========================
    # CUSTOM VALIDATIONS
    # =========================

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")

        return email

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')

        if not name.isalpha():
            raise ValidationError("First name must contain only letters.")

        return name

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name')

        if not name.isalpha():
            raise ValidationError("Last name must contain only letters.")

        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone:
            if len(phone) < 10:
                raise ValidationError("Phone number is too short.")

        return phone

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords do not match!")

        return cleaned_data