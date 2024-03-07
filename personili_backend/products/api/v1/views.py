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
    
    @action(detail=False, methods=['GET'], url_path='v1/products', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_products_light(self, request):
        """
        This method is used to get the list of products with minimal information and based on criterias :
        - category_id
        - personalization_method_id
        - theme_id
        - design_id
        - organization_id
        - sponsored_organization_ids
        - search term 
        """
        # Get the query parameters
        offset = request.query_params.get('offset', 0)
        limit = request.query_params.get('limit', 10)
        category_id = request.query_params.get('category_id', None)
        personalization_method_id = request.query_params.get('personalization_method_id', None)
        theme_id = request.query_params.get('theme_id', None)
        design_id = request.query_params.get('design_id', None)
        organization_id = request.query_params.get('organization_id', None)
        sponsored_organization_ids = request.query_params.get('sponsored_organization_ids', None)

        # Get the products based on the query parameters
        products = Product.get_products_light(category_id, 
                                              personalization_method_id, 
                                              theme_id, 
                                              design_id, 
                                              organization_id, 
                                              sponsored_organization_ids)

        # Return the response
        response = Response(products, status=status.HTTP_200_OK)
