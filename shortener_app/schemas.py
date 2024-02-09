from pydantic import BaseModel

class URLBase(BaseModel):
    """Contains the target URL field"""
    target_url: str

class URL(URLBase):
    """Enables admin to deactivate shortened urls and
    count the number of clicks"""
    is_active: bool
    clicks: int

    class Config:
        """Allows interaction with db using FastAPI ORM"""
        orm_mode = True

class URLInfo(URL):
    """Defines shortened and admin url fields"""
    url: str
    admin_url: str
