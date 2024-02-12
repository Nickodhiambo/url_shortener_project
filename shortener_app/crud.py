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

def get_db_url_by_secret_key(db: Session, secret_key: str) ->  models.URL:
    """Cheks the database for an active key using secret_key"""
    return(
            db.query(models.URL)
            .filter(models.URL.secret_key == secret_key, models.URL.is_active)
            .first()
            )

def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """
    Increases the number of clicks with every forward to target url"""
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url
