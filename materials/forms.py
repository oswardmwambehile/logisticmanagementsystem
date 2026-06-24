from django import forms
from .models import MaterialCategory


from django import forms
from .models import MaterialCategory


class MaterialCategoryForm(forms.ModelForm):

    class Meta:
        model = MaterialCategory
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': '''
                    w-full
                    border border-gray-300
                    rounded-xl
                    px-3 py-2
                    text-gray-700
                    focus:outline-none
                    focus:ring-2 focus:ring-blue-500
                    focus:border-blue-500
                    transition
                ''',
                'placeholder': 'Category name'
            }),

            'description': forms.Textarea(attrs={
                'class': '''
                    w-full
                    border border-gray-300
                    rounded-xl
                    px-3 py-2
                    text-gray-700
                    focus:outline-none
                    focus:ring-2 focus:ring-blue-500
                    focus:border-blue-500
                    transition
                ''',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
        }
from django import forms
from .models import Material, MaterialCategory


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = [
            'category',
            'name',
            'description',
            'unit',
            'image',
            'stock_quantity',
            'price'
        ]

        widgets = {

            # CATEGORY DROPDOWN
            'category': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),

            # NAME
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Material name'
            }),

            # DESCRIPTION
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Material description'
            }),

            # UNIT DROPDOWN
            'unit': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),

            # IMAGE UPLOAD
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2'
            }),

            # STOCK
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'e.g. 100'
            }),

            # PRICE
            'price': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'e.g. 15000'
            }),
        }


from django import forms
from .models import StockMovement


class StockMovementForm(forms.ModelForm):

    class Meta:
        model = StockMovement
        fields = ['material', 'movement_type', 'quantity', 'note']

        widgets = {

            # MATERIAL SELECT
            'material': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),

            # IN / OUT
            'movement_type': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),

            # QUANTITY
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter quantity'
            }),

            # NOTE
            'note': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Optional note'
            }),
        }