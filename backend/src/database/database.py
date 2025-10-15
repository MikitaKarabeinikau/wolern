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
    return db.query(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()


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
                                        example_sentence=ex)
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
     
    

def delete_word(db: Session, word: str, clerk_id: str):
    word_entry = db.query(models.Words).filter(models.Words.word == word.strip(), models.Words.added_by_user_id == clerk_id).first()
    if word_entry:
        db.delete(word_entry)
        db.commit()
        return True
    return False

def get_word_translations_from_db(db: Session, word: str, clerk_id: str):
    data =  db.query(models.Words).join(models.Translation).filter(models.Words.word == word.strip(), models.Words.added_by_user_id == clerk_id).all()
    print("\n\nRaw translation data from DB:", data)  # Debug log
    print(f'fetching translations for word {data}')
    return data

def get_word_synonyms_from_db(db: Session, word: str, clerk_id: str):
    return db.query(models.Words).join(models.Synonym).filter(models.Words.word == word.strip(), models.Words.added_by_user_id == clerk_id).all()

def get_word_tags_from_db(db: Session, word: str, clerk_id: str):
    return db.query(models.Words).join(models.Tag).filter(models.Words.word == word.strip(), models.Words.added_by_user_id == clerk_id).all()

def get_word_warnings_from_db(db: Session, word: str, clerk_id: str):
    return db.query(models.Words).join(models.Warning).filter(models.Words.word == word.strip(), models.Words.added_by_user_id == clerk_id).all()

def get_word_part_of_speech_from_db(db: Session, word: str, clerk_id: str):
    return db.query(models.Words).join(models.Definition.part_of_speech).filter(models.Words.word == word.strip(), models.Words.added_by_user_id == clerk_id).all()

def get_all_translations_for_user_from_db(db: Session, clerk_id: str):
    return db.query(models.Translation).join(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()

def get_all_definitions_for_user_from_db(db: Session, clerk_id: str):
    return db.query(models.Definition).join(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()   

def get_all_examples_for_user_from_db(db: Session, clerk_id: str):
    return db.query(models.Example).join(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()

def get_all_synonyms_for_user_from_db(db: Session, clerk_id: str):
    return db.query(models.Synonym).join(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()

def get_all_tags_for_user_from_db(db: Session, clerk_id: str):
    return db.query(models.Tag).join(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()

def get_all_warnings_for_user_from_db(db: Session, clerk_id: str):
    return db.query(models.Warning).join(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()

def delete_definition_by_id(db: Session,clerk_id:str, definition_id: int):
    to_delete = db.query(models.Definition).join(models.Words).filter(models.Definition.id == definition_id, models.Words.added_by_user_id == clerk_id).first()
    if not to_delete:
        print("No definition found or user does not have permission to delete it.")
        return None
    db.delete(to_delete)
    db.commit()
    print("Definition deleted successfully.")
    return True  # Indicate successful deletion

def get_definition_by_id(db: Session, definition_id: int):
    return db.query(models.Definition).filter(models.Definition.id == definition_id).first()

def update_definition_by_id(db: Session, definition_id: int, new_definition: str):
    definition_entry = get_definition_by_id(db, definition_id)
    if definition_entry:
        definition_entry.definition = new_definition
        db.commit()
        db.refresh(definition_entry)
        return definition_entry
    return None
