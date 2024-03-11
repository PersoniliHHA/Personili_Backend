# Rest framework 
from rest_framework.authentication import BaseAuthentication

from config import settings

from security.jwt import verify_access_token, verify_refresh_token

from accounts.models import AccountProfile

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
        if not token_components.get('is_valid_signature'):
            return None
        
        # Check the header
        header = token_components.get('header')
        if not header or header.get('alg') != settings.JWT_SIGNING_ALGORITHM or header.get('typ') != 'JWT':
            return None
        # Check the payload
        payload = token_components.get('payload')
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
        
        # get the token type
        token_type = private_claims.get('tk')
        if not token_type or token_type != 'acc':
            return None
        
        # get the account profile
        account_profile_id = private_claims.get('ar')
        if not account_profile_id:
            return None
        
        # check if the account profile exists
        try:
            account_profile = AccountProfile.objects.get(id=account_profile_id)
        except AccountProfile.DoesNotExist:
            return None
        
        return (account_profile, None)

    

