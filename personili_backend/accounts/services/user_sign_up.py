# Models
from accounts.models import Account, AccountProfile

# Utils
from utils.aws.storage.s3_engine import s3_engine

# Security
from security.jwt import create_access_token, create_refresh_token

def create_main_account_sign_up_response(account: Account, AccountProfile: AccountProfile) -> dict:
   """
   Build the json response for the main account sign up
   """
   return {
         'id': account.id,
         'email': account.email,
         'first_name': AccountProfile.first_name,
         'last_name': AccountProfile.last_name,
         'phone_number': AccountProfile.phone_number,
         'age': AccountProfile.age,
         'gender': AccountProfile.gender,
         'profile_picture_url': s3_engine.generate_presigned_s3_url(AccountProfile.profile_picture_path),
         'access_token': create_access_token(str(account.id)),
         'refresh_token': create_refresh_token(str(account.id))
    }