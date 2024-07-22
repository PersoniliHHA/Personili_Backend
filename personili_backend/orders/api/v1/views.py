# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Models 
from orders.models import Order, OrderItem, Cart, CartItem
from accounts.models import AccountProfile, Account, DeliveryAddress


class CartViewSet(viewsets.ViewSet):
    """
    ViewSet class for the product app
    """
    queryset = Cart.objects.all()

    def get_account_profile(self, profile_id: str) -> AccountProfile:
        account_profile = get_object_or_404(AccountProfile, id=profile_id)
        return account_profile
    
    #################################### GET APIS, PUBLIC #####################################
    ##### GET current open cart of the user and all its order items #####
    @action(detail=False, methods=['GET'], url_path='current')
    def get_current_cart(self, request):
        """
        Get the current cart of the user
        """
        account_profile = self.get_account_profile(request.user.id)
        cart = Cart.objects.get(account_profile=account_profile, is_active=True)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    
    ###### ADD product variant to the cart ####################
    @action(detail=False, methods=['PUT'], url_path='current')
    def update_cart(self, cart: Cart, product_id: str, quantity: int) -> Cart:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        return cart
    
    ###### DELETE product variant from the cart ####################
    @action(detail=False, methods=['DELETE'], url_path='current')
    def delete_cart_item(self, cart: Cart, product_id: str) -> Cart:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
        return cart

    ###### Update the quantity of a product variant in the cart ####################
    @action(detail=False, methods=['PUT'], url_path='current')
    def update_cart_item_quantity(self, cart: Cart, product_id: str, quantity: int) -> Cart:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        return cart