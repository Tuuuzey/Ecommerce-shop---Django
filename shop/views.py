from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Products, Comment
from django.core.paginator import Paginator
from checkout.models import OrderItem, Order
from decimal import Decimal
from django.db.models import Avg, Count

# Create your views here.

def index(request):
    products = Products.objects.all()
    # SORTING
    product_search = request.GET.get('searchbtn', '')
    if product_search:
        products = products.filter(name__icontains=product_search)
    category = request.GET.get('category', None)
    if category:
        products = products.filter(category=category)
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('orderitem__comment__rating')).order_by('avg_rating')
    elif sort_by == 'comments':
        products = products.annotate(comment_count=Count('orderitem__comment')).order_by('-comment_count')
    else:
        products = products.order_by('name')
    # PAGINATION
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    categories = dict(Products.CATEGORY_CHOICES)
    
    return render(request, 'shop/index.html', {
        'products': products,
        'product_search': product_search,
        'categories': categories,
        'current_sort': sort_by,
    })


def detail(request, id):
    product = Products.objects.get(id=id)
    comments = Comment.objects.filter(order_item__product=product)
    average_rating = product.get_average_rating()
    full_stars = int(average_rating)
    half_star = 1/2 if (average_rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    if empty_stars < 0:
        empty_stars = 0
    elif empty_stars > 5:
        empty_stars = 5

    total_stars = full_stars + half_star + empty_stars
    if total_stars > 5:
        full_stars = 5 - (half_star + empty_stars)
    
    context = {
        'product': product,
        'average_rating': average_rating,
        'full_stars': full_stars,
        'half_star': half_star,
        'empty_stars': empty_stars,
        'comments': comments,
    }

    return render(request, 'shop/detail.html', context)

# COMMENTS AND OPINIONS
def add_comment(request):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to leave a comment.", status=403)

    if request.method == "POST":
        content = request.POST.get("content")
        product_id = request.POST.get("product")
        rating = request.POST.get("rating")
        rating = 6 - int(rating)

        if content and product_id and rating:
            product = get_object_or_404(Products, id=product_id)
            order_item = OrderItem.objects.filter(product=product, order__user=request.user).first()

            if order_item:
                new_comment = Comment(
                    order_item=order_item,
                    user=request.user,
                    content=content,
                    rating=Decimal(rating),
                )
                new_comment.save()
                return redirect('orders')
            else:
                return HttpResponse("You must have ordered this product to comment.", status=403)
        else:
            return HttpResponse("Comment, Product selection, and Rating cannot be empty.", status=400)

    orders = Order.objects.filter(user=request.user, status='delivered')
    order_items = OrderItem.objects.filter(order__in=orders)

    return render(request, 'shop/add_comment.html', {'order_items': order_items, 'orders': orders})
