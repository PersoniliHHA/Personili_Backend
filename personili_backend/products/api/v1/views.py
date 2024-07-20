# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Local imports
from products.models import Product, Promotion
from accounts.models import AccountProfile
from personalizables.models import Category

# Utils
from utils.validators import is_all_valid_uuid4
from datetime import datetime


# configure logging 
import logging
logging.basicConfig(level=logging.DEBUG)


class ProductViewSet(viewsets.ViewSet):
    """
    ViewSet class for the product app
    """
    queryset = Product.objects.all()

    def get_account_profile(self, profile_id: str) -> AccountProfile:
        account_profile = get_object_or_404(AccountProfile, id=profile_id)
        return account_profile
    
    #################################### GET APIS, PUBLIC #####################################
    ##### GET PRODUCTS LIGHT #####
    @action(detail=False, methods=['POST'], url_path='catalog', permission_classes=[permissions.AllowAny])
    def get_products(self, request):
        """
        This method is used to get the list of products with minimal information and based on criterias :
        - category_ids
        - department_ids
        - personalization_type_ids
        - personalization_method_ids
        - theme_ids
        - design_ids
        - organization_ids
        - sponsored_organization_ids
        - search term 
        - limit
        - offset
        - min_price
        - max_price
        - promotion type : discount, free shipping, etc
        """
        # specify the permission and authentication classes
        self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        self.authentication_classes = []

        # Get the query parameters
        offset = request.data.get('offset', None)
        limit = request.data.get('limit', None)
        
        category_ids = request.data.get('categories', None)
        department_ids = request.data.get('departments', None)
        organization_ids = request.data.get('organizations', None)
        workshop_ids = request.data.get('workshops', None)
        sponsored_organizations = request.data.get('sponsored_organizations', None)
        sponsored_products = request.data.get('sponsored_products', None)
        
        
        brands = request.data.get('brands', None)
        models = request.data.get('models', None)
        option_value_ids = request.data.get('option_values', None)
        
        personalization_method_ids = request.data.get('personalization_methods', None)
        
        theme_ids = request.data.get('themes', None)
        design_ids = request.data.get('designs', None)
        
        search_term = request.data.get('search_term', None)
        
        min_price = request.data.get('min_price', None)
        max_price = request.data.get('max_price', None)

        publication_date = request.data.get('publication_date', None)

        with_promotion = request.data.get('with_promotion', None)

        ####################### Query parameters validation ########################
        ##### offset and limit should be integers and greater than 0
        if offset and limit:
            if not (offset.isdigit() and limit.isdigit()):
                return Response({"error": "BAD_REQUEST"}, status=400)
            else:
                offset = int(offset)
                limit = int(limit)
                
                if (offset < 0 or limit < 0) or (offset > limit):
                    return Response({"error": "BAD_REQUEST"}, status=400)
        else:
            offset = 0
            limit = 20

        ##### price min and price max should be integers and greater than 0
        if min_price and max_price:
            if not (min_price.isdigit() and max_price.isdigit()) or (int(min_price) < 0 or int(max_price) < 0) or (int(min_price) > int(max_price)):
                return Response({"error": "BAD_REQUEST"}, status=400)
        else :
            min_price = 0
            max_price = 1000000
        
        ##### category_ids, personalization_method_ids, theme_ids, design_id, organization_ids, sponsored_organization_ids should be valid uuid format
        if category_ids:
            # remove the white spaces
            category_ids = category_ids.replace(" ", "")
            # split the string into a list
            category_ids = category_ids.split(",")
            if not is_all_valid_uuid4(category_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
            # Get all the leaf categories
            category_ids = Category.get_leaf_categories_from_list(category_ids)
        
        if department_ids:
            # remove the white spaces
            department_ids = department_ids.replace(" ", "")
            # split the string into a list
            department_ids = department_ids.split(",")
            if not is_all_valid_uuid4(department_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if personalization_method_ids:
            # remove the white spaces
            personalization_method_ids = personalization_method_ids.replace(" ", "")
            # split the string into a list
            personalization_method_ids = personalization_method_ids.split(",")
            if not is_all_valid_uuid4(personalization_method_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if theme_ids:
            # remove the white spaces
            theme_ids = theme_ids.replace(" ", "")
            # split the string into a list
            theme_ids = theme_ids.split(",")
            if not is_all_valid_uuid4(theme_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if design_ids:
            # remove the white spaces
            design_ids = design_ids.replace(" ", "")
            # split the string into a list
            design_ids = design_ids.split(",")
            if not is_all_valid_uuid4(design_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if brands:
            # brands has to be a string and not longer than 100 characters
            if not isinstance(brands, str) or len(search_term) > 100:
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if models:
            # models has to be a string and not longer than 100 characters
            if not isinstance(models, str) or len(search_term) > 100:
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if option_value_ids:
            # remove the white spaces
            option_value_ids = option_value_ids.replace(" ", "")
            # split the string into a list
            option_value_ids = option_value_ids.split(",")
            if not is_all_valid_uuid4(option_value_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if organization_ids:
            # remove the white spaces
            organization_ids = organization_ids.replace(" ", "")
            # split the string into a list
            organization_ids = organization_ids.split(",")
            if not is_all_valid_uuid4(organization_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if workshop_ids:
            # remove the white spaces
            workshop_ids = workshop_ids.replace(" ", "")
            # split the string into a list
            workshop_ids = workshop_ids.split(",")
            if not is_all_valid_uuid4(workshop_ids):
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if sponsored_organizations:
            # sponsored_organizations should ba valid boolean value
            if sponsored_organizations not in ["true","True", "false", "False"]:
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if sponsored_products:
            # sponsored_products should ba valid boolean value
            if sponsored_products not in ["true","True", "false", "False"]:
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if with_promotion:
            # with_promotion should ba valid boolean value
            if with_promotion not in ["true","True"]:
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if search_term:
            # search term has to be a string and not longer than 100 characters
            if not isinstance(search_term, str) or len(search_term) > 100:
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if publication_date:
            # publication date has to be a string and in the format YYYY-MM-DD
            if not isinstance(publication_date, str) or len(publication_date) != 10:
                return Response({"error": "BAD_REQUEST"}, status=400)
            if datetime.strptime(publication_date, '%d-%m-%Y'):
                publication_date = datetime.strptime(publication_date, '%d-%m-%Y')

        ###########################################################################

        try :
            # Get the products based on the query parameters
            products = Product.get_products(
                                            offset=offset,
                                            limit=limit,
                                            
                                            max_price=max_price,
                                            min_price=min_price,
                                            
                                            category_ids=category_ids, 
                                            department_ids=department_ids,
                                            organization_ids=organization_ids, 
                                            workshop_ids=workshop_ids,
                                            
                                            personalization_method_ids=personalization_method_ids, 
                                            design_ids=design_ids, 
                                            theme_ids=theme_ids, 
                                            
                                            sponsored_products=sponsored_products,
                                            sponsored_workshops=workshop_ids,
                                            sponsored_organizations=sponsored_organizations,
                                            
                                            publication_date=publication_date,

                                            search_term=search_term)

            # Return the response
            response = Response(products, status=status.HTTP_200_OK)
            return response
        except Exception as e:
            logging.error(f"get_products_light action method error :{e.args} ")
            return Response({"error": "UNKNOWN_ERROR"}, status=400)

    @action(detail=True, methods=['GET'], url_path='details', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_product_detail(self, request, pk=None):
        """
        This method is used to get the detail of a product
        """
        self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        self.authentication_classes = []
        try:
            # Get the product id
            product_id = pk
            if not product_id:
                return Response({"error": "BAD_REQUEST"}, status=400)
            # First check if the product exists and that it's not self made or not to be published
            product: Product = get_object_or_404(Product, id=product_id)
            if not product or product.self_made or not product.to_be_published:
                return Response({"error": "NOT_FOUND"}, status=404)
            
            # Get the full details  of the product
            product_details: dict = Product.get_full_product_details(product_id)
            response = Response(product_details, status=status.HTTP_200_OK)

            return response
        except Exception as e:
            logging.error(f"get_product_detail action method error :{e.args} ")
            return Response({"error": "UNKNOWN_INTERNAL_ERROR"}, status=400)
    