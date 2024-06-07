# Models
from accounts.models import AccountProfile, Account, AccountBlacklist

# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

# AWS
from utils.aws.storage.s3_engine import s3_engine

###################### GET, LIST ###################################################
def get_main_account_personal_information(account_id: str, account_profile_id: str) -> Response:
    """
    Get the personal information of the main account
    """
    # Validate the parameters
    if not account_id or not account_profile_id:
        print("condition 3")
        return Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the account exists
    account = Account.objects.filter(id=account_id).first()
    if not account:
        print("condition 4")
        return Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
    
    # First check that the account is not blacklisted
    account_blacklist = AccountBlacklist.is_email_blacklisted(account.email)
    if account_blacklist:
        print("condition 5")
        return Response({"error": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if the account profile exists
    account_profile = AccountProfile.objects.filter(id=account_profile_id).first()
    if not account_profile:
        print("condition 6")
        return Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the account profile belongs to the account
    if account_profile.account != account:
        print("condition 7")
        print(account_profile.account, account)
        return Response({"error": "FORBIDDEN"}, status=status.HTTP_403_FORBIDDEN)
    
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
        "profile_picture": s3_engine.generate_presigned_s3_url(account_profile.profile_picture_path) if account_profile.profile_picture_path else None,
    }

    return Response(personal_info, status=status.HTTP_200_OK)


def get_main_account_delivery_addresses(account_id: str, account_profile_id: str) -> dict:
    """
    """