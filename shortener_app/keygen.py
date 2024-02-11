import string
import secrets

from . import crud

def create_random_key(length: int = 5) -> str:
    """Generates a random key of 5 chars by default"""
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_key(db) -> str:
    """Genetates a unique shortened URL"""
    key = create_random_key()
    while (crud.get_db_url_by_key(db, key)):
        key = create_random_key()
    return key

