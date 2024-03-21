from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import json
import uuid
from django.shortcuts import redirect, render

from cart.models import CartItem, Coupon, UserCoupon
from cart.views import get_user_first_valid_coupon
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment
from shop.models import Product

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


def get_payment_info(req, body, order):
    """
    stroe payment object attributes values
    """
    return Payment(
        user=req.user,
        payment_id=body['transicID'],
        payment_method=body['payment_method'],
        paid_amount=order.total,
        status=body['status'],
    )


def payments(req):
    """
    payments view
    """
    body = json.loads(req.body)
    order = Order.objects.get(
        user=req.user, is_ordered=False, order_id=body['orderID'])
    payment = get_payment_info(req, body, order)
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    move_to_order_products(req, order, payment)
    remove_applied_coupon(req)
    clear_cart(req)
    send_order_received_mail(req, order)
    data = {
        'order_number': order.order_id,
        'payment_id': payment.payment_id,
    }
    return JsonResponse(data)


def remove_applied_coupon(req):
    """
    If the user did use a coupon, then we will remove it
    after the purchase
    """
    applied_coupon_code = get_user_first_valid_coupon(req.user)
    if (applied_coupon_code):
        applied_coupon = Coupon.objects.get(code=applied_coupon_code)
        user_coupon = UserCoupon.objects.get(
            user=req.user, coupon=applied_coupon)
        user_coupon.delete()


def move_to_order_products(req, order, payment):
    """
    Move the cart items to order product table
    """
    cart_items = CartItem.objects.filter(user=req.user)

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = req.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()
        product_variations = item.variations.all()
        order_product.variations.set(product_variations)
        order_product.save()
        remove_quantity_sold(item)


def remove_quantity_sold(item):
    """
    remove quantity of sold products
    """
    product = Product.objects.get(id=item.product_id)
    product.stock -= item.quantity
    product.save()


def clear_cart(req):
    """
    Clear the cart after payment is completed
    """
    CartItem.objects.filter(user=req.user).delete()


def send_order_received_mail(req, order):
    """
    Send a mail to the user that the request has been received
    """
    mail_subject = "Order Received Successfully!"
    render_str = 'orders/order_received_mail.html'
    message = render_to_string(render_str, {
        'user': req.user,
        'order': order,
    })
    to_email = req.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


def order_completed(req):
    """
    An order completed view
    """
    order_number = req.GET.get('order_number')
    payment_id = req.GET.get('payment_id')

    try:
        order = Order.objects.get(order_id=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=payment_id)

        total_products = 0
        for item in ordered_products:
            total_products += (item.quantity * item.product.price)

        context = {
            "order": order,
            "ordered_products": ordered_products,
            "order_number": order_number,
            "payment": payment,
            "payment_id": payment.payment_id,
            "total_products": total_products,
        }
        return render(req, 'orders/order_completed.html', context)
    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')
