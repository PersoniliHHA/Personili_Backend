# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Local imports
from products.models import Product, ProductDesignedPersonalizableVariant, ProductReview, Promotion
from accounts.models import AccountProfile

# Utils
from utils.validators import is_all_valid_uuid4


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
        - personalization_type_id
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
        category_ids = request.query_params.get('categories', None)
        personalization_method_ids = request.query_params.get('personalization_methods', None)
        theme_ids = request.query_params.get('themes', None)
        design_ids = request.query_params.get('designs', None)
        organization_ids = request.query_params.get('organizations', None)
        sponsored_organizations = request.query_params.get('sponsored_organizations', None)
        search_term = request.query_params.get('search_term', None)
        min_price = request.query_params.get('min_p', None)
        max_price = request.query_params.get('max_p', None)

        ####################### Query parameters validation ########################
        ##### offset and limit should be integers and greater than 0
        if (not offset or not limit) or (not offset and not limit):
            offset = 0
            limit = 20
        if offset and limit:
            if not (offset.isdigit() and limit.isdigit()) or (int(offset) < 0 or int(limit) < 0) or (int(offset) > int(limit)):
                return Response({"error": "BAD_REQUEST"}, status=400)
        ##### price min and price max should be integers and greater than 0
        if min_price and max_price:
            if not (min_price.isdigit() and max_price.isdigit()) or (int(min_price) < 0 or int(max_price) < 0) or (int(min_price) > int(max_price)):
                return Response({"error": "BAD_REQUEST"}, status=400)
        else :
            min_price = 0
            max_price = 1000000
        
        ##### category_ids, personalization_method_ids, theme_ids, design_id, organization_ids, sponsored_organization_ids should be valid uuid format
        if category_ids:
            category_ids = category_ids.split(",")
            if not is_all_valid_uuid4(category_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if personalization_method_ids:
            personalization_method_ids = personalization_method_ids.split(",")
            if not is_all_valid_uuid4(personalization_method_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if theme_ids:
            theme_ids = theme_ids.split(",")
            if not is_all_valid_uuid4(theme_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if design_ids:
            design_ids = design_ids.split(",")
            if not is_all_valid_uuid4(design_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if organization_ids:
            organizations_ids = organization_ids.split(",")
            if not is_all_valid_uuid4(organizations_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if sponsored_organizations:
            # sponsored_organizations should ba valid boolean value
            if sponsored_organizations not in ["true", "false", "True", "False"]:
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if search_term:
            # search term has to be a string and not longer than 100 characters
            if not isinstance(search_term, str) or len(search_term) > 100:
                return Response({"error": "BAD_REQUEST"}, status=400)
        ###########################################################################

        try :
            # Get the products based on the query parameters
            products = Product.get_products_light(offset=offset,
                                                limit=limit,
                                                max_price=max_price,
                                                min_price=min_price,
                                                category_ids=category_ids, 
                                                organization_ids=organization_ids, 
                                                personalization_method_ids=personalization_method_ids, 
                                                design_ids=design_ids, 
                                                theme_ids=theme_ids, 
                                                sponsored_organizations=sponsored_organizations,
                                                search_term=search_term)

            # Return the response
            response = Response(products, status=status.HTTP_200_OK)
            return response
        except Exception as e:
            logging.error(f"get_products_light action method error :{e.args} ")
            return Response({"error": "UNKNOWN_INTERNAL_ERROR"}, status=400)
