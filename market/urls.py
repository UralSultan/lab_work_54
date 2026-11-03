from django.urls import path
from . import views


urlpatterns = [
    path('', views.products_view, name='products_list'),
    path('products/', views.products_view, name='products_list'),
    path('products/add', views.product_add_view, name='product_add'),
    path('products/<int:product_id>/', views.product_view, name='product_detail'),
    path('categories/add', views.category_add_view, name='category_add'),
]
