"""
A model for cart related functionalities
"""
from django.db import models
from shop.models import Product
from django.utils import timezone

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

    def item_total_price(self):
        """
        return product price * the quatity
        """
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


class Coupon(models.Model):
    """
    This model represents discount coupons
    """
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
    max_usages = models.PositiveIntegerField(default=1)

    current_usages = models.PositiveIntegerField(default=0)

    def is_valid(self):
        return self.expiration_date >= timezone.now().date() and self.current_usages < self.max_usages

    def __str__(self):
        return self.code