from django.core.mail import send_mail
from emails.brevo_engine import brevo_engine

def send_email_activation_link():
    brevo_engine.send_email()
