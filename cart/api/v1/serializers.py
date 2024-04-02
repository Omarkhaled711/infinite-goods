from rest_framework import serializers
from cart.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    variations = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        # Exclude 'cart' field from the response
        exclude = ('cart', )

    def get_product(self, obj):
        return obj.product.product_name

    def get_user(self, obj):
        return obj.user.email

    def get_variations(self, obj):
        variation_details = {}
        for variation in obj.variations.all():
            if variation.variation_category not in variation_details:
                variation_details[variation.variation_category] = []
            variation_details[variation.variation_category].append(
                variation.variation_value)
        return variation_details
