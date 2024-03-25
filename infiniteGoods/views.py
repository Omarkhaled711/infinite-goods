'''
views model for main application
'''
from django.shortcuts import render
from shop.models import Product, ReviewRating


def home(req):
    '''
    The home page (root) of our website
    '''
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    for product in products:

        reviews = ReviewRating.objects.filter(
            product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(req, 'index.html', context)
