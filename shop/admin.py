from django.contrib import admin
from .models import Products, ProductImage, Comment
# Register your models here.

admin.site.register(Products)
admin.site.register(ProductImage)
admin.site.register(Comment)