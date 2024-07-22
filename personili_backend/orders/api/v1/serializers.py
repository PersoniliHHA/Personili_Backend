# Models
from orders.models import Order, OrderItem, Cart, CartItem

# Django imports


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'account_profile', 'is_active', 'created_at', 'updated_at']


class DeleteCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created_at', 'updated_at']