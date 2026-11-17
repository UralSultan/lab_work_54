from django import forms
from market.models import Category, Product, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'address', 'phone']
        labels = {
            'user': 'Имя',
            'address': 'Адрес',
            'phone': 'Телефон',
        }