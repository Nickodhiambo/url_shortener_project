import string
import secrets

def create_random_key(length: int = 5) -> str:
    """Generates a random key of 5 chars by default"""
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))
