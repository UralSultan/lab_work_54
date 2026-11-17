from django.urls import reverse, reverse_lazy
from market.models import Product, ProductsInCart
from market.forms import  ProductForm, ProductSearchForm
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
        products = list(context['products'])
        product_ids = [product.id for product in products]
        cart_quantities = {
            item.product_id: item.quantity_of_product_in_cart
            for item in ProductsInCart.objects.filter(product_id__in=product_ids)}
        for product in products:
            product.available_quantity = (product.quantity - cart_quantities.get(product.id, 0))
        context['products'] = products
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