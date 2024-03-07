# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Local imports
from designs.models import Store, Design, Collection, Theme
from accounts.models import AccountProfile
from designs.api.v1.serializers import DesignSerializerBase, DesignPostSerializer, DesignGetSerializerLight, ThemeSerializerGet
from utils.constants import DESIGNER_UPLOADED_IMAGES_PATH_TEMPLATES
from utils.utilities import store_image_in_s3


# boto3 imports
import boto3
from botocore.exceptions import ClientError

# logger
import logging

# set the logging on the debug level
logging.basicConfig(level=logging.DEBUG)

#################################
#                               #
#   Public Stores ViewSet       #
#                               #
#################################

class PublicStoresViewSet_GetStores(viewsets.ModelViewSet):
    """
       - ViewSet for the Store model and StoreSerializer_GetStores serializer
       - Connected to the API that fetches a list of all stores
       -
    """
    pass


#################################
#                               #
#  Designs ViewSet              #
#                               #
#################################
class DesignsViewSet(viewsets.ViewSet):
    """
    ViewSet for the Design class
    """
    queryset = Design.objects.all()
    serializer_class = DesignSerializerBase
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_user_profile(self):
        user_profile = get_object_or_404(AccountProfile, user=self.request.user)
        return user_profile

    def get_serializer_class(self):
        if self.action == "add-new-design-for-designer":
            return DesignPostSerializer
        elif self.action == "get-all-designs-by-criteria-light":
            return DesignGetSerializerLight

        return DesignSerializerBase

    ################################### GET APIS, PUBLIC #####################################
    
    ##### Get the designs based on criteria : theme, store, workshop, nb of likes, sponsored stores, sponsored workshops
    @action(detail=False, methods=['GET'], url_path='v1/designs', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_designs_light(self, request):
        """
        Get the designs based on different criterias : 
        - theme
        - store
        - workshop
        - sponsored stores
        - sponsored organizations
        - search term
        """
        # Get the query parameters from the request
        theme = request.query_params.get('theme', None)
        store = request.query_params.get('store', None)
        workshop = request.query_params.get('workshop', None)
        sponsored_stores = request.query_params.get('sponsored_stores', None)
        sponsored_organizations = request.query_params.get('sponsored_organizations', None)
        search_term = request.query_params.get('search_term', None)
        try :

            popular_designs = Design.get_designs_light(offset=0, 
                                                    limit=20,
                                                    theme_id=theme,
                                                    store_id=store,
                                                    workshop_id=workshop,
                                                    sponsored_stores=sponsored_stores,
                                                    sponsored_organizations=sponsored_organizations,
                                                    search_term=search_term)
        except Exception as e:
            logging.error(f"get_popular_designs_light action method error :{e.args} ")
            return Response({"error": "UNKNOWN INTERNAL ERROR"}, status=400)
            
        response = Response(popular_designs, status=status.HTTP_200_OK)

        return response

    ##### Get the themes
    @action(detail=False, methods=['GET'], url_path='v1/designs/themes', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_themes(self, request):
        """
        Get all themes
        """
        themes = Theme.objects.all()
        serializer = ThemeSerializerGet(themes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    ###########################################################################################
    
    ################################### GET APIS, PRIVATE #####################################


    ###########################################################################################

class CollectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Collection class
    """
    queryset = Collection.objects.all()
    serializer_class = DesignSerializerBase
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "get_collection_by_id":
            return DesignSerializerBase

        return DesignSerializerBase

    @action(detail=True, methods=['GET'], url_path='get-collection-by-id', permission_classes=[permissions.IsAuthenticated])
    def get_collection_by_id(self, request, pk=None):
        """
        Get a collection by id
        """
        collection = get_object_or_404(Collection, pk=pk)
        serializer = DesignSerializerBase(collection)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'], url_path='get-collection-and-its-designs', permission_classes=[permissions.IsAuthenticated])
    def get_collection_and_its_designs(self, request, pk=None):
        """
        Get a collection and its designs
        """
        collection = get_object_or_404(Collection, pk=pk)
        serializer = DesignSerializerBase(collection)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='get-all-collections', permission_classes=[permissions.IsAuthenticated])
    def get_all_collections(self, request):
        """
        Get all collections
        """
        collections = Collection.objects.all()
        serializer = DesignSerializerBase(collections, many=True)
        return Response(serializer.data)