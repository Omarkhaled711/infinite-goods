import uuid
from django.http import HttpResponse
from django.shortcuts import redirect, render

from cart.models import CartItem, Coupon
from cart.views import get_user_first_valid_coupon
from orders.forms import OrderForm
from orders.models import Order

# Create your views here.


def is_cart_items(user):
    """
    if there's no cart items return false, else return true
    """
    cart_items = CartItem.objects.filter(user=user)
    if cart_items.count() > 0:
        return True
    return False


def calculate_paid(user, paid_amount, total_products=0, quantity=0):
    """
    calculate total_products, tax, disounct, and grand_total
    """
    cart_items = CartItem.objects.filter(user=user)
    grand_total = 0
    tax = 0
    for item in cart_items:
        total_products += (item.quantity * item.product.price)
        quantity += item.quantity
    tax = round(total_products * (2 / 100), 2)
    applied_coupon_code = get_user_first_valid_coupon(user)
    discount = 0
    if applied_coupon_code:
        applied_coupon = Coupon.objects.get(code=applied_coupon_code)
        discount = round(
            total_products * (applied_coupon.discount_percentage / 100), 2)
    grand_total = round(total_products + tax - float(discount), 2)
    paid_amount['total_products'] = total_products
    paid_amount['tax'] = tax
    paid_amount['discount'] = discount
    paid_amount['grand_total'] = grand_total


def save_form_info(req, form, data, current_user, paid_amount):
    """
    Saves the data we got from the form into the database
    """
    data.user = current_user
    for field_name, field_value in form.cleaned_data.items():
        setattr(data, field_name, field_value)
    data.total = paid_amount['grand_total']
    data.tax = paid_amount['tax']
    data.discount = paid_amount['discount']
    data.ip = req.META.get('REMOTE_ADDR')
    data.save()
    unique_val = str(uuid.uuid4())
    data.order_id = unique_val + str(data.id)
    data.save()


def place_order(req):
    """
    This view handles placing order functionality
    """
    current_user = req.user
    if (not is_cart_items(current_user)):
        return redirect('shop')

    # get cart_items
    cart_items = CartItem.objects.filter(user=current_user)
    # we will append total_products, tax, discount and grand_total to this array
    paid_amount = {}
    calculate_paid(current_user, paid_amount)

    if req.method == "POST":
        form = OrderForm(req.POST)
        if form.is_valid():
            data = Order()
            save_form_info(req, form, data, current_user, paid_amount)
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_id=data.order_id)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total_products': paid_amount['total_products'],
            }
        return render(req, 'orders/payments.html', context)
    return redirect('checkout')


def payments(req):
    """
    payments view
    """
    return render(req, 'orders/payments.html')
