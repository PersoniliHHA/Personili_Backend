# Standard Library Imports
import base64
from datetime import UTC, datetime, timedelta
from typing import Optional

# settings
from django.conf import settings

from accounts.models import Account


# Cryptogrphay imports
import hmac
import hashlib
import json

####################################
## JWT (JSON Web Token) Functions ##
###################################

def base64url_encode(input: str) -> str:
    """This method encodes a string to base64url"""
    if isinstance(input, str):
        input = input.encode("utf-8")
    encoded_bytes = base64.urlsafe_b64encode(input)
    encoded_string = encoded_bytes.decode("utf-8").rstrip("=")
    return encoded_string
    
def base64url_decode(input: str) -> str:
    """This method decodes a base64url string"""
    input += "=" * (4 - len(input) % 4)
    decoded_bytes = base64.urlsafe_b64decode(input.encode("utf-8"))
    decoded_string = decoded_bytes.decode("utf-8")
    return decoded_string
    

#################### JWT Token Generation and Verification ####################
def generate_jwt_token(registred_claims: dict, 
                       private_claims: dict = {},
                       public_claims: dict = {}):
    """This method creates a jwt token"""

    header: dict = {
        "alg": settings.JWT_SIGNING_ALGORITHM,
        "typ": "JWT"
    }
    payload: dict = {
        "registered_claims": registred_claims,
        "private_claims": private_claims,
        "public_claims": public_claims
    }
    secret = settings.JWT_SECRET_KEY
    signature = hmac.new(secret.encode("utf-8"), 
                         msg=(base64url_encode(json.dumps(header)) + "." + base64url_encode(json.dumps(payload))).encode("utf-8"), 
                         digestmod=hashlib.sha3_512).digest()
    signature = base64url_encode(signature)
    
    return f"{base64url_encode(json.dumps(header))}.{base64url_encode(json.dumps(payload))}.{signature}"

def verify_jwt_token(token: str, type: str):
    """This method verifies a jwt token"""
    header, payload, signature = token.split(".")
    secret = settings.JWT_SECRET_KEY
    expected_signature = hmac.new(secret.encode("utf-8"), 
                                  msg=(header + "." + payload).encode("utf-8"), 
                                  digestmod=hashlib.sha3_512).digest()
    expected_signature = base64url_encode(expected_signature)
    if signature != expected_signature:
        return {
            "is_valid_token": False
        }
    
    else:
        # Decode the payload
        payload_decoded = json.loads(base64url_decode(payload))

        # Check if the token is of the right type
        if payload_decoded.get('private_claims').get('tk') != type:
            return {
                "is_valid_token": False,
                "error": "Token is not of the right type"
            }

        # Check if the token is expired
        if 'exp' in payload_decoded.get('registered_claims') and datetime.now() > datetime.fromtimestamp(payload_decoded.get('registered_claims').get('exp')):
            return {
                "is_valid_token": False,
                "error": "Token is expired"
            }
        
        return {
            "is_valid_token": True,
            "header": base64url_decode(header),
            "payload": base64url_decode(payload)
        }

# Access token creation and verification
def create_access_token(account_id: Optional[str] = None, role_id: Optional[str] = None):
    """This method creates an access token"""
    nb_days = settings.JWT_ACCESS_TOKEN_EXPIRATION 
    future_exp_time = datetime.now(UTC) + timedelta(days=nb_days)
    registred_claims = {
        "iss": "personili",
        "sub": "personili_api",
        "exp": future_exp_time.timestamp()
    }
    private_claims = {
        "aid": account_id,
        "rid": role_id,
        "tk": "acc"
    }
    access_token: str = generate_jwt_token(registred_claims, private_claims)
    return access_token

def verify_access_token(token: str):
    """This method verifies an access token"""
    return verify_jwt_token(token, "acc")


# Refresh token creation and verification
def create_refresh_token(account_id: str):
    """This method creates a refresh token"""
    nb_days = settings.JWT_REFRESH_TOKEN_EXPIRATION
    future_exp_time = datetime.utcnow() + timedelta(days=nb_days)
    registred_claims = {
        "iss": "personili",
        "sub": "personili_api",
        "exp": future_exp_time.timestamp()
    }
    private_claims = {
        "aid": account_id,
        "rid": None,
        "tk": "ref"
    }
    refresh_token: str = generate_jwt_token(registred_claims, private_claims)
    return refresh_token

def verify_refresh_token(token :str):
    """This method verifies a refresh token"""
    return verify_jwt_token(token, "ref")


# Verify the token components
def verify_token_components(token_components: dict, token_type: str):
    """
    Verify the payload and header components of a token
    """
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
    
    # Check that the token is not expired
    if not 'exp' in registered_claims or datetime.now(UTC).timestamp() > registered_claims.get('exp'):
        return None
    
    # check the private claims
    private_claims = payload.get('private_claims')
    if not private_claims:
        return None
    
    if not private_claims.get('tk'):
        return None
    if private_claims.get('tk') != token_type:
        return None
    
    # get the account profile
    account_id = private_claims.get('aid')
    if not account_id:
        return None
    
    # check if the account profile exists
    try:
        account = Account.objects.get(id=account_id)
        return account
    except Account.DoesNotExist:
        return None
    
    return None