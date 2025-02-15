from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from shop.models import Products
# Create your models here.

class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    value = models.IntegerField(validators=[MinValueValidator(0) ,MaxValueValidator(100)])

    def __str__(self):
        return f"{self.code} {self.value}"


class Address(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    username = models.CharField(max_length=150, null=False)
    id_username = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=254, null=False)
    address = models.CharField(max_length=300, null=False)
    phone_number = models.IntegerField(validators=[MinValueValidator(1000000) ,MaxValueValidator(999999999999999)], null=False)
    country = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=False)
    zip = models.CharField(max_length=9, null=False)
    preparing = models.BooleanField(null=True)
    on_the_way = models.BooleanField(null=True)
    delivered = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.username} {self.id}"
    

class Transaction(models.Model):
    id_transaction = models.AutoField(primary_key=True, null=False)
    id_username = models.ForeignKey(Address, on_delete=models.CASCADE, null=False)
    method = models.CharField(max_length=200, null=False)
    status = models.CharField(max_length=20, null=False)
    total = models.FloatField(null=False)
    currency = models.CharField(max_length=100, null=False, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.id_transaction}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('preparing', 'Preparing'),
            ('on_the_way', 'On the Way'),
            ('delivered', 'Delivered'),
            ('canceled', 'Canceled'),
        ],
        default='pending',
    )
    total = models.FloatField(validators=[MinValueValidator(0.00)])

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.FloatField(validators=[MinValueValidator(0.00)])
    discount_price = models.FloatField(validators=[MinValueValidator(0.00)], null=True, blank=True)

    def __str__(self):
        return f"Order items {self.order.id}"
