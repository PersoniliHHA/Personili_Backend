# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Local imports
from designs.models import Store, Design, Collection, Theme
from accounts.models import AccountProfile
from designs.api.v1.serializers import DesignSerializerBase, DesignPostSerializer, DesignGetSerializerHeavy, DesignGetSerializerLight
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
class DesignsViewSet(viewsets.ModelViewSet):
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

    @action(detail=False, methods=['GET'], url_path='v1/designs/popular', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_popular_designs_light(self, request):
        """
        Get a list of popular designs based on number of likes
        """
        popular_designs = Design.optimized_get_popular_designs_light(offset=0, limit=10)
        response = Response(popular_designs, status=status.HTTP_200_OK)

        return response

    @action(detail=False, methods=['POST'], url_path='v1/add-new-design-for-designer', permission_classes=[permissions.IsAuthenticated])
    def get_design_by_id(self, pk):
        return get_object_or_404(Design, pk=pk)

    @action(detail=False, methods=['GET'], url_path='get-all-designs-by-designer', permission_classes=[permissions.IsAuthenticated])
    def get_designs_by_store(self, request, pk=None):
        """
        Get all designs by store
        """
        designs = Design.objects.filter(store=pk)
        serializer = Design(designs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_designs_by_collection(self, request, pk=None):
        """
        Get all designs by collection
        """
        designs = Design.objects.filter(collection=pk)
        serializer = DesignSerializerBase(designs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def get_designs_by_theme(self, request, pk=None):
        """
        Get all designs by theme
        """
        designs = Design.objects.filter(theme=pk, status="APPROVED", to_publish=True)
        serializer = DesignSerializerBase(designs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], url_path='add-new-design-for-designer', permission_classes=[permissions.IsAuthenticated])
    def add_new_design_for_designer(self, request, pk=None):
        """
        Add a new design
        """
        # Get the store of the user
        user_profile = self.get_user_profile()
        
        # Get the data from the request and validate the serializer
        serializer = DesignPostSerializer(data=request.data)

        if serializer.is_valid():
            try :
                # Create the design
                design_id , image_presigned_url = Design.create_new_design(
                    user_profile=user_profile,
                    serializer=serializer,
                )
            except ClientError as e:
                logging.error(f"add_new_design_for_designer action method error :{str(e)} ")
                return Response({"error": "UNKNOWN INTERNAL ERROR"}, status=400)

            except Exception as e:
                # first log the error
                logging.error(f"add_new_design_for_designer action method error :{e.__str__} ")
                return Response({"error": "UNKNOWN INTERNAL ERROR"}, status=400)

            return Response({"message": "Design created successfully", "design_id": design_id, "image_url": image_presigned_url}, status=201)

        return Response({"error": "BAD REQUEST"}, status=400)


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
