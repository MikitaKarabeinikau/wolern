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

def get_all_words_from_db(db: Session, clerk_id: str):
    words  = db.query(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()
    print(words)
    word_list = [
        {
            "id": word.id,
            "word": word.word
        }
        for word in words
    ]
    
    print(f'Words after processing: {word_list} ')
    return word_list

def get_word_id_by_word(db: Session, word: str):
    word_entry = db.query(models.Words.id).filter(models.Words.word == word.strip()).first()
    return word_entry.id if word_entry else None

#When i will want to add a different translation language i will modify this function
def add_word(db: Session, word: Word, clerk_id: str):
    if word is None:
        raise ValueError("Word is required")
    if word.word in get_all_words_from_db(db, clerk_id):
        raise ValueError("Word already exists in the database")
    print("Word object created:", word)
    db_word = models.Words(word=word.word,
                           added_by_user_id=clerk_id,
                           frequency=word.frequency,
                           difficulty=word.difficulty)
    
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    print("Word added to database:", db_word.word)
    word_id = get_word_id_by_word(db, word.word)
    
    for lang, translation in word.translation.items():
        if translation:  # Ensure translation is not empty
            for t in word.translation[lang]:
                print ("Adding translation:", t, "for language:", lang)
                db_translation = models.Translation(word_id=db_word.id,
                                                language=lang,
                                                translation=t)
                db.add(db_translation)  

    for synonym in word.synonyms:
        print("Adding synonym:", synonym)
        db_synonym = models.Synonym(word_id=db_word.id,
                                    synonym=synonym)
        db.add(db_synonym)
        
    print("Definitions to add:", word.definition)
    for part_of_speech, definitions in word.definition.items():
        for definition in definitions:
            print("Adding definition:", definition, "for part of speech:", part_of_speech)
            db_definition = models.Definition(word_id=db_word.id,
                                            part_of_speech=part_of_speech,
                                            definition=definition)
            db.add(db_definition)

    print("Examples to add:", word.examples)
    for part_of_speech,example in word.examples.items():
        for ex in example:
            print("Adding example:", ex, "for part of speech:", part_of_speech)
            db_example = models.Example(word_id=db_word.id,
                                        part_of_speech=part_of_speech,
                                        example=ex)
            db.add(db_example)

    for tag in word.tags:
        if len(tag) == 0 :
            break
        print("Adding tag:", tag)
        db_tag = models.Tag(word_id=db_word.id,
                            tag=tag)
        db.add(db_tag)

    for warning in word.warnings:
        if len(warning) == 0 :
            break
        print("Adding warning:", warning)
        db_warning = models.Warning(word_id=db_word.id,
                                    warning_message=warning)
        db.add(db_warning)
    
    db.commit()
     
    
    def get_word_translations(db: Session, word: int):
        return db.query(models.Translation).filter(models.Translation.word == word.strip()).all()

  
     