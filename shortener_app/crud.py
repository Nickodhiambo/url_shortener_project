from sqlalchemy.orm import Session
from . import models, keygen, schemas

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    """Generates a shortened URL from target"""
    key = keygen.create_random_key()
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(
            target_url=url.target_url, key=key, secret_key=secret_key
            )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    """Checks if a generated key exists in the database"""
    return (
            db.query(models.URL)
            .filter(models.URL.key == url_key, models.URL.is_active)
            .first()
            )
