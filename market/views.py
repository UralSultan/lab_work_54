from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from .models import Product, Category
from .forms import CategoryForm, ProductForm, ProductSearchForm
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class ProductListView(ListView):
    model = Product
    template_name = 'market/products_list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = (Product.objects
                    .select_related('category')
                    .filter(quantity__gt=0)
                    .order_by('category__name', 'name'))

        self.search_form = ProductSearchForm(self.request.GET or None)
        if self.search_form.is_valid():
            name = self.search_form.cleaned_data['name']
            if name:
                queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'market/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_queryset(self):
        return Product.objects.select_related('category')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'market/product_add.html'

    def get_success_url(self):
        return reverse('product_detail', kwargs={'product_id': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'market/product_edit.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse('product_detail', kwargs={'product_id': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'market/product_confirm_delete.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('products_list')


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
