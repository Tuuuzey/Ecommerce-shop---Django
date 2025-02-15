from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Products
from django.contrib import messages
from .models import SellerUser
from django.contrib.auth.decorators import login_required
from shop.models import Products, ProductImage
import stripe
from django.core.exceptions import ValidationError
from .forms import ProductForm

# Create your views here.

@login_required
def newseller_view(request):
    if SellerUser.objects.filter(user=request.user).exists():
        return redirect('seller:addproducts') 
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        new_seller = SellerUser.objects.create(
            user=request.user, 
            phone_number=phone_number,
        )

        return redirect('seller:addproducts')

    return render(request, 'seller/newseller.html')


@login_required
def not_seller_view(request):
    return render(request, 'seller/not_seller_error.html')

def create_stripe_product_and_price(user, name, price, description, image_url, category):
    try:
        stripe_product = stripe.Product.create(
            name=name,
            description=description,
            images=[image_url],
            metadata={'category': category}
        )
        stripe_price = stripe.Price.create(
            unit_amount=int(price * 100), 
            currency="usd",
            product=stripe_product.id
        )
        seller_profile = SellerUser.objects.get(user=user)
        product = Products.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image_url,
            stripe_price_id=stripe_price.id,
            seller=seller_profile
        )

        return product

    except stripe.error.StripeError as e:
        raise ValidationError(f"Stripe Error: {e}")


@login_required
def add_products_view(request):
    try:
        is_seller = SellerUser.objects.get(user=request.user)
        if not is_seller:
            return redirect('seller:notseller')

        if request.method == 'POST':
            name = request.POST.get('name')
            price = float(request.POST.get('price'))
            description = request.POST.get('description')
            main_image_url = request.POST.get('image')
            category = request.POST.get('category')
            additional_images = request.POST.getlist('additional_images') 
            
            if not name or not price or not description or not main_image_url or not category:
                raise ValidationError("All the fields must be completed!")

            product = create_stripe_product_and_price(request.user, name, price, description, main_image_url, category)
            for image_url in additional_images:
                if image_url.strip():
                    ProductImage.objects.create(product=product, image_url=image_url)
            
            messages.success(request, 'Product has been added')
            return redirect('seller:addproducts')

        return render(request, 'seller/addproducts.html')

    except SellerUser.DoesNotExist:
        return redirect('seller:notseller')

    except ValidationError as e:
        return render(request, 'seller/addproducts.html', {'error': str(e)})
    
def sellers_prods(request):
    try:
        is_seller = SellerUser.objects.get(user=request.user)
        if not is_seller:
            return redirect('seller:notseller')
        products = Products.objects.filter(seller_id=request.user.id)
        return render(request, 'seller/sellersprods.html', {'products': products})


    except SellerUser.DoesNotExist:
        return redirect('seller:notseller')
    
    except ValidationError as e:
        return render(request, 'seller/addproducts.html', {'error': str(e)})
    

def edit_product(request, product_id):
    try:
        seller_user = SellerUser.objects.get(user=request.user)
        product = get_object_or_404(Products, id=product_id, seller=seller_user)
        
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product = form.save()
                additional_images = request.POST.getlist('additional_images')
                product.images.all().delete()
                for image_url in additional_images:
                    if image_url.strip():
                        ProductImage.objects.create(product=product, image_url=image_url.strip())
                
                return redirect('seller:sellers_prods')

        else:
            form = ProductForm(instance=product)
        
        return render(request, 'seller/edit_product.html', {'form': form, 'product': product})

    except SellerUser.DoesNotExist:
        return redirect('seller:notseller')
