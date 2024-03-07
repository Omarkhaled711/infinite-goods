from django.shortcuts import render, get_object_or_404
from . models import Product
from category.models import Category

# Create your views here.

def shop(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, category_urlSlug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        category = get_object_or_404(Category, slug=category_slug)
        single_product = Product.objects.get(category=category, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
    }
    return render(request, 'product_detail', context)
