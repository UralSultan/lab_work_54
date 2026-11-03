from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField('Наименование', max_length=120, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Товар', max_length=120)
    description = models.TextField('Описание товара',blank=True)
    category = models.ForeignKey('market.Category',null=True, related_name='category', on_delete=models.SET_NULL,
                                 verbose_name='Категория')
    created_at = models.DateTimeField('Дата и время добавления', auto_now_add=True)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    image_url = models.URLField('Изображение')
    quantity = models.IntegerField('Остаток', default=0, validators=[MinValueValidator(0)])


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at', 'name']

    def __str__(self):
        return self.name
