from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from seller.models import SellerUser 
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user_has_errors = False
        
        if User.objects.filter(username=username).exists():
            user_has_errors = True
            messages.error(request, 'User with this username already exists')
        if User.objects.filter(email=email).exists():
            user_has_errors = True
            messages.error(request, 'User with this email already exists')
        if password1 != password2:
            user_has_errors = True
            messages.error(request, 'Passwords must match')
        if len(password1) < 8:
            user_has_errors = True
            messages.error(request, 'Password must be atleast 8 characters long')
        
        if user_has_errors:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(request, 'Account created, login now')
            return redirect('login')
    
    return render(request, 'user/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid password')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'user/login.html') 

def logout_view(request):
    logout(request)
    return redirect('login')

def tos_view(request):
    return render(request, 'user/tos.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        current_user = request.user
        has_error = False

        if User.objects.filter(username=username).exclude(pk=current_user.pk).exists():
            messages.error(request, "This username is already taken.")
            has_error = True

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email

        if password1 and password2:
            if password1 == password2:
                current_user.set_password(password1)
            else:
                has_error = True
                messages.error(request, "Passwords does not match.")

        if not has_error:
            current_user.username = username
            current_user.save()
            if password1 and password2:
                return redirect('login')
        else:
            messages.error(request, "Failed to save credentials.")

    is_seller = False
    try:
        seller_profile = SellerUser.objects.get(user=request.user)
        is_seller = True
    except SellerUser.DoesNotExist:
        is_seller = False

    return render(request, 'user/profile.html', {'is_seller': is_seller})

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'user/orders.html', {'orders':orders})


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if user with given email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No user with that email address found.")
            return render(request, 'user/forgot_password.html')
        # Generate the reset link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = request.build_absolute_uri(
            f'/reset/{uid}/{token}/' 
        )
        # Email subject and message
        subject = "e-Shop, reset your password"
        message = render_to_string(
            'user/password_reset_email.html',
            {
                'user': user,
                'reset_link': reset_link,
                'domain': get_current_site(request).domain, 
            }
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, f'An email with instructions to change your password has been sent to {email}')

    return render(request, 'user/forgot_password.html')

def api_home(request):
    return render(request, 'user/apiview.html')