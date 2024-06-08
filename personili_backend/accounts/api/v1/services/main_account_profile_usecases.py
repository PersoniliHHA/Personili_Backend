# Typing
from typing import Optional, Tuple, Union

# Models
from accounts.models import AccountProfile, Account, AccountBlacklist, DeliveryAddress

# rest framework imports
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# AWS
from utils.aws.storage.s3_engine import s3_engine

################### ACCOUNT AND ACCOUNT PROFILE VERIFICATION #####################
def verify_account_and_account_profile(account_id: str, account_profile_id: str) -> Union[Tuple[Tuple[Account, AccountProfile],bool], Tuple[Response, bool]]:
    """
    This method will encapsulate the logic to verify that the account and account profile
    """
    # Check if the account exists
    account = Account.objects.filter(id=account_id).first()
    if not account:
        return (Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST), False)
    
    # First check that the account is not blacklisted
    account_blacklist = AccountBlacklist.is_email_blacklisted(account.email)
    if account_blacklist:
        return (Response({"error": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED), False)
    
    # Check if the account profile exists
    account_profile = AccountProfile.objects.filter(id=account_profile_id).first()
    if not account_profile:
        return (Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST), False)
    
    # Check if the account profile belongs to the account
    if account_profile.account != account:
        print(account_profile.account, account)
        return (Response({"error": "FORBIDDEN"}, status=status.HTTP_403_FORBIDDEN), False)
    
    return ((account, account_profile), True)
    

###################### GET, LIST ###################################################
def get_main_account_personal_information(account_id: str, account_profile_id: str) -> Response:
    """
    Get the personal information of the main account
    """   
    # Verify the account and account profile
    response, success = verify_account_and_account_profile(account_id, account_profile_id)
    if not success:
        return response
    
    account_profile = response[1]
    account = response[0]
    
    # Return the account profile information
    personal_info: dict = {
        "first_name": account_profile.first_name,
        "last_name": account_profile.last_name,
        "email": account.email,
        "phone_number": account_profile.phone_number,
        "date_of_birth": account_profile.date_of_birth,
        "username": account_profile.username,
        "gender": account_profile.gender,
        "social_media_links": account_profile.social_media_links,
        "biography": account_profile.biography,
        "profile_picture_url": s3_engine.generate_presigned_s3_url(account_profile.profile_picture_path) if account_profile.profile_picture_path else None,
    }

    return Response(personal_info, status=status.HTTP_200_OK)


def get_main_account_delivery_addresses(account_id: str, account_profile_id: str) -> dict:
    """
    This method will return the delivery addresses of the main account
    """
    # Verify the account and account profile
    response, success = verify_account_and_account_profile(account_id, account_profile_id)
    if not success:
        return response
    
    account_profile = response[1]
    account = response[0]

    # Return all the delivery addresses
    delivery_addresses: list[dict] = DeliveryAddress.get_delivery_addresses_by_account_profile(account_profile)

    return Response(delivery_addresses, status=status.HTTP_200_OK)
