from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from . import models


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__),"../../../.env"))  # Load environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


with engine.connect() as connection:
    print("Succesfully connected to the database!")

    result = connection.execute(text("SELECT version();"))
    print("PostgreSQL version:", result.scalar())

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

def get_user_by_clerk_id(db: Session, clerk_user_id: str):
    return db.query(models.Users).filter(models.Users.clerk_user_id == clerk_user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def create_user(db: Session, clerk_user_id: str, username: str, email: str = None):
    db_user = models.Users(clerk_user_id=clerk_user_id, username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user