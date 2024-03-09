"""
A model for cart related functionalities
"""
from django.db import models
from shop.models import Product

# Create your models here.


class Cart(models.Model):
    """
    Model for cart app, an ORM for our database
    """
    cart_id = models.CharField(max_length=256, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    """
    Model for items added in the cart
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product
