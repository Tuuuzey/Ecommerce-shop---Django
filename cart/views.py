from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import Products
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def cart_summary(request):
    cart = Cart(request)
    prods = cart.get_items()
    qty = cart.get_quants() 
    total = cart.cart_total()
    return render(request, 'cart/cart_summary.html', {'prods': prods, 'quantities': qty, 'total': total})

def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        prod_id = int(request.POST.get('prod_id'))
        prod_qty = int(request.POST.get('prod_qty'))
        prod = get_object_or_404(Products, id=prod_id)
        cart.add(product=prod, quantity=prod_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': cart_qty})
        messages.success(request, 'Product added to cart')
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'POST':
        prod_id = int(request.POST.get('prod_id'))
        cart.delete(product=prod_id)
        return JsonResponse({'prod': prod_id, 'message': 'Product removed from cart'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        prod_id = int(request.POST.get('item_id'))
        prod_qty = int(request.POST.get('item_qty'))
        cart.update(prod=prod_id, quantity=prod_qty)
        response = JsonResponse({'prod': prod_id, 'qty': prod_qty})
        return response
    return JsonResponse({'error': 'Invalid request'}, status=400)