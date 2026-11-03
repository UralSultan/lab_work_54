from django.shortcuts import render
from .models import Product


def products_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'market/products_list.html', {'products': products})