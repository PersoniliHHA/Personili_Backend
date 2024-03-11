# Rest framework 
from rest_framework.authentication import BaseAuthentication

from security.jwt import verify_access_token, verify_refresh_token

###############################
# Custom Authentication Class #
###############################

class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication class
    """
    def authenticate(self, request):
        """
        Custom authenticate method
        """
        raw_token: str = request.META.get('Authorization')
        
        # Check if the token is present
        if not raw_token:
            return None

        # Check if the token if the token is valid
        
        
        # Separate the token from the prefix Bearer
        token = raw_token.split(' ')[1]
        
        return None