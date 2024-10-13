# Validators
from security.secure_tokens import generate_random_token
from emails.brevo_engine import brevo_engine

from rest_framework.response import Response
from rest_framework import status

# Standard imports
import os
from datetime import datetime, timedelta, UTC

# Models imports
from accounts.models import ActionToken, Account, AccountBlacklist

# Validators
from utils.validators import validate_email

# Scenario:
# The user wants to reset their password
# The system must generate a password reset link
# The system must send the password reset link to the user
# The system must verify the password reset token


def verify_password_reset_token(token: str, type: str) -> bool:
    """
    Verify that the token is valid
    """
    return ActionToken.verify_token(token, type)


def generate_password_reset_link(account_id: str, domain: str, token_size: int, api_version: str = "v1") -> bool:
    """
    Generate a password reset link.
    :param domain: The domain of the link.
    :return: The generated password reset link.
    """

    # Generate the token
    token: str = generate_random_token(size=token_size, signed=False)

    # Save the token
    expiry_date = datetime.now(UTC) + timedelta(days=1)
    ActionToken.create_new_token(token=token, account_id=account_id, token_type="PASSWORD_RESET", expiry_date=expiry_date)

    return f"{domain}/api/accounts/{api_version}/accounts/reset-password/{token}/"


def send_password_reset_email_link(email: str,
                                   token_size: int = 32,
                                   api_version: str = "v1",
                                   template_name: str = "fancy_password_reset_en",
                                   first_name: str = None,
                                   last_name: str = None):

     ##################### Email and account Verification ###########################
    # Check if the email is valid
    if not email or not validate_email(email):
        return False, "INVALID_EMAIL"
    
    # Check if an account with this email exists
    if not Account.objects.filter(email=email).exists():
        return False, "ACCOUNT_NOT_FOUND"
    # Check if the email is blacklisted or suspended
    if AccountBlacklist.is_email_blacklisted(email):
        return False, "EMAIL_BLACKLISTED"
    
    # Check if the email is verified
    if not Account.objects.filter(email=email).first().email_verified:
        return False, "EMAIL_NOT_VERIFIED"
    
    # Get the account id
    account_id = Account.objects.filter(email=email).first().id

    # Get the domain name from env variables
    domain: str = os.getenv("DOMAIN_NAME", "http://localhost:5000")

    # Generate the activation link
    activation_link: str = generate_password_reset_link(
        account_id=account_id,
        domain=domain,
        api_version=api_version,
        token_size=token_size)

    placeholders: dict[str, str] = {
        "first_name": first_name,
        "last_name": last_name,
        "activation_link": activation_link
    }

    # Send the email
    brevo_engine.send_email(
        to_email=email,
        subject="Reset your Personili account password",
        template_name=template_name,
        placeholders=placeholders
    )

    return True, "EMAIL_SENT"
