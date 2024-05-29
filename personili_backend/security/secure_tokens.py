import secrets
import hmac

def generate_random_token(size: int, signed: bool = False) -> str:
    """
    Generate a random token of the given size.
    :param size: The size of the token.
    :param signed: Whether to sign the token.
    :return: The generated token.
    """
    token = secrets.token_urlsafe(size)
    if signed:
        # Sign the token using hmac, the token must be returned
        token = token.encode('utf-8')
        signature = hmac.new(token, digestmod='sha256').hexdigest
        token = f"{token}.{signature}"
    
    return token

def verify_token(token: str) -> bool: 
    """
    Verify the token.
    :param token: The token to verify.
    :return: True if the token is valid, False otherwise.
    """
    if '.' in token:
        token, signature = token.split('.')
        token = token.encode('utf-8')
        signature = signature.encode('utf-8')
        return hmac.compare_digest(hmac.new(token, digestmod='sha256').hexdigest, signature)
    return False


