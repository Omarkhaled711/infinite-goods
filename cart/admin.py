"""
Register the cart app models to the admin page
"""
from django.contrib import admin
from cart.models import Cart, CartItem
# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
