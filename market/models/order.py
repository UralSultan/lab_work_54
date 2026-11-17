from django.core.validators import MinValueValidator
from django.db import models


class ProductOrder(models.Model):
    order = models.ForeignKey('market.Order', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('market.Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField('Количество',validators=[MinValueValidator(1)],)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='one_product_per_order',
            )
        ]

    def __str__(self):
        return f'{self.product.name} — {self.quantity} шт.'


class Order(models.Model):
    user = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=120)
    address = models.CharField('Адрес', max_length=120)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True)
    products = models.ManyToManyField('market.Product', through='ProductOrder', related_name='orders')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.pk}'
