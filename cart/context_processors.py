"""
This module include some utility functions for the cart app
"""
from cart.models import Cart, CartItem
from cart.views import get_cart_id


def counter(req):
    """
    This function counts the items inside the cart
    """
    cart_count = 0
    if 'admin' in req.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=get_cart_id(req))[:1]
            cart_items = CartItem.objects.all().filter(cart=cart)
            for item in cart_items:
                cart_count += item.quantity
        except Exception:
            cart_count = 0
    return dict(cart_count=cart_count)
