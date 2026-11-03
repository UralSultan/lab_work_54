from django.shortcuts import render, get_object_or_404
from .models import Product


def products_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'market/products_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product.objects.select_related('category'),pk=product_id)
    return render(request, 'market/product_detail.html', {'product': product})