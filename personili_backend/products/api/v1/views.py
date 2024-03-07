# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Local imports
from products.models import Product, ProductDesignedPersonalizableVariant, ProductReview, Promotion
from accounts.models import AccountProfile


# configure logging 
import logging
logging.basicConfig(level=logging.DEBUG)


class ProductViewSet(viewsets.ViewSet):
    """
    ViewSet class for the product app
    """
    queryset = Product.objects.all()
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_user_profile(self):
        user_profile = get_object_or_404(AccountProfile, user=self.request.user)
        return user_profile
