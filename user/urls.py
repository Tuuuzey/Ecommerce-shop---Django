from django.urls import path
from user import views as user_views

app_name = 'user'

urlpatterns = [
    path('profile/', user_views.profile_view, name='profile'),
    path('orders/', user_views.orders_view, name='orders'),
    path('forgot_password/', user_views.forgot_password_view, name='forgot_password'),
]
