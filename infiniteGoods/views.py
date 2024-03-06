'''
views model for main application
'''
from django.shortcuts import render
from shop.models import Product


def home(req):
    '''
    The home page (root) of our website
    '''
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(req, 'index.html', context)
