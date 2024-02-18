from django.core.mail import send_mail

def send_email_activation_link():
    # Registration logic...
    send_mail(
        'Activate your account',
        'Click the link below to activate your account.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )