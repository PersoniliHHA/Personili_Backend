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
        return (Response({"error": "FORBIDDEN"}, status=status.HTTP_403_FORBIDDEN), False)
    
    return ((account, account_profile), True)
################## Delivery address verification ############################
def verify_delivery_address_and_profile(account_profile: AccountProfile, delivery_address_id: str, action: str) -> Union[Tuple[DeliveryAddress, bool], Tuple[Response, bool]]:    
    """
    - if the action is create, then we should verify that the delivery address does not exist with the same values and that
    the delivery address does not exceed the maximum limit (3 addresses per account profile)
    - if the action is delete, then we should verify the delivery address exists and the delivery address belongs to the account profile
    - if the action is update, then we should verify the delivery address exists and the delivery address belongs to the account profile
    """
    if action == "create":
        # Check if the delivery address already exists
        delivery_address = DeliveryAddress.objects.filter(
            account_profile=account_profile,
            street=delivery_address_id["street"],
            city=delivery_address_id["city"],
            zip_code=delivery_address_id["zip_code"],
            country=delivery_address_id["country"],
            state=delivery_address_id["state"]
        ).first()
        if delivery_address:
            return (Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST), False)
        
        # Check if the account profile has reached the maximum limit of delivery addresses
        delivery_addresses_count = DeliveryAddress.objects.filter(account_profile=account_profile).count()
        if delivery_addresses_count >= 3:
            return (Response({"error": "MAXIMUM_NUMBER_REACHED"}, status=status.HTTP_400_BAD_REQUEST), False)
        
        return (None, True)
    elif action == "delete" or action == "update":
        # Check if the delivery address exists
        delivery_address = DeliveryAddress.objects.filter(id=delivery_address_id).first()
        if not delivery_address:
            return (Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST), False)
        
        # Check if the delivery address belongs to the account profile
        if delivery_address.account_profile != account_profile:
            return (Response({"error": "FORBIDDEN"}, status=status.HTTP_403_FORBIDDEN), False)
        
        return (delivery_address, True)
    

###################### Personal infos ###################################################
########## Personal infos GET
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
        "profile_id": account_profile.id,
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

########## Personal infos UPDATE

def update_main_account_personal_information(account_id: str, account_profile_id: str, updated_personal_info: dict) -> Response:
    """
    This allows the user to update their personal info, including :
    - the profile picture
    - the biography
    - the social media links
    - the phone number
    """
    # Verify the account and account profile
    response, success = verify_account_and_account_profile(account_id, account_profile_id)
    if not success:
        return response
    
    account_profile = response[1]
    account = response[0]

    # Update the personal information
    account_profile.biography = updated_personal_info.get("biography")
    account_profile.social_media_links = updated_personal_info.get("social_media_links")
    account_profile.phone_number = updated_personal_info.get("phone_number")
    # First delete the old profile picture
    if account_profile.profile_picture_path:
        s3_engine.delete_file_from_s3(account_profile.profile_picture_path)
    # Upload the new profile picture
    if updated_personal_info.get("profile_picture"):
        account_profile.profile_picture_path = s3_engine.upload_file_to_s3(updated_personal_info.get("profile_picture"), "regular_user_profile", {"regular_user_profile_id": account.id, "regular_user_email": account_profile.id})
    account_profile.save()

    return Response({"message": "Personal information updated successfully"}, status=status.HTTP_200_OK)


################################## Delivery addresses ########################################
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


def create_new_delivery_address(account_id: str, account_profile_id: str, address: dict) -> Response:
    """
    This method will create a new delivery address for the main account
    """
    # Verify the account and account profile
    response, success = verify_account_and_account_profile(account_id, account_profile_id)
    if not success:
        return response
    
    account_profile = response[1]
    account = response[0]

    # Verify the delivery address
    response, success = verify_delivery_address_and_profile(account_profile, address, "create")
    if not success:
        return response
    
    # Create the delivery address
    new_delivery_address = DeliveryAddress(
        account_profile=account_profile,
        street=address.get("street"),
        city=address.get("city"),
        zip_code=address.get("zip_code"),
        state=address.get("state"),
        country=address.get("country"),
    )
    new_delivery_address.save()

    return Response({"message": "Delivery address created successfully"}, status=status.HTTP_201_CREATED)

def update_existing_delivery_address(account_id: str, account_profile_id: str, delivery_address_id: str, address: dict) -> Response:
    """
    This method will update an existing delivery address for the main account
    """
    # Verify the account and account profile
    response, success = verify_account_and_account_profile(account_id, account_profile_id)
    if not success:
        return response
    
    account_profile = response[1]
    account = response[0]

    # Verify the delivery address
    response, success = verify_delivery_address_and_profile(account_profile, delivery_address_id, "update")
    if not success:
        return response
    
    delivery_address = response

    # Update the delivery address only if the new date is not null
    delivery_address.street = address.get("street") if address.get("street") else delivery_address.street
    delivery_address.city = address.get("city") if address.get("city") else delivery_address.city
    delivery_address.zip_code = address.get("zip_code") if address.get("zip_code") else delivery_address.zip_code
    delivery_address.state = address.get("state") if address.get("state") else delivery_address.state
    delivery_address.country = address.get("country") if address.get("country") else delivery_address.country
    delivery_address.default_delivery_address = address.get("default_delivery_address") if address.get("default_delivery_address") else delivery_address.default_delivery_address
    delivery_address.save()

    # Return the newly updated delivery address
    updated_delivery_address: dict = {
        "delivery_address_id": delivery_address.id,
        "street": delivery_address.street,
        "city": delivery_address.city,
        "zip_code": delivery_address.zip_code,
        "state": delivery_address.state,
        "country": delivery_address.country,
    }

    return Response(updated_delivery_address, status=status.HTTP_200_OK)


def delete_existing_delivery_address(account_id: str, account_profile_id: str, delivery_address_id: str) -> Response:
    """
    This method will delete an existing delivery address for the main account
    """
    # Verify the account and account profile
    response, success = verify_account_and_account_profile(account_id, account_profile_id)
    if not success:
        return response
    
    account_profile = response[1]
    account = response[0]

    # Verify the delivery address
    response, success = verify_delivery_address_and_profile(account_profile, delivery_address_id, "delete")
    if not success:
        return response
    
    delivery_address = response

    # Delete the delivery address
    delivery_address.delete()

    return Response({"message": "Delivery address deleted successfully"}, status=status.HTTP_200_OK)