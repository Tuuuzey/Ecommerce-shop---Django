from django.contrib import admin
from .models import Address, PromoCode, Transaction, Order, OrderItem

# Register your models here.

admin.site.register(Address)
admin.site.register(PromoCode)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(OrderItem)