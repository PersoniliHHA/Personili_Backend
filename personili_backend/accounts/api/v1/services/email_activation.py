
from security.secure_tokens import generate_random_token
from emails.brevo_engine import brevo_engine
from config import settings
import os
from accounts.models import ActionToken


def verify_email_verification_token(token: str) -> bool:
    """
    Verify that the token is valid
    """
    return ActionToken.verify_token(token)


def generate_email_activation_link(domain: str, token_size: int, api_version: str = "v1") -> str:
    """
    Generate an email activation link.
    :param domain: The domain of the link.
    :return: The generated email activation link.
    """
    token = generate_random_token(size=token_size , signed=False)
    return f"{domain}/api/accounts/{api_version}/accounts/activate/{token}"


def send_email_activation_link(email_to_activate: str,
                               token_size: int = 32,
                               api_version: str = "v1", 
                               template_name: str= "email_verification_en", 
                               first_name: str = None, 
                               last_name: str = None):
    
    # Get the domain name from env variables
    domain: str = os.getenv("DOMAIN_NAME", "localhost")

    # Generate the activation link
    activation_link: str = generate_email_activation_link(
        domain=domain,
        api_version=api_version,
        token_size=token_size)

    placeholders: dict[str, str] = {
        "first_name": first_name,
        "last_name": last_name,
        "activation_link": activation_link
    }

    brevo_engine.send_email(
        to_email=email_to_activate,
        subject="Activate your Personili account",
        template_name=template_name,
        placeholders=placeholders
    )

