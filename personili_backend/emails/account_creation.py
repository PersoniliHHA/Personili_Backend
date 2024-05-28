from django.core.mail import send_mail
from emails.brevo_engine import brevo_engine

def send_email_activation_link( email_to_activate, activation_link, template_name= "email_verification_en", first_name = None, last_name = None):
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
