from wishlist import views
from django.urls import path


app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>', views.add_wishlist_view, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>', views.remove_wishlist_view, name='remove_from_wishlist'),
]
