from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from . import models
import psycopg2
import os
from backend.src.core.word import Word
from datetime import datetime

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__),"../../../.env"))  # Load environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

with engine.connect() as connection:
    print("Succesfully connected to the database!")

    result = connection.execute(text("SELECT version();"))
    print("PostgreSQL version:", result.scalar())

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

def get_user_by_clerk_id(db: Session, clerk_id: str):
    return db.query(models.Users).filter(models.Users.clerk_id == clerk_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def get_user_vocabulary(db: Session, user_id: str):
    return db.query(models.Words).filter(models.Words.added_by_user_id == user_id).all()

def create_user(db: Session, clerk_id: str, username: str = None, email: str = None):
    db_user = models.Users(clerk_id=clerk_id, username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_username(db: Session, clerk_id: int, new_username: str):
    user = get_user_by_id(db, clerk_id)
    if user:
        user.username = new_username
        db.commit()
        db.refresh(user)
    return user

def get_all_words(db: Session, clerk_id: str):
    return db.query(models.Words.word).filter(models.Words.added_by_user_id == clerk_id).all()

#When i will want to add a different translation language i will modify this function
def add_word(db: Session, new_word: dict,clerk_id: str):
    if new_word.get("word") is None:
        raise ValueError("Word is required")
    if new_word in get_all_words(db, clerk_id):
        raise ValueError("Word already exists in the database")
    word_to_add = Word(new_word)
    db_word = models.Words(word=word_to_add.word,
                           added_by_user_id=clerk_id,
                           notes=word_to_add.notes,
                           audio_url=word_to_add.audio_url, 
                           frequency=word_to_add.frequency,
                           difficulty=word_to_add.difficulty)
    
    db.add(db_word)
    
    for lang, translation in word_to_add.translations.items():
        if translation:  # Ensure translation is not empty
            db_translation = models.Translation(word_id=db_word.id,
                                               language=lang,
                                               translation=translation)
            db.add(db_translation)  

    for synonym in word_to_add.synonyms:
        db_synonym = models.Synonym(word_id=db_word.id,
                                    synonym=synonym)
        db.add(db_synonym)

    for part_of_speech,definition in word_to_add.definitions:
        db_definition = models.Definition(word_id=db_word.id,
                                          part_of_speech=part_of_speech,
                                          definition=definition)
        db.add(db_definition)
    
    for part_of_speech, example in word_to_add.examples:
        db_example = models.Example(word_id=db_word.id,
                                    example=example,
                                    part_of_speech=part_of_speech)
        db.add(db_example)

    for tag in word_to_add.tags:
        db_tag = models.Tag(word_id=db_word.id,
                            tag=tag)
        db.add(db_tag)

    for warning in word_to_add.warnings:
        db_warning = models.Warning(word_id=db_word.id,
                                    warning_message=warning)
        db.add(db_warning)
    
    db.commit()
    db.refresh(db_word) 
    

  
     