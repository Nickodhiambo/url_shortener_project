import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine

from starlette.datastructures import URL
from .config import get_settings

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

def raise_not_found(request):
    """Checks if a shortened url exists in the db"""
    message = f"URL {request.url} does not exist"
    raise HTTPException(status_code=404, detail=message)

@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
        ):
    """Redirects shortened URL requests to the real URL"""
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """Sends a post request with target url"""
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    
    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)

@app.get(
        "/admin/{secret_key}",
        name="admin info",
        response_model=schemas.URLInfo
        )
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    """Sends a get request to admin endpoint with secret_key as param"""
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """Concatenates the returned shortened and admin keys
    to base URL
    """
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
            "admin info", secret_key=db_url.secret_key
            )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

@app.delete("/admin/{secret_key}")
def delete_url(
        secret_key: str,
        request: Request,
        db: Session = Depends(get_db)
        ):
    """An endpoint to deactivate a shortened URL
    by its secret key"""
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deactivated shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)

