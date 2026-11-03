from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import CategoryForm, ProductForm


def products_view(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'market/products_list.html', {'products': products})

def product_view(request, product_id):
    product = get_object_or_404(Product.objects.select_related('category'),pk=product_id)
    return render(request, 'market/product_detail.html', {'product': product})

def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()

    return render(request, 'market/product_add.html', {'form': form})

def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = CategoryForm()
    return render(request, 'market/category_add.html', {'form': form})


def categories_view(request):
    categories = Category.objects.all()
    return render(
        request,
        'market/categories_list.html',
        {'categories': categories}
    )