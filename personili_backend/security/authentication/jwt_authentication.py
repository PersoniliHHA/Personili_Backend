# Rest framework 
from rest_framework.authentication import BaseAuthentication

from django.conf import settings

from security.jwt import verify_access_token, verify_refresh_token

from accounts.models import Account

import json
###############################
# Custom Authentication Class #
###############################

class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication class
    """
    def authenticate(self, request):
        """
        Custom authenticate method that checks the validity of the access token
        """
        raw_token: str = request.headers.get('Authorization')
        print(raw_token)
        
        # Check if the token is present
        if not raw_token:
            return None
        
        # Separate the token from the prefix Bearer
        token = raw_token.split(' ')[1]

        # Check if the token if the token is valid
        token_components: dict = verify_access_token(token)
        print(token_components)

        # Check the signature 
        if not token_components.get('is_valid_token'):
            return None
        
        # Check the header
        header = token_components.get('header')
        header = json.loads(header)
        if not header or header.get('alg') != settings.JWT_SIGNING_ALGORITHM or header.get('typ') != 'JWT':
            return None
        
        # Check the payload
        payload = token_components.get('payload')
        payload = json.loads(payload)
        if not payload:
            return None
        
        # Check the registered claims
        registered_claims = payload.get('registered_claims')
        if not registered_claims:
            return None
        if registered_claims.get("iss") != "personili":
            return None
        if registered_claims.get("sub") != "personili_api":
            return None
        # check the private claims
        private_claims = payload.get('private_claims')
        if not private_claims:
            return None
        
        # get the account profile
        account_id = private_claims.get('aid')
        if not account_id:
            return None
        
        # check if the account profile exists
        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return None
        
        return (account, None)

    

jwt_authentication = JWTAuthentication()