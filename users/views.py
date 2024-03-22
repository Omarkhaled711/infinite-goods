"""
This module handles user related views
"""
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserForm, UserProfileForm
from .models import User, UserProfile
from django.contrib import messages, auth
from orders.models import Order
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cart.views import get_cart_id, get_previous_products
from cart.models import Cart, CartItem

import requests


def register(request):
    """
    registering view
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_name = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            user_name=user_name,
                                            password=password)
            user.phone_number = phone_number
            user.save()
            # activation
            mail_subject = 'Please activate your account'
            render_str = 'users/account_verification_email.html'
            send_verification_email(
                request, user, email, mail_subject, render_str)
            return redirect('/users/login/?command=activation&email='+email)

    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def send_verification_email(request, user, email, subject, render_str):
    """
    sending a verification mail for the user to preform an action,
    like activating his email, or reseting his password
    """
    current_site = get_current_site(request)
    mail_subject = subject
    message = render_to_string(render_str, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


def load_task_items(request, user):
    """
    when a user adds task items to his cart before logging in,
    this cart items should still be there login, so we will check
    if there's a cart associated with the session key when logging in,
    if there's one, the items will be added to the user's cart
    """
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        found_in_cart = CartItem.objects.filter(cart=cart).exists()
        if found_in_cart:
            cart_item = CartItem.objects.filter(cart=cart)
            product_variations = []
            for item in cart_item:
                variations = list(item.variations.all())
                # Sort the variations based on some criterion, e.g., variation_value
                variations.sort(key=lambda x: x.variation_value)
                product_variations.append(variations)

            cart_item = CartItem.objects.filter(user=user)
            prev_products = []
            prev_prod_ids = []
            get_previous_products(cart_item, prev_products, prev_prod_ids)
            for prod in product_variations:
                if prod in prev_products:
                    index = prev_products.index(prod)
                    item_id = prev_prod_ids[index]
                    item = CartItem.objects.get(id=item_id)
                    item.quantity += 1
                    item.user = user
                    item.save()
                else:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
    except Exception:
        pass


def redirect_next_page(request, url):
    """
    when you login to access a specific page, you should
    be redirect to that exact page after loggin in, so that's
    what this function is taking care of
    """
    try:
        url_parsed = requests.utils.urlparse(url).query
        params = dict(param.split('=') for param in url_parsed.split('&'))
        if 'next' in params:
            return params['next']
    except Exception:
        pass
    return 'dashboard'


def login(request):
    """
    logging in view
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user:
            load_task_items(request, user)
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            next_page = redirect_next_page(request, url)
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid login cerdentials')
            return redirect('login')
    return render(request, 'users/login.html')


@login_required(login_url='login')
def logout(request):
    """
    logging out view
    """
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


def activate(request, uidb64, token):
    """
    activate account after the user presses on the verification link
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (OverflowError, TypeError, User.DoesNotExist, ValueError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Well done! Your account has been successfully activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    """
    dashboard view
    """
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    context = {
        'orders_count': orders_count,
    }
    return render(request, 'users/dashboard.html')


def forgotPass(request):
    """
    A view to handle forgetting password case
    """
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password

            mail_subject = 'Reset Your Password'
            render_str = 'users/reset_password.html'
            send_verification_email(
                request, user, email, mail_subject, render_str)

            messages.success(
                request, 'Password rest email has been sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exsist!')
            return redirect('forgotPass')
    return render(request, 'users/forgotPass.html')


def resetpassword_validate(request, uidb64, token):
    """
    The view that gets called when the user press on the link
    that was sent to him in the email (the forgetting pass link)
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.success(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    """
    Creating a new pass
    """
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'users/resetPassword.html')


def my_orders(request):
    """
    Renders a user's orders page.
    """
    orders = Order.objects.filter(user=request.user, is_orderd=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'users/order.html', context)


def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request, 'Your Profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'users/edit_profile.html', context)