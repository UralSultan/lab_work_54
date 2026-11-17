from django.db import models
from django.core.validators import MinValueValidator


class ProductsInCart(models.Model):
    product = models.ForeignKey('market.Product', on_delete=models.CASCADE)
    quantity_of_product_in_cart = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        ordering = ['product__name']
        constraints = [
            models.UniqueConstraint(
                fields=['product'],
                name='one_cart_row_per_product'
            )
        ]

    def get_line_total(self):
        return self.product.price * self.quantity_of_product_in_cart

    def __str__(self):
        return self.product.name