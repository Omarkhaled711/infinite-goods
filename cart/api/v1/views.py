from rest_framework import generics
from cart.models import CartItem
from .serializers import CartItemSerializer
from rest_framework.permissions import IsAuthenticated


class CartItemListAPIView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)
