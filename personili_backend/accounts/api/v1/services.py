# Django
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from rest_framework import status

# Serializers
from personili_backend.personili_backend.accounts.api.v1.serializers import UserSignUpSerializer

# Models
from accounts.models import UserProfile, DeliveryAddress, PaymentMethod
from designs.models import Store, Collection
# Errors
from django.db import transaction, IntegrityError, DatabaseError, Error

# Standard imports
import logging as logger

# Local imports
from utils.utilities import upload_image_to_S3_bucket
from utils.constants import USER_UPLOADED_PROFILE_PICTURE_PATH_PREFIX


logger.basicConfig(level=logger.DEBUG)
User = get_user_model()


#################################
#                               #
#     User Creation             #
#                               #
#################################

def create_new_user(serializer: UserSignUpSerializer) -> User:
    try:
        with transaction.atomic():
            # Create the user and save it to the database
            user = serializer.save()

            # Create an empty user profile for the user
            profile = UserProfile()
            profile.user = user
            profile.save()

            # Create an empty store for the user
            store = Store()
            store.user_profile = profile.id
            store.save()

            # Create an empty collection for the user and attach it to the store
            collection = Collection()
            collection.store = store.id
            collection.save()

            # Create an empty payment method for the user
            payment_method = PaymentMethod()
            payment_method.user_profile = profile.id
            payment_method.save()

    except IntegrityError as e:
        logger.error("Integrity Error: {}".format(e))
        return Response(
            {"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except DatabaseError as e:
        logger.error("Database Error: {}".format(e))
        return Response(
            {"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Error as e:
        logger.error("Error: {}".format(e))
        return Response(
            {"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


#################################
#                               #
#     Profile Udpates           #
#                               #
#################################
def update_user_profile():
    pass

def update_user_profile_picture(file, profile_id, user_email):
    """
    Takes a file and a file path and uploads the file to the S3 bucket
    """
    # Create the file path
    file_path: str = USER_UPLOADED_PROFILE_PICTURE_PATH_PREFIX + f"/{profile_id}-{user_email}/" + "main_profile_picture"





#################################
#                               #
#     Feedback APIs             #
#                               #
#################################

#################################
#                               #
#     Wallet and                #
#     transaction APIs          #
#                               #
#################################
def create_new_transaction(request_data: dict) -> Response:
    pass

def create_new_wallet(request_data: dict) -> Response:
    pass

def update_existing_wallet(request_data: dict) -> Response:
    pass

def delete_existing_wallet(request_data: dict) -> Response:
    pass

def get_wallet_details(request_data: dict) -> Response:
    pass

def get_transaction_details(request_data: dict) -> Response:
    pass

#################################
#                               #
#     Wallet and                #
#     transaction APIs          #
#                               #
#################################
