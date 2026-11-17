from django import forms
from market.models import Category, Product, Order


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']