from django.db import models
from shop.models import Products
from django.contrib.auth.models import User

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)

    def __str__(self):
        return f'{self.user.username} wishlist'
    
