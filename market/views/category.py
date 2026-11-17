from django.shortcuts import render, get_object_or_404, redirect
from market.models import Category
from market.forms import CategoryForm


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

def category_edit_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'market/category_edit.html', {
        'form': form,
        'category': category,
    })


def category_delete_view(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
    return redirect('categories_list')