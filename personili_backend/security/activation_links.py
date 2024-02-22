import secrets

def generate_activation_link():
    token = secrets.token_urlsafe(32)
    activation_link = f"https://example.com/activate?token={token}"
    return activation_link
