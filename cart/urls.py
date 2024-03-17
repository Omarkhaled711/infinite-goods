'''
Module for cart urls
'''
from django.urls import path
from cart import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/',
         views.add_cart_item, name="add_cart_item"),
    path('dec_cart/<int:product_id>/<int:cart_item_id>',
         views.decrement_cart_item, name="decrement_cart_item"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>',
         views.remove_cart_item, name="remove_cart_item"),
    path('checkout/', views.checkout, name='checkout'),

]
