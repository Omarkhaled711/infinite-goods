"""
This module handles the orders models
"""
from django.db import models
from shop.models import Product, Variation
from users.models import User

# Create your models here.


class Payment(models.Model):
    """
    A payment class to represent the payment table in database
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=128)
    payment_method = models.CharField(max_length=128)
    paid_amount = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        string representation for the payement model
        """
        return self.payment_id


class Order(models.Model):
    """
    An order class to represent the order table in database
    """
    status_choices = (
        ('New', 'New'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
        ('Accepted', 'Accepted')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.CharField(max_length=128)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=32)
    address_1 = models.CharField(max_length=64)
    address_2 = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    order_note = models.CharField(max_length=128, blank=True)
    is_ordered = models.BooleanField(default=False)
    tax = models.FloatField()
    discount = models.FloatField(default=0)
    total = models.FloatField()
    status = models.CharField(
        max_length=32, choices=status_choices, default='New')
    ip = models.CharField(blank=True, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        """
        return full name from first and last names
        """
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        """
        return full address
        """
        return f'{self.address_1} {self.address_2}'

    def __str__(self):
        """
        a string representation for order model
        """
        return f'{self.email}:{self.order_id}'


class OrderProduct(models.Model):
    """
    An order product class to represent the products associated
    with orders in a table in database
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color = models.CharField(max_length=64)
    size = models.CharField(max_length=64)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        """
        string representation for order products model
        """
        return f"{self.order.order_id}: {self.product.product_name}"
