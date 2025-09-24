from sqlalchemy import Integer, String, Column, DateTime, create_engine,text
# Importing declarative_base to define the base class for our models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .database import engine

Base = declarative_base()



#TODO: Add more fields as necessary
#Create schema for words table
# Define the Words model
class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, index=True, nullable=False)
    added_by_user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Translations(Base):
    __tablename__ = "translations"

    pass

class Definitions(Base):
    __tablename__ = "definitions"

    pass

class Examples(Base):
    __tablename__ = "examples"

    pass

class Levels(Base):
    __tablename__ = "levels"

    pass

class Tags(Base):
    __tablename__ = "tags"

    pass

class Warnings(Base):
    __tablename__ = "warnings"

    pass

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()