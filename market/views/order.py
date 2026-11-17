from django.shortcuts import redirect
from django.urls import  reverse_lazy
from decimal import Decimal
from market.models import  ProductsInCart, Order, ProductOrder
from market.forms import  OrderForm
from django.views.generic import CreateView


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'market/cart.html'
    success_url = reverse_lazy('products_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = list(ProductsInCart.objects.select_related('product'))
        context['cart_items'] = cart_items
        context['cart_total'] = sum((item.get_line_total() for item in cart_items),Decimal('0.00'),)
        context['order_form'] = context['form']
        return context

    def form_valid(self, form):
        cart_items = list(ProductsInCart.objects.select_related('product'))
        if not cart_items:
            form.add_error(None, 'Корзина пуста.')
            return self.form_invalid(form)
        for item in cart_items:
            if item.quantity_of_product_in_cart > item.product.quantity:
                form.add_error(
                    None,
                    f'Недостаточно товара «{item.product.name}» на складе.',
                )
                return self.form_invalid(form)
        self.object = form.save()
        for item in cart_items:
            ProductOrder.objects.create(
                order=self.object,
                product=item.product,
                quantity=item.quantity_of_product_in_cart,
            )
            item.product.quantity -= item.quantity_of_product_in_cart
            item.product.save(update_fields=['quantity'])
        ProductsInCart.objects.all().delete()
        return redirect(self.get_success_url())