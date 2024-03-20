"""
A module for cart application
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from cart.models import Cart, CartItem, Coupon, UserCoupon
from shop.models import Product, Variation
from django.contrib.auth.decorators import login_required
from django.db.models import F
# Create your views here.


def get_cart_id(req):
    """
    make the session key as the cart id
    """
    cart_id = req.session.session_key
    if not cart_id:
        cart_id = req.session.create()
    return cart_id


def get_cart(req):
    """
    get cart object, so that we can add items to it later
    """
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(req))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=get_cart_id(req))
    cart.save()
    return cart


def add_product_variations(req, product, product_variation):
    """
    Add the variations associated with each product
    """
    for item in req.POST:
        value = req.POST[item]
        try:
            variation = Variation.objects.get(product=product,
                                              variation_category__iexact=item,
                                              variation_value__iexact=value)
            product_variation.append(variation)
        except Exception:
            pass
    # Sort the variations based on some criterion, e.g., variation_value
    product_variation.sort(key=lambda x: x.variation_value)


def get_previous_products(cart_item,
                          previous_products_variations, previous_products_ids):
    """
    A function that returns the gets all existing variatoins for a product
    and appends them to a list
    """
    for item in cart_item:
        variations = list(item.variations.all())
        # Sort the variations based on some criterion, e.g., variation_value
        variations.sort(key=lambda x: x.variation_value)
        previous_products_variations.append(variations)
        previous_products_ids.append(item.id)


def add_cart_item(req, product_id):
    """
    add a cart item to the cart
    """
    current_user = req.user
    cart = get_cart(req)
    product = Product.objects.get(id=product_id)

    product_variation = []
    previous_products_variations = []
    previous_products_ids = []
    if req.method == "POST":
        add_product_variations(req, product, product_variation)

    if current_user.is_authenticated:
        found_in_cart = CartItem.objects.filter(
            product=product, user=current_user).exists()
        if found_in_cart:
            cart_items = CartItem.objects.filter(
                product=product, user=current_user)
            get_previous_products(cart_items,
                                  previous_products_variations, previous_products_ids)
    else:
        found_in_cart = CartItem.objects.filter(
            product=product, cart=cart).exists()
        if found_in_cart:
            cart_items = CartItem.objects.filter(product=product, cart=cart)
            get_previous_products(cart_items,
                                  previous_products_variations, previous_products_ids)

    if found_in_cart and product_variation in previous_products_variations:
        index = previous_products_variations.index(product_variation)
        item_id = previous_products_ids[index]
        cart_item = CartItem.objects.get(product=product, id=item_id)
        cart_item.quantity += 1
    else:
        if current_user.is_authenticated:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                quantity=1
            )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )
        previous_products_variations.append(list(cart_item.variations.all()))

    if len(product_variation) > 0:
        cart_item.variations.clear()
        for item in product_variation:
            cart_item.variations.add(item)
    cart_item.save()
    return redirect('cart')


def decrement_cart_item(req, product_id, cart_item_id):
    """
    decrement a cart item from the cart
    """
    product = get_object_or_404(Product, id=product_id)
    try:
        if req.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=req.user, id=cart_item_id)
        else:
            cart = get_cart(req)
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def remove_cart_item(req, product_id, cart_item_id):
    """
    remove a cart item from the cart
    """
    product = get_object_or_404(Product, id=product_id)
    try:
        if req.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=req.user, id=cart_item_id)
        else:
            cart = get_cart(req)
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


@login_required(login_url='login')
def apply_coupon(req, coupon_code, coupons):
    """
    Apply coupon logic and associate it with the logged-in user.
    """
    try:
        applied_coupon = coupons.get(code=coupon_code)
        if applied_coupon.is_valid():
            user = req.user
            if not UserCoupon.objects.filter(user=user, coupon=applied_coupon).exists():
                UserCoupon.objects.create(user=user, coupon=applied_coupon)
                applied_coupon.current_usages += 1
                applied_coupon.save()
                return True
    except Coupon.DoesNotExist:
        pass
    return False


def get_user_first_valid_coupon(user):
    """
    Get the first valid coupon associated with the given user.
    """
    try:
        now = timezone.now().date()
        user_first_valid_coupon = Coupon.objects.filter(
            usercoupon__user=user, expiration_date__gte=now, current_usages__lt=F('max_usages')).first()
        return user_first_valid_coupon
    except Exception:
        return None


def cart(req, total_price=0, quantity=0, cart_items=None):
    """
    Main cart page
    """
    try:
        if req.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=req.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=get_cart_id(req))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total_price += (item.quantity * item.product.price)
            quantity += item.quantity
    except Cart.DoesNotExist:
        pass

    # apply tax
    tax = round(total_price * (2 / 100), 2)
    # apply coupons
    coupons = Coupon.objects.filter(expiration_date__gte=timezone.now().date())
    applied_coupon_code = None
    if req.method == 'POST':
        coupon_code = req.POST.get('coupon_code', None)
        if req.user.is_authenticated:
            if coupon_code and apply_coupon(req, coupon_code, coupons):
                return redirect('cart')

    if req.user.is_authenticated:
        applied_coupon_code = get_user_first_valid_coupon(req.user)
    discount = 0
    if applied_coupon_code:
        applied_coupon = coupons.get(code=applied_coupon_code)
        discount = round(
            total_price * (applied_coupon.discount_percentage / 100), 2)

    # Total money
    all_total = round(total_price + tax - float(discount), 2)
    # gather the context data and pass it to the template
    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'discount': discount,
        'all_total': all_total,
        'applied_coupon': applied_coupon_code
    }
    return render(req, 'shop/cart.html', context)


@login_required(login_url="login")
def checkout(req, total_price=0, quantity=0, cart_items=None):
    """
    Adding checkout functionality to our store
    """
    try:
        cart_items = CartItem.objects.filter(user=req.user, is_active=True)
        for item in cart_items:
            total_price += (item.quantity * item.product.price)
            quantity += item.quantity
    except Exception:
        pass

    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(req, 'shop/checkout.html', context)
