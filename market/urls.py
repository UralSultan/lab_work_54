from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='products_list'),
    path('products/', views.ProductListView.as_view(), name='products_list'),
    path('products/add', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:product_id>/edit', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:product_id>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
    path('categories/add', views.category_add_view, name='category_add'),
    path('categories', views.categories_view, name='categories_list'),
    path('categories/<int:category_id>/edit', views.category_edit_view, name='category_edit'),
    path('categories/<int:category_id>/delete', views.category_delete_view, name='category_delete'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('products/<int:product_id>/cart/add/',views.CartAddView.as_view(),name='cart_add',),
    path('cart/remove/<int:product_id>/',views.CartRemoveView.as_view(),name='cart_remove',),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
]
