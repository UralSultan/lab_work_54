from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from decimal import Decimal
from .models import Product, Category, ProductsInCart
from .forms import CategoryForm, ProductForm, ProductSearchForm
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views import View


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


class CartAddView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        try:
            quantity_to_add = int(request.POST.get('quantity', '1'))
        except (TypeError, ValueError):
            return render(request, 'market/cart_error.html', {'error': 'Введите корректное количество.',})
        if quantity_to_add < 1:
            return render(request, 'market/cart_error.html', {'error': 'Количество должно быть не меньше 1.',})
        cart_item = ProductsInCart.objects.filter(product=product).first()
        current_quantity = (cart_item.quantity_of_product_in_cart if cart_item else 0)
        new_quantity = current_quantity + quantity_to_add
        if new_quantity > product.quantity:
            return render(request, 'market/cart_error.html', {
                'error': (
                    f'Нельзя добавить это количество. '
                    f'В наличии {product.quantity} шт., '
                    f'в корзине уже {current_quantity} шт.'
                ),
            })

        if cart_item:
            cart_item.quantity_of_product_in_cart = new_quantity
            cart_item.save(update_fields=['quantity_of_product_in_cart'])
        else:
            ProductsInCart.objects.create(
                product=product,
                quantity_of_product_in_cart=quantity_to_add,
            )
        return redirect('products_list')


class CartView(ListView):
    model = ProductsInCart
    template_name = 'market/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return ProductsInCart.objects.select_related('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_total'] = sum(
            (item.get_line_total() for item in context['cart_items']),
            Decimal('0.00'),
        )
        return context


class CartRemoveView(View):
    def post(self, request, product_id):
        cart_item = get_object_or_404(
            ProductsInCart,
            product_id=product_id,
        )

        if cart_item.quantity_of_product_in_cart > 1:
            cart_item.quantity_of_product_in_cart -= 1
            cart_item.save(update_fields=['quantity_of_product_in_cart'])
        else:
            cart_item.delete()

        return redirect('cart')