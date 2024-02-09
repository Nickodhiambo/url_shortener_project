import secrets

import validators
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    """Landing page for URL Shortener app"""
    return "Welcome to URL Shortener App :)"

def raise_bad_request(message):
    """Raises exception if url provided is invalid"""
    raise HTTPException(status_code=400, detail=message)

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """Sends a post request with tartet url"""
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = "".join(secrets.choice(chars) for _ in range(5))
        secret_key = "".join(secrets.choice(chars) for _ in range(8))
        db_url = models.URL(
            target_url=url.target_url, key=key, secret_key=secret_key
            )
        
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        db_url.url = key
        db_url.admin_url = secret_key

        return db_url
