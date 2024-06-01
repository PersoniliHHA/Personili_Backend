from accounts.models import ActionToken, Account
from datetime import datetime, timedelta, timezone


def have_action_token(token: str, type: str, email: str) -> bool:
    """
    Check if a user with given email has a token of given type, use the email
    to get the user account and pass it to the action token method
    """
    return ActionToken.objects.filter(
        account=Account.objects.get(email=email), token=token, type=type
    ).exists()
    