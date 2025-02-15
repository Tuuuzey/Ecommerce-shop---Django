from django.shortcuts import render, redirect
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from .models import Address, PromoCode, Transaction, Order, OrderItem
from django.contrib import messages
from django.http import Http404
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

@login_required
def checkout_view(request):
    cart = Cart(request)
    prods = cart.get_items()
    qty = cart.get_quants() 
    total = cart.cart_total()
    new_total = total

    if request.method == 'POST':
        # REDEEM CODE FORM        
        if 'redeem_code' in request.POST:
            promo_code = request.POST.get('promo_code')
            try:
                db_code = PromoCode.objects.get(code=promo_code)
                value = 1 - (db_code.value / 100)
                new_total *= value
                new_total = round(new_total, 2)
                messages.success(request, f"Code: {db_code.code}, -{db_code.value}%")
                request.session['promo_code'] = promo_code
                request.session['new_total'] = new_total

            except PromoCode.DoesNotExist:
                messages.error(request, "This code does not exist")

        # ADDRESS FORM 
        elif 'address' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')    
            phone_number = request.POST.get('phone_number')    
            address = request.POST.get('address_input')    
            country = request.POST.get('country')    
            state = request.POST.get('state')    
            city = request.POST.get('city')    
            zip = request.POST.get('zip')

            cur_user = request.user
            new_address = Address(
                first_name=first_name,
                last_name=last_name,
                id_username=cur_user,
                username=cur_user.username,
                email=email,
                phone_number=phone_number,
                address=address,
                country=country,
                state=state,
                city=city,
                zip=zip,
            )
            new_address.save()

            request.session['new_address_id'] = new_address.id
            request.session['payment'] = request.POST.get('paymentMethod')
            request.session['total'] = total
            
            return redirect('checkout:checkoutpayment')

    return render(request, 'checkout/checkout.html', {'prods': prods, 'qty':qty, 'total':total, 'new_total': new_total})

@login_required
def checkout_payment_view(request):
    new_address_id = request.session.get('new_address_id')
    payment = request.session.get('payment')
    new_total = request.session.get('new_total')
    total = request.session.get('total')
    promo_code = request.session.get('promo_code')

    price = total
    request.session['total_val'] = price
    if new_total and new_total != total:
        request.session['total_val'] = new_total

    if not new_address_id:
        raise Http404("Address ID not provided.")

    new_address = Address.objects.get(id=new_address_id)
    cart = Cart(request)
    prods = cart.get_items()
    qty = cart.get_quants() 

    context = {
        'prods': prods, 
        'qty': qty,
        'new_address': new_address,
        'payment': payment,
        'new_total': new_total,
        'promo_code': promo_code,
        'total': total,
    }

    # STRIPE PAYMENT
    if request.method == 'POST':
        if promo_code:
            db_code = PromoCode.objects.filter(code=promo_code).first()
            discount_factor = 1 - (db_code.value / 100) if db_code else 1
        else:
            discount_factor = 1

        line_items = []
        for product in prods:
            quantity = qty.get(str(product.id), 0)
            price = product.discount_price if product.discount_price is not None else product.price

            if quantity > 0:
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.name,
                            'description': product.description[:200],
                        },
                        'unit_amount': int(price * 100 * discount_factor),
                    },
                    'quantity': quantity,
                })

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            payment_method_types=['card'],
            mode='payment',
            success_url=f'{settings.BASE_URL}checkout/success_checkout/?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{settings.BASE_URL}checkout/failed_checkout?error=payment_failed',
            customer_email=request.user.email if request.user.is_authenticated else None,
            custom_text={'submit': {
                'message': 'DO NOT USE YOUR REAL CARD CREDENTIALS. Use card number: 4242 4242 4242 4242, expiration date 12/30, cvv/cvc 123.'
            }}
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'checkout/checkout_payment.html', context)




@login_required
def success_checkout_view(request):
    session_id = request.GET.get('session_id')
    total = request.session.get('total_val')
    promo_code = request.session.get('promo_code')
    
    if not session_id:
        return redirect('index')
    
    session = stripe.checkout.Session.retrieve(session_id)
    
    if session.payment_status == "paid":
        try:
            # TRANSACTION TABLE
            usert = Address.objects.filter(id_username=request.user).first()
            new_transaction = Transaction(
                id_username=usert,
                method='Stripe',
                status='paid',
                total=total,
                currency='USD',
            )
            new_transaction.save()

            # ORDER TABLE
            address = usert
            transaction = new_transaction
            promo_code_obj = PromoCode.objects.filter(code=promo_code).first()

            new_order = Order(
                user=request.user,
                address=address,
                transaction=transaction,
                promo_code=promo_code_obj,
                status='pending',
                total=total
            )
            new_order.save()

            # ORDER ITEM TABLE
            cart = Cart(request)
            prods = cart.get_items()
            qty = cart.get_quants()

            for product in prods:
                quantity = qty.get(str(product.id), 0)
                price = product.price
                if product.discount_price is not None:
                    price = product.discount_price

                value = 1
                if promo_code_obj:
                    value = 1 - (promo_code_obj.value / 100)

                if quantity > 0:
                    new_order_item = OrderItem(
                        order=new_order,
                        product=product,
                        quantity=quantity,
                        price=price * value,
                        discount_price=product.discount_price if product.discount_price else None,
                    )
                    new_order_item.save()
        
        except Exception as e:
            print(f"Error during checkout: {e}")
            return redirect('index')
        # Clear all items from the cart
        cart.cart.clear() 
        # Clear session data related to checkout
        request.session.pop('total_val', None)
        request.session.pop('promo_code', None)
        request.session.pop('new_total', None)
        request.session.pop('new_address_id', None)
        request.session.pop('payment', None)

    return render(request, 'checkout/success_checkout.html')


@login_required
def failed_checkout_view(request):
    session_id = request.GET.get('session_id')
    total = request.session.get('total_val')
    
    if not session_id:
        return redirect('index')
    
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status != "paid":
        # TRANSACTION TABLE
        usert = Address.objects.filter(id_username=request.user).first()
        new_transaction = Transaction(
            id_username=usert,
            method='Stripe',
            status='failed',
            total=total,
            currency='USD',
        )
        new_transaction.save()
    return render(request, 'checkout/failed_checkout.html')


