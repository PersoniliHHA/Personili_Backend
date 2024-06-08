
from security.secure_tokens import generate_random_token
from emails.brevo_engine import brevo_engine
from config import settings
import os
from datetime import datetime, timedelta, UTC
from accounts.models import ActionToken, Account


def verify_email_verification_token(token: str, type: str) -> bool:
    """
    Verify that the token is valid
    """
    return ActionToken.verify_token(token, type)


def generate_email_activation_link(account_id: str, domain: str, token_size: int, api_version: str = "v1") -> str:
    """
    Generate an email activation link.
    :param domain: The domain of the link.
    :return: The generated email activation link.
    """
    # Generate the token
    token: str = generate_random_token(size=token_size , signed=False)

    # Save the token
    expiry_date = datetime.now(UTC) + timedelta(days=1)
    ActionToken.create_new_token(token=token, account_id=account_id, token_type = "EMAIL_VERIFICATION", expiry_date=expiry_date)
    
    return f"{domain}/api/accounts/{api_version}/accounts/verify-email/{token}/"


def send_email_activation_link(email_to_activate: str,
                               account_id: str,
                               token_size: int = 32,
                               api_version: str = "v1", 
                               template_name: str= "email_verification_en", 
                               first_name: str = None, 
                               last_name: str = None):
    
    # Get the domain name from env variables
    domain: str = os.getenv("DOMAIN_NAME", "http://localhost:5000")

    # Generate the activation link
    activation_link: str = generate_email_activation_link(
        account_id = account_id,
        domain=domain,
        api_version=api_version,
        token_size=token_size)

    placeholders: dict[str, str] = {
        "first_name": first_name,
        "last_name": last_name,
        "activation_link": activation_link
    }

    print("activation link: ", activation_link)

    # Send the email
    brevo_engine.send_email(
        to_email=email_to_activate,
        subject="Activate your Personili account",
        template_name=template_name,
        placeholders=placeholders
    )


def verify_account_email(account_id: str) -> None:
    """
    Verify the email of an account
    """
    Account.verify_email(account_id)