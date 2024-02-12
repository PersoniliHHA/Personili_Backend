# Rest framework imports
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Standard imports
import boto3
from botocore.client import Config
from typing import Optional

# Local imports
from utils.storages import MediaStorage


######## JWT UTILITIES ########
def is_refresh_token_valid(refresh_token):
    """This method checks if the refresh token is valid or not"""
    try:
        RefreshToken(refresh_token)
    except (TokenError, InvalidToken):
        return False
    return True


def is_access_token_valid(access_token):
    """This method checks if the access token is valid or not"""
    try:
        AccessToken(access_token)
    except (TokenError, InvalidToken):
        return False
    return True


def create_token_pairs(user):
    """This method creates token pairs for a user"""
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    return {
        "access": str(access_token),
        "refresh": str(refresh_token),
    }


######## Cookie Utilities ########

######## Response Utilities ########
class Response:
    """This class is used to create a response object"""

    def __init__(self, success=False, message="UNKNOWN ERROR", status_code=None, data=None):
        self.success = success
        self.message = message
        self.data = data
        self.status_code = status_code

    def get_response(self):
        """This method returns the response object"""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }

