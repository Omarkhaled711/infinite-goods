"""
Register the cart app models to the admin page
"""
from django.contrib import admin
from cart.models import Cart, CartItem, Coupon, UserCoupon
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    """
    specify how to display data on Cart admin site
    """
    list_display = ('cart_id', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
    """
    specify how to display data on CartItem admin page
    """
    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Coupon)
admin.site.register(UserCoupon)
