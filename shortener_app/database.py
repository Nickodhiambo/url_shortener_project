from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

# Define entry point to database
engine = create_engine(
        get_settings().db_url, connect_args={"check_same_thread": False}
        )

# Initialize a CRUD session
SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
        )

# Links the ORM to db tables
Base = declarative_base()
