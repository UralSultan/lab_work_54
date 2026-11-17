from django.contrib import admin
from .models import Category, Product, Order, ProductOrder


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'created_at', 'price')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 0
    fields = ('product', 'quantity')
    readonly_fields = ('product', 'quantity')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'phone', 'created_at')
    ordering = ('-created_at',)
    inlines = [ProductOrderInline]