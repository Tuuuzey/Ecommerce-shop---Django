from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from shop.models import Products
from django.urls import reverse
from django.contrib import messages

# Create your views here.
@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})

@login_required
def add_wishlist_view(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, 'Product added to wishlist')
    return redirect(reverse('detail', kwargs={'id': product.id}))

@login_required
def remove_wishlist_view(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist:wishlist')


