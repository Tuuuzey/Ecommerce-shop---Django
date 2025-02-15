from . import views
from django.urls import path

app_name = 'checkout'
urlpatterns = [
   path('checkout/', views.checkout_view, name='checkout'),
   path('checkoutpayment/', views.checkout_payment_view, name='checkoutpayment'),
   path('success_checkout/', views.success_checkout_view, name='success_checkout'),
   path('failed_checkout/', views.failed_checkout_view, name='failed_checkout'),
]