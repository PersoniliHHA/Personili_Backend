# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Local imports
from personalizables.models import Department, Category, PersonalizationType, PersonalizationMethod, Personalizable, PersonalizableVariant, PersonalizableZone
from accounts.models import AccountProfile
from utils.validators import is_all_valid_uuid4

# Standard imports
from typing import List


# configure logging 
# logger
import logging

# set the logging on the debug level
logger = logging.getLogger(__name__)

#################################
#     Cat ViewSet              #
#################################

class CategoryViewSet(viewsets.ViewSet):
    """Viewset for the category class, it uses a method decorated by the action decorator to
     retrieve all categories and their subcategories"""

    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['GET'], url_path='categories', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_all_categories(self, request):
        """Method that returns all categories and their subcategories"""
        try:
            response_data: List = Category.get_category_tree()
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"UNKNOWN_ERROR : {e}")
            return Response({
                "error": "UNKNOWN_ERROR"
            },status=status.HTTP_400_BAD_REQUEST)


#################################
#     Cat ViewSet           #
#################################

class DepartmentViewSet(viewsets.ViewSet):
    """Viewset for the department class"""

    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['GET'], url_path='departments', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_all_departments(self, request):
        """Method that returns all categories and their subcategories"""
        try:
            response_data: List = Department.get_all_departments()
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"UNKNOWN_ERROR : {e}")
            return Response({
                "error": "UNKNOWN_ERROR"
            },status=status.HTTP_400_BAD_REQUEST)

#################################
#  Personalizables   ViewSet    #
#################################
class PersonalizableViewSet(viewsets.ViewSet):
    """Viewset for the personalizable class"""

    queryset = Personalizable.objects.all()
    permission_classes = []

    @action(detail=False, methods=['POST'], url_path='catalog', permission_classes=[permissions.AllowAny])
    def get_all_personalizables(self, request):
        """Method that returns all personalizables"""
        # Get the query parameters from the request
        offset = request.data.get('offset', None)
        limit = request.data.get('limit', None)

        min_price = request.data.get('min_price', None)
        max_price = request.data.get('max_price', None)

        brands = request.data.get('brands', None)
        models = request.data.get('models', None)

        category_ids = request.data.get('categories', None)
        departement_ids = request.data.get('departements', None)

        option_values_ids = request.data.get('option_values', None)

        workshop_ids = request.data.get('workshops', None)
        organization_ids = request.data.get('organizations', None)
        promotion_ids = request.data.get('promotions', None)
        events_ids = request.data.get('events', None)
        
        sponsored_organizations = request.data.get('sponsored_organizations', None)
        sponsored_workshops = request.data.get('sponsored_workshops', None)
        sponsored_personalizables = request.data.get('sponsored_personalizables', None)

        search_term = request.data.get('search_term', None)

        ####################### Query parameters validation ########################
        if offset and limit:
            if not (offset.isdigit() and limit.isdigit()):
                logger.debug("offset and limit should be integers")
                return Response({"error": "BAD_REQUEST"}, status=400)
            else:
                offset = int(offset)
                limit = int(limit)
                if (offset < 0 or limit < 0) or (offset > limit) or (limit - offset > 50):
                    logger.debug("offset and limit should be positive integers and offset should be less than limit and limit should be less than 50")
                    return Response({"error": "BAD_REQUEST"}, status=400)
        else:
            offset = 0
            limit = 20
        
        if max_price and min_price:
            if not (max_price.isdigit() and min_price.isdigit()):
                logger.debug("max_price and min_price should be integers")
                return Response({"error": "BAD_REQUEST"}, status=400)
            else:
                max_price = int(max_price)
                min_price = int(min_price)
                if (max_price < 0 or min_price < 0) or (max_price < min_price):
                    logger.debug("max_price and min_price should be positive integers and max_price should be greater than min_price")
                    return Response({"error": "BAD_REQUEST"}, status=400)

        if organization_ids:
            # remove the white spaces
            organization_ids = organization_ids.replace(" ", "")
            # split the string into a list
            organization_ids = organization_ids.split(",")
            if not is_all_valid_uuid4(organization_ids):
                logger.debug("organization_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        
        if promotion_ids :
            # remove the white spaces
            promotion_ids = promotion_ids.replace(" ", "")
            # split the string into a list
            promotion_ids = promotion_ids.split(",")
            if not is_all_valid_uuid4(promotion_ids):
                logger.debug("promotion_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if events_ids :
            # remove the white spaces
            events_ids = events_ids.replace(" ", "")
            # split the string into a list
            events_ids = events_ids.split(",")
            if not is_all_valid_uuid4(events_ids):
                logger.debug("events_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if sponsored_organizations:
            # sponsored_organizations should ba valid boolean value
            if sponsored_organizations not in ["true","True"]:
                logger.debug("sponsored_organizations should be a boolean value")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if sponsored_workshops:
            # sponsored_workshops should ba valid boolean value
            if sponsored_workshops not in ["true","True"]:
                logger.debug("sponsored_workshops should be a boolean value")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if workshop_ids:
            # remove the white spaces
            workshop_ids = workshop_ids.replace(" ", "")
            # split the string into a list
            workshop_ids = workshop_ids.split(",")
            if not is_all_valid_uuid4(workshop_ids):
                logger.debug("workshop_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if search_term:
            # search term has to be a string and not longer than 100 characters
            if not isinstance(search_term, str) or len(search_term) > 100:
                logger.debug("search_term should be a string and not longer than 100 characters")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if category_ids:
            # remove the white spaces
            category_ids = category_ids.replace(" ", "")
            # split the string into a list
            category_ids = category_ids.split(",")
            if not is_all_valid_uuid4(category_ids):
                logger.debug("category_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if departement_ids:
            # remove the white spaces
            departement_ids = departement_ids.replace(" ", "")
            # split the string into a list
            departement_ids = departement_ids.split(",")
            if not is_all_valid_uuid4(departement_ids):
                logger.debug("departement_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if option_values_ids:
            # remove the white spaces
            option_values_ids = option_values_ids.replace(" ", "")
            # split the string into a list
            option_values_ids = option_values_ids.split(",")
            if not is_all_valid_uuid4(option_values_ids):
                logger.debug("option_values_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if brands:
            # split the string into a list
            brands = brands.split(",")
            if not all(isinstance(brand, str) for brand in brands):
                logger.debug("brands should be a list of strings")
                return Response({"error": "BAD_REQUEST"}, status=400)
        if models:
            # split the string into a list
            models = models.split(",")
            if not all(isinstance(model, str) for model in models):
                logger.debug("models should be a list of strings")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        try:
            response_data: List[dict] = Personalizable.get_personalizables(
                offset=offset,
                limit=limit,
                min_price=min_price,
                max_price=max_price,
                brands=brands,
                models=models,
                category_ids=category_ids,
                department_ids=departement_ids,
                option_values_ids=option_values_ids,
                workshop_ids=workshop_ids,
                organization_ids=organization_ids,
                promotion_ids=promotion_ids,
                events_ids=events_ids,
                sponsored_personalizables=sponsored_personalizables,
                sponsored_organizations=sponsored_organizations,
                sponsored_workshops=sponsored_workshops,
                search_term=search_term
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"UNKNOWN_ERROR : {e}")
            return Response({
                "error": "UNKNOWN_ERROR"
            },status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='(?P<personalizable_id>[^/.]+)/details', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_personalizable_details_by_id(self, request, personalizable_id=None):
        """Method that returns a personalizable object"""
        try:
            # Check if the personalizable id is present in the url
            if not personalizable_id or not is_all_valid_uuid4(personalizable_id):
                return Response({
                    "error": "BAD_REQUEST"
                }, status=status.HTTP_400_BAD_REQUEST)
            personalizable = get_object_or_404(Personalizable, pk=personalizable_id)
            
            # Check if the workshop linked to this personalizable is active
            if not personalizable.workshop.is_active:
                return Response({
                "error": "BAD_REQUEST"
                }, status=status.HTTP_400_BAD_REQUEST)

            response_data = personalizable.get_personalizable_details(personalizable_id=personalizable_id)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"UNKNOWN_ERROR : {e}")
            return Response({
                "error": "UNKNOWN_ERROR"
            },status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='personalizables/(?P<pk>[^/.]+)/variants', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_personalizable_variants(self, request, pk=None):
        """Method that returns all variants of a personalizable object"""
        try:
            personalizable = get_object_or_404(Personalizable, pk=pk)
            response_data = personalizable.get_personalizable_variants()
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"UNKNOWN_ERROR : {e}")
            return Response({
                "error": "UNKNOWN_ERROR"
            },status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='personalizables/(?P<pk>[^/.]+)/zones', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_personalizable_zones(self, request, pk=None):
        """Method that returns all zones of a personalizable object"""
        pass