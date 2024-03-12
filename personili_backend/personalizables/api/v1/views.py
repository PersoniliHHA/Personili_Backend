# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Local imports
from personalizables.models import Category, PersonalizationType, PersonalizationMethod, Personalizable, PersonalizableVariant, PersonalizableZone
from personalizables.api.v1.serializers import CategorySerializer, PersonalizationTypeGetSerializer, PersonalizationMethodGetSerializer
from accounts.models import AccountProfile

# Standard imports
from typing import List


# configure logging 
import logging
logging.basicConfig(level=logging.DEBUG)

#################################
#     Cat/Sub ViewSet           #
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
            return Response(status=status.HTTP_400_BAD_REQUEST)
            



#################################
#  Personalization   ViewSet    #
#################################
class PersonalizationTypeViewSet(viewsets.ModelViewSet):
    """
    Viewset for the PersonalizationType class, as well as the Personalization method
    """
    queryset = PersonalizationType.objects.all()
    serializer_class = PersonalizationTypeGetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_user_profile(self):
        """This method returns the user profile of the user who made the request"""
        user_profile = get_object_or_404(AccountProfile, user=self.request.user)
        return user_profile
    

    # Get all personalization types
    @action(detail=False, methods=['GET'], url_path='v1/personalization-types')
    def get_all_personalization_types(self, request):
        """This method returns all personalization types"""
        response = Response()
        response.data = PersonalizationType.get_all_personalization_types()
        response.status_code = status.HTTP_200_OK

        return response
    

    # Get all personalization types and their methods
    @action(detail=False, methods=['GET'], url_path='v1/personalization-types-and-methods')
    def get_all_personalization_types_and_methods(self, request):
        """This method returns all personalization types and methods"""
        response = Response()
        response.data = PersonalizationType.get_all_personaliation_types_with_related_personalization_methods()
        response.status_code = status.HTTP_200_OK

        return response

    
    # Get all personalizables and their zones based on the personalization type
    @action(detail=False, methods=['GET'], url_path='v1/get-personalizables-with-zones-based-on-personalization-type', permission_classes=[permissions.IsAuthenticated])
    def get_all_personizables_and_their_zones_based_on_personalization_type(self, request):
        """
        This method gets all personalizables and their zones based on the personalization type
        """
        # check that the personalization_type_id is in the request
        if not request.query_params.get('personalization_type_id'):
            logging.error("content of query params:",request.query_params)
            logging.error("get_all_personizables_and_their_zones_based_on_personalization_type error : personalization_type_id not in query params")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response = Response()
        try :
            response.data = PersonalizationType.get_allowed_personalizables_and_their_zones_for_personalization_type(request.query_params.get('personalization_type_id'))
            response.status_code = status.HTTP_200_OK
        except Exception as e:
            logging.error(f"get_all_personizables_and_their_zones_based_on_personalization_type error : {e}")
            response.status_code = status.HTTP_400_BAD_REQUEST

        return response