"""
A module for cart application
"""
from django.shortcuts import render

# Create your views here.


def cart(req):
    return render(req, 'shop/cart.html')
