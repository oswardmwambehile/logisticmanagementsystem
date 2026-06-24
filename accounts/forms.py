from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


# =========================
# LOGIN FORM
# =========================
class LoginForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Enter your email address'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
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
            'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
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
            'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
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
            'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter your last name'
        })
    )

    # =========================
    # PHONE
    # =========================
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'e.g. +255 712 345 678'
        })
    )

    # =========================
    # PASSWORD 1
    # =========================
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Create a strong password'
        })
    )

    # =========================
    # PASSWORD 2
    # =========================
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
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
    
    

    def save(self, commit=True):
        user = super().save(commit=False)

        # Force every public registration to CUSTOMER
        user.role = "CUSTOMER"

        if commit:
            user.save()

        return user
    


from django import forms
from .models import User


from django import forms
from .models import User


class DriverCreateForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter password"
            }
        )
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500",
                "placeholder": "Confirm password"
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "address",
            "license_number",
            "vehicle_name",
            "vehicle_type",
            "vehicle_model",
            "vehicle_color",
            "vehicle_capacity",
            "vehicle_number",
            "is_available",
        ]

        widgets = {

            "email": forms.EmailInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500",
                    "placeholder": "driver@email.com"
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "First name"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "Last name"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "+255..."
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "Driver address"
                }
            ),

            "license_number": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "Driving license number"
                }
            ),

            "vehicle_name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "Example: Isuzu FTR"
                }
            ),

            "vehicle_type": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
                }
            ),

            "vehicle_model": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "Example: 2022"
                }
            ),

            "vehicle_color": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "White"
                }
            ),

            "vehicle_capacity": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "Example: 5 Tons"
                }
            ),

            "vehicle_number": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
                    "placeholder": "T123 ABC"
                }
            ),

            "is_available": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5 text-green-600 rounded"
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A driver with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = "DRIVER"

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user
    

class DriverUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "address",
            "license_number",
            "vehicle_name",
            "vehicle_type",
            "vehicle_model",
            "vehicle_color",
            "vehicle_capacity",
            "vehicle_number",
            "is_available",
        ]

        widgets = {

            "email": forms.EmailInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "first_name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "phone": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "address": forms.Textarea(attrs={
                "rows": 3,
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "license_number": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "vehicle_name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "vehicle_type": forms.Select(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "vehicle_model": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "vehicle_color": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "vehicle_capacity": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "vehicle_number": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-4 py-2"
            }),

            "is_available": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 text-green-600"
            }),
        }

    def save(self, commit=True):

        user = super().save(commit=False)

        # Keep role as DRIVER
        user.role = "DRIVER"

        if commit:
            user.save()

        return user
    


from django import forms


class PasswordChangeFormCustom(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter old password",
           "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
        })
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter new password",
           "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm new password",
           "class": "w-full border border-gray-300 rounded-xl px-4 py-2",
        })
    )

    # =========================
    # CUSTOM VALIDATIONS
    # =========================

    def clean_new_password(self):
        password = self.cleaned_data.get("new_password")

        # LENGTH CHECK
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long")

        # STRONG PASSWORD RULE (optional)
        if password.isdigit():
            raise forms.ValidationError("Password cannot be only numbers")

        return password

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:

            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data