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
    ##### GET
    @action(detail=False, methods=['GET'], url_path='current')
    def get_current_cart(self, request):
        """
        Get the current cart of the user
        """
        account_profile = self.get_account_profile(request.user.id)
        cart = Cart.objects.get(account_profile=account_profile, is_active=True)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)