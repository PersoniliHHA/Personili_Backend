# Rest framework
from rest_framework.authentication import BaseAuthentication

import logging as logger


logger.basicConfig(level=logger.DEBUG)



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
        logger.debug('JWTAuthentication.authenticate()')
        raw_token: str = request.META.get('Authorization')
        
        # Check if the token is present
        if not raw_token:
            return None
        
        # Separate the token from the prefix Bearer
        token = raw_token.split(' ')[1]
        logger.debug(f'JWTAuthentication.authenticate() - token: {token}')
        
        return None