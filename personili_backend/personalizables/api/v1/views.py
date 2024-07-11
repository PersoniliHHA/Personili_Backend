# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Local imports
from personalizables.models import Department, Category, PersonalizationType, PersonalizationMethod, Personalizable, PersonalizableVariant, PersonalizableZone
from accounts.models import AccountProfile

# Standard imports
from typing import List


# configure logging 
import logging
logging.basicConfig(level=logging.DEBUG)

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
#  Personalization   ViewSet    #
#################################


        """This method returns all personalization types and methods"""
        response = Response()
        response.data = PersonalizationType.get_all_personaliation_types_with_related_personalization_methods()
        response.status_code = status.HTTP_200_OK

        return response

    

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