# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Local imports
from designs.models import Store, Design, Collection, Theme
from accounts.models import AccountProfile
from designs.api.v1.serializers import DesignSerializerBase, ThemeSerializerGet
from utils.constants import DESIGNER_UPLOADED_IMAGES_PATH_TEMPLATES
from utils.validators import is_all_valid_uuid4

from security.authentication.jwt_authentication_class import JWTAuthentication


# boto3 imports
import boto3
from botocore.exceptions import ClientError

# logger
import logging

# set the logging on the debug level
logger = logging.getLogger(__name__)


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
    
    def get_user_profile(self):
        user_profile = get_object_or_404(AccountProfile, user=self.request.user)
        return user_profile

    ################################### GET/POST APIS, PUBLIC #####################################
    
    ##### Get the designs based on criteria : theme, store, workshop, nb of likes, sponsored stores, sponsored workshops
    @action(detail=False, methods=['POST'], url_path='catalog', permission_classes=[permissions.AllowAny])
    def get_designs(self, request):
        """
        Get the designs based on different criterias : 
        - themes
        - stores
        - workshops
        - sponsored stores
        - sponsored organizations
        - search term
        - offset
        - limit
        - free
        - Latest publication date
        - promotion ids
        """
        self.permission_classes = [permissions.AllowAny]
        self.authentication_classes = []
        # Get the query parameters from the request
        offset = request.data.get('offset', None)
        limit = request.data.get('limit', None)

        min_price = request.data.get('min_price', None)
        max_price = request.data.get('max_price', None)

        # Latest publication date
        latest_publication_date_max = request.data.get('latest_publication_date_max', None)
        latest_publication_date_min = request.data.get('latest_publication_date_min', None)

        theme_ids = request.data.get('themes', None)
        store_ids = request.data.get('stores', None)
        workshop_ids = request.data.get('workshops', None)
        organization_ids = request.data.get('organizations', None)
        promotion_ids = request.data.get('promotions', None)
        events_ids = request.data.get('events', None)
        
        sponsored_stores = request.data.get('sponsored_stores', None)
        sponsored_organizations = request.data.get('sponsored_organizations', None)
        sponsored_designs = request.data.get('sponsored_designs', None)
        sponsored_workshops = request.data.get('sponsored_workshops', None)

        search_term = request.data.get('search_term', None)
        free = request.data.get('free', None)
        tags = request.data.get('tags', None)

        ####################### Query parameters validation ########################
        if offset and limit:
            if not (offset.isdigit() and limit.isdigit()):
                logger.debug("offset and limit should be integers")
                return Response({"error": "BAD_REQUEST"}, status=400)
            else:
                offset = int(offset)
                limit = int(limit)
                print(type(offset), type(limit))
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

        if free:
            if free not in ["true","True"]:
                logger.debug("free should be a boolean value")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if theme_ids:
            # remove the white spaces
            theme_ids = theme_ids.replace(" ", "")
            # split the string into a list
            theme_ids = theme_ids.split(",")
            if not is_all_valid_uuid4(theme_ids):
                logger.debug("theme_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
            
        if organization_ids:
            # remove the white spaces
            organization_ids = organization_ids.replace(" ", "")
            # split the string into a list
            organization_ids = organization_ids.split(",")
            if not is_all_valid_uuid4(organization_ids):
                logger.debug("organization_ids should be a list of valid uuid4")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if store_ids:
            # remove the white spaces
            store_ids = store_ids.replace(" ", "")
            # split the string into a list
            store_ids = store_ids.split(",")
            if not is_all_valid_uuid4(store_ids):
                logger.debug("store_ids should be a list of valid uuid4")
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
        
        if sponsored_stores:
            # sponsored_stores should ba valid boolean value
            if sponsored_stores not in ["true","True"]:
                logger.debug("sponsored_stores should be a boolean value")
                return Response({"error": "BAD_REQUEST"}, status=400)
        
        if sponsored_designs:
            # sponsored_designs should ba valid boolean value
            if sponsored_designs not in ["true","True"]:
                logger.debug("sponsored_designs should be a boolean value")
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
            
        if tags:
            # tags should be a string
            if not isinstance(tags, str):
                logger.debug("tags should be a string")
                return Response({"error": "BAD_REQUEST"}, status=400)
        try :

            popular_designs = Design.get_designs(   latest_publication_date_max=latest_publication_date_max,
                                                    latest_publication_date_min=latest_publication_date_min,
                                                    
                                                    offset=offset, 
                                                    limit=limit,
                                                    
                                                    min_price = min_price,
                                                    max_price = max_price,
                                                    
                                                    theme_ids=theme_ids,
                                                    
                                                    store_ids=store_ids,
                                                    workshop_ids=workshop_ids,
                                                    organization_ids=organization_ids,
                                                    
                                                    promotion_ids=promotion_ids,
                                                    events_ids=events_ids,

                                                    sponsored_stores=sponsored_stores,
                                                    sponsored_organizations=sponsored_organizations,
                                                    sponsored_workshops=sponsored_workshops,
                                                    sponsored_designs=sponsored_designs,
                                                    
                                                    search_term=search_term,
                                                    tags=tags,
                                                    free=free
                                                )
        except Exception as e:
            logging.error(e)
            logging.error(f"get_popular_designs_light action method error :{e.args} ")
            return Response({"error": "UNKNOWN_ERROR"}, status=400)
            
        response = Response(popular_designs, status=status.HTTP_200_OK)

        return response
    
    ##### Get the full design
    @action(detail=False, methods=['GET'], url_path='(?P<design_id>[^/.]+)/details', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_design_by_id(self, request, design_id=None):
        """
        Get the full details of a design by its id
        """
        self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        self.authentication_classes = []

        if not is_all_valid_uuid4([design_id]):
            return Response({"error": "BAD_REQUEST"}, status=400)
        # first check if the design exists and that it is to be published and that is approved
        design = Design.objects.filter(id=design_id).first()
        if not design or not design.status == Design.APPROVED or not design.to_be_published or design.regular_user:
            return Response({"error": "NOT_FOUND"}, status=404)
        
        try :
            design_details = Design.get_full_design_details(design_id=design_id)
            response = Response(design_details, status=status.HTTP_200_OK)
            return response
        
        except Exception as e:
            logging.error(f"get_design_by_id action method error :{e.args} ")
            return Response({"error": "UNKNOWN_ERROR"}, status=400)

    ##### Get the themes
    @action(detail=False, methods=['GET'], url_path='themes', permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def get_themes(self, request):
        """
        Get all themes
        """
        self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        self.authentication_classes = []
        try:

            themes = Theme.objects.all()
            serializer = ThemeSerializerGet(themes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"get_themes action method error :{e.args} ")
            return Response({"error": "UNKNOWN_ERROR"}, status=400)

    ################################### POST APIS, PRIVATE #####################################
    ##### Like a design
    @action(detail=True, methods=['POST'], url_path='like')
    def like_design(self, request, pk=None):
        """
        Like a design
        """
        self.authentication_classes = [JWTAuthentication]
        self.permission_classes = [permissions.IsAuthenticated]
        
        account = request.user
        account_profile = AccountProfile.objects.get(account=account)
        
        # Check the design exists
        design = get_object_or_404(Design, pk=pk)
        if not design:
            return Response({"error": "NOT_FOUND"}, status=404)
        
        # Check if the user has already liked the design
        if design.is_liked_by(account_profile):
            return Response({"error": "ALREADY_LIKED"}, status=400)
        
        try:
            design.like(account_profile)
            return Response({"message": "LIKED"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"like_design action method error :{e.args} ")
            return Response({"error": "UNKNOWN_ERROR"}, status=400)
        
    ##### Unlike a design
    @action(detail=True, methods=['POST'], url_path='unlike')
    def unlike_design(self, request, pk=None):
        """
        Unlike a design
        """
        self.authentication_classes = [JWTAuthentication]
        self.permission_classes = [permissions.IsAuthenticated]
        
        account = request.user
        account_profile = AccountProfile.objects.get(account=account)
        
        # Check the design exists
        design = get_object_or_404(Design, pk=pk)
        if not design:
            return Response({"error": "NOT_FOUND"}, status=404)
        
        # Check if the user has already liked the design
        if not design.is_liked_by(account_profile):
            return Response({"error": "NOT_LIKED"}, status=400)
        
        try:
            design.unlike(account_profile)
            return Response({"message": "UNLIKED"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"unlike_design action method error :{e.args} ")
            return Response({"error": "UNKNOWN_ERROR"}, status=400)
    
    ##### Is the design liked by the user
    @action(detail=True, methods=['GET'], url_path='is-liked-by', permission_classes=[permissions.IsAuthenticated])
    def is_liked_by(self, request, pk=None):
        """
        Check if the design is liked by the user
        """
        self.authentication_classes = [JWTAuthentication]
        self.permission_classes = [permissions.IsAuthenticated]
        
        account = request.user
        account_profile = AccountProfile.objects.get(account=account)
        
        # Check the design exists
        design = get_object_or_404(Design, pk=pk)
        if not design:
            return Response({"error": "NOT_FOUND"}, status=404)
        
        # Check if the user has already liked the design
        if design.is_liked_by(account_profile):
            return Response({"message": "LIKED"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "NOT_LIKED"}, status=status.HTTP_200_OK)
    