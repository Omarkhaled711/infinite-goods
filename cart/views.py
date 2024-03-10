"""
A module for cart application
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from cart.models import Cart, CartItem, Coupon
from shop.models import Product

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


def add_cart_item(req, product_id):
    """
    add a cart item to the cart
    """
    cart = get_cart(req)
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
    cart_item.save()
    return redirect('cart')


def decrement_cart_item(req, product_id):
    """
    decrement a cart item from the cart
    """
    cart = get_cart(req)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def remove_cart_item(req, product_id):
    """
    remove a cart item from the cart
    """
    cart = get_cart(req)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def apply_coupon(req, coupon_code, coupons):
    """
    Apply coupon logic and store discount in session.
    """
    try:
        applied_coupon = coupons.get(code=coupon_code)
        if applied_coupon.is_valid():
            req.session['applied_coupon'] = applied_coupon.code
            return True
    except Coupon.DoesNotExist:
        pass
    return False


def cart(req, total_price=0, quantity=0, cart_items=None):
    """
    Main cart page
    """
    try:
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
    if req.method == 'POST':
        coupon_code = req.POST.get('coupon_code', None)
        if coupon_code and apply_coupon(req, coupon_code, coupons):
            return redirect('cart')

    applied_coupon_code = req.session.get('applied_coupon', None)
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
