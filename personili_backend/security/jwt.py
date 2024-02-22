# Settings
from django.conf import settings
import base64
from datetime import datetime, timedelta

# Cryptogrphay imports
import hmac
import hashlib


###################################
## JWT (JSON Web Token) Functions ##
###################################

def base64url_encode(input: str) -> str:
    """This method encodes a string to base64url"""
    encoded_bytes = base64.urlsafe_b64encode(input.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8").rstrip("=")
    return encoded_string
    
def base64url_decode(input: str) -> str:
    """This method decodes a base64url string"""
    input += "=" * (4 - len(input) % 4)
    decoded_bytes = base64.urlsafe_b64decode(input.encode("utf-8"))
    decoded_string = decoded_bytes.decode("utf-8")
    return decoded_string
    

def generate_jwt_token(registred_claims: dict, 
                     private_claims: dict = {},
                     public_claims: dict = {}):
    """This method creates a jwt token"""

    header: dict = {
        "alg": settings.JWT_SIGNING_ALGORITHM,
        "typ": "JWT"
    }
    payload: dict = {
        "registred_claims": registred_claims,
        "private_claims": private_claims,
        "public_claims": public_claims
    }
    secret = settings.JWT_SECRET_KEY

    signature = hmac.new(secret.encode("utf-8"), 
                         msg=(base64url_encode(str(header)) + "." + base64url_encode(str(payload))).encode("utf-8"), 
                         digestmod=hashlib.sha3_512).digest()
    signature = base64url_encode(signature.decode("utf-8"))
    
    return f"{base64url_encode(str(header))}.{base64url_encode(str(payload))}.{signature}"

def verify_jwt_token(token: str):
    """This method verifies a jwt token"""
    header, payload, signature = token.split(".")
    secret = settings.JWT_SECRET_KEY
    expected_signature = hmac.new(secret.encode("utf-8"), 
                                  msg=(header + "." + payload).encode("utf-8"), 
                                  digestmod=hashlib.sha3_512).digest()
    expected_signature = base64url_encode(expected_signature.decode("utf-8"))
    if signature != expected_signature:
        return {
            "is_valid_signature": False
        }
    else:
        # Check if the token is expired

        return {
            "is_valid_signature": True,
            "header": base64url_decode(header),
            "payload": base64url_decode(payload)
        }


def create_access_token(account_profile_id: str):
    """This method creates an access token"""
    nb_days = settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME 
    future_exp_time = datetime.utcnow() + datetime.timedelta(days=nb_days)
    registred_claims = {
        "iss": "personili",
        "sub": "you",
        "exp": future_exp_time.timestamp()
    }
    private_claims = {
        "pr": account_profile_id,
        "tk": "acc"
    }
    access_token: str = generate_jwt_token(registred_claims, private_claims)
    return access_token

def create_refresh_token():
    """This method creates a refresh token"""
    return None

def verify_access_token(token: str):
    """This method verifies an access token"""
    return None

def verify_refresh_token(token :str):
    """This method verifies a refresh token"""
    return None