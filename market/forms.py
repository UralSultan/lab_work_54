from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class ProductForm(forms.ModelForm):
    quantity = forms.IntegerField(
        label='Остаток',
        min_value=0,
        initial=0
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image_url', 'quantity']

class ProductSearchForm(forms.Form):
    name = forms.CharField(
        label="Название товара",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Введите название товара",
        }),
    )
