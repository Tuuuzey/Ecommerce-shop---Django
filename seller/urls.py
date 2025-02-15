from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('becomeaseller/', views.newseller_view, name='newseller'),
    path('addproducts/', views.add_products_view, name='addproducts'),
    path('not_seller/', views.not_seller_view, name='notseller'),
    path('sellers_prods/', views.sellers_prods, name='sellers_prods'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product')
]
