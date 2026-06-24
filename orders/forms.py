# orders/forms.py

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['delivery_address', 'location']

        widgets = {

            # DELIVERY ADDRESS
            'delivery_address': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-yellow-400',
                'rows': 4,
                'placeholder': 'Enter full delivery address (street, house, etc)'
            }),

            # LOCATION
            'location': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-yellow-400',
                'placeholder': 'Enter location (e.g. Dar es Salaam, Kariakoo)'
            }),
        }


class OrderItemForm(forms.Form):

    quantity = forms.DecimalField(
        min_value=1,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={
            'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-yellow-400',
            'placeholder': 'Enter quantity'
        })
    )

    def __init__(self, *args, material=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.material = material

    def clean_quantity(self):
        qty = self.cleaned_data["quantity"]

        if self.material and qty > self.material.stock_quantity:
            raise forms.ValidationError(
                f"Only {self.material.stock_quantity} available in stock. You cannot Place order above the Stock"
            )

        return qty