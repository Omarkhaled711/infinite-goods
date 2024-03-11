from django.db.models import Q
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from . models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import get_cart_id

# Create your views here.


def shop(request, category_slug=None):
    """
    The shop page view
    """
    categories = None
    products = None
    products_page_num = 6

    if category_slug != None:
        categories = get_object_or_404(
            Category, category_urlSlug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True).order_by('id')
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    product_count = products.count()
    paginator = Paginator(products, products_page_num)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    context = {
        'products': products_page,
        'product_count': product_count,
    }
    return render(request, 'shop/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        category = get_object_or_404(Category, category_urlSlug=category_slug)
        single_product = Product.objects.get(
            category=category, slug=product_slug)
        inside_cart = CartItem.objects.filter(cart__cart_id=get_cart_id(request),
                                              product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'inside_cart': inside_cart
    }
    return render(request, 'shop/product_detail.html', context)


def search(request):
    """
    Adding a search functionality to our store
    """
    products = None
    product_count = 0
    keyword = request.GET.get('keyword', None)
    if keyword:
        products = Product.objects.filter(
            Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('id')
        product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'shop/store.html', context)
