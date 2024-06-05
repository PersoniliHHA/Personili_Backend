# Models
from accounts.models import AccountProfile, Account, AccountBlacklist

# rest framework imports
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

def get_main_account_personal_information(account_id: str, account_profile_id: str):
    """
    """
    # Validate the parameters
    if not account_id or not account_profile_id:
        return Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the account exists
    account = Account.objects.filter(id=account_id).first()
    if not account:
        return Response({"error": "BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
    
    # First check that the account is not blacklisted
    account_blacklist = AccountBlacklist.is_email_blacklisted(account.email)
    if account_blacklist:
        return Response({"error": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if the account is active