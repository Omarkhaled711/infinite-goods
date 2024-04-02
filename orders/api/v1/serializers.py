from rest_framework import serializers
from orders.models import Order, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        # Include only necessary fields
        fields = ('payment_method', 'paid_amount')


class OrderSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.email
