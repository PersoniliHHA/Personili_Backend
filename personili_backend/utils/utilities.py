# Rest framework imports


# Standard imports
import boto3
from botocore.client import Config
from typing import Optional

from config.settings.base import AWS_ACCESS_KEY_ID



######## JWT UTILITIES ########
def is_refresh_token_valid(refresh_token):
    """This method checks if the refresh token is valid or not"""

    return True


def is_access_token_valid(access_token):
    """This method checks if the access token is valid or not"""

    return True


def create_token_pairs(user):
    """This method creates token pairs for a user"""

    return {

    }

def get_presigned_url_for_image():
    return None

def store_image_in_s3():
    return None


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

