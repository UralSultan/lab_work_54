from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from market.models import Product, ProductsInCart
from market.forms import OrderForm
from django.views.generic import ListView
from django.views import View


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
        context['order_form'] = OrderForm()
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