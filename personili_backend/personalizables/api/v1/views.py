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
#  Personalizables   ViewSet    #
#################################
class PersonalizableViewSet(viewsets.ViewSet):
    """Viewset for the personalizable class"""

    queryset = Personalizable.objects.all()
    permission_classes = []

    @action(detail=False, methods=['POST'], url_path='catalog', permission_classes=[permissions.AllowAny])
    def get_all_personalizables(self, request):
        """Method that returns all personalizables"""
        try:
            response_data: List = Personalizable.get_personalizables()
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"UNKNOWN_ERROR : {e}")
            return Response({
                "error": "UNKNOWN_ERROR"
            },status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='personalizables/(?P<pk>[^/.]+)', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_personalizable(self, request, pk=None):
        """Method that returns a personalizable object"""
        try:
            personalizable = get_object_or_404(Personalizable, pk=pk)
            response_data = personalizable.get_personalizable()
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