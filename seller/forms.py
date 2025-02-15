from django import forms
from shop.models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'discount_price', 'category', 'description', 'image']
