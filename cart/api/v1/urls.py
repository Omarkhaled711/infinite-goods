from django.urls import path
from .views import CartItemListAPIView

urlpatterns = [
    path('cart/items/', CartItemListAPIView.as_view(), name='cart-item-list'),
]
