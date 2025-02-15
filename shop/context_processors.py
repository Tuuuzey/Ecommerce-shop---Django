from .models import Products

def categories_processor(request):
    return {'categories': dict(Products.CATEGORY_CHOICES)}
