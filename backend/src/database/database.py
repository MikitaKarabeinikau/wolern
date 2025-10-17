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
     
def delete_word_by_id_from_db(db: Session, word_id: int, clerk_id: str):
    print(f"Attempting to delete word with ID {word_id} for user {clerk_id}")
    word_to_delete = db.query(models.Words).filter(models.Words.id == word_id, models.Words.added_by_user_id == clerk_id).first()
    print("Word to delete:", clerk_id)
    if word_to_delete: 
        # Delete dependent rows explicitly to avoid nulling non-null FK columns
            db.query(models.Translation).filter(models.Translation.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Synonym).filter(models.Synonym.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Definition).filter(models.Definition.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Example).filter(models.Example.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Tag).filter(models.Tag.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Warning).filter(models.Warning.word_id == word_id).delete(synchronize_session=False)

            db.delete(word_to_delete)
            db.commit()
            print(f"Word with ID {word_id} deleted successfully.")
            return True
    return False

def delete_word(db: Session, word: str, clerk_id: str):
    word_entry = get_word_by_id(db, word, clerk_id)
    if word_entry:
        db.delete(word_entry)
        db.commit()
        return True
    return False

def get_word_by_id(db: Session, word_or_id: str, clerk_id: str):
    """
    Accept either a numeric id or a word string.
    - If int: lookup by id.
    - Otherwise: lookup by word text.
    """
    try:
        if isinstance(word_or_id, int):
            return db.query(models.Words).filter(models.Words.id == word_or_id, models.Words.added_by_user_id == clerk_id).first()
        # handle numeric strings too
        if isinstance(word_or_id, str) and word_or_id.isdigit():
            return db.query(models.Words).filter(models.Words.id == int(word_or_id), models.Words.added_by_user_id == clerk_id).first()
        return db.query(models.Words).filter(models.Words.word == word_or_id.strip(), models.Words.added_by_user_id == clerk_id).first()
    except Exception:
        return None
    
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
    definition_to_update = get_definition_by_id(db, definition_id)
    if definition_to_update:
        definition_to_update.definition = new_definition
        db.commit()
        db.refresh(definition_to_update)
        return definition_to_update
    return None

def delete_example_by_id(db: Session, clerk_id: str, example_id: int):
    to_delete = db.query(models.Example).join(models.Words).filter(models.Example.id == example_id, models.Words.added_by_user_id == clerk_id).first()
    if not to_delete:
        print("No example found or user does not have permission to delete it.")
        return None
    db.delete(to_delete)
    db.commit()
    print("Example deleted successfully.")
    return True  # Indicate successful deletion

def get_example_by_id(db: Session, example_id: int):
    return db.query(models.Example).filter(models.Example.id == example_id).first()

def update_example_by_id(db: Session, example_id: int, new_example: str, word_id: int):
    example_to_update = get_example_by_id(db, example_id)
    if example_to_update:
        example_to_update.example_sentence = new_example
        example_to_update.word_id = word_id
        db.commit()
        db.refresh(example_to_update)
        return example_to_update
    return None


def delete_translation_by_id(db: Session, clerk_id: str, translation_id: int):
    to_delete = db.query(models.Translation).join(models.Words).filter(models.Translation.id == translation_id, models.Words.added_by_user_id == clerk_id).first()
    if not to_delete:
        print("No translation found or user does not have permission to delete it.")
        return None
    db.delete(to_delete)
    db.commit()
    print("Translation deleted successfully.")
    return True  # Indicate successful deletion

def get_translation_by_id(db: Session, translation_id: int):
    return db.query(models.Translation).filter(models.Translation.id == translation_id).first()

def update_translation_by_id(db: Session, translation_id: int, new_translation: str, word_id: int):
    translation_to_update = get_translation_by_id(db, translation_id)
    if translation_to_update:
        translation_to_update.translation = new_translation
        translation_to_update.word_id = word_id
        db.commit()
        db.refresh(translation_to_update)
        return translation_to_update
    return None

def delete_tags_by_id(db: Session, clerk_id: str, tag_id: int):
    to_delete = db.query(models.Tag).join(models.Words).filter(models.Tag.id == tag_id, models.Words.added_by_user_id == clerk_id).first()
    if not to_delete:
        print("No tag found or user does not have permission to delete it.")
        return None
    db.delete(to_delete)
    db.commit()
    print("Tag deleted successfully.")
    return True  # Indicate successful deletion

def get_tag_by_id(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def update_tag_by_id(db: Session, tag_id: int, new_tag: str, word_id: int):
    tag_to_update = get_tag_by_id(db, tag_id)
    if tag_to_update:
        tag_to_update.tag = new_tag
        tag_to_update.word_id = word_id
        db.commit()
        db.refresh(tag_to_update)
        return tag_to_update
    return None

def delete_synonym_by_id(db: Session, clerk_id: str, synonym_id: int):
    to_delete = db.query(models.Synonym).join(models.Words).filter(models.Synonym.id == synonym_id, models.Words.added_by_user_id == clerk_id).first()
    if not to_delete:
        print("No synonym found or user does not have permission to delete it.")
        return None
    db.delete(to_delete)
    db.commit()
    print("Synonym deleted successfully.")
    return True  # Indicate successful deletion

def get_synonym_by_id(db: Session, synonym_id: int):
    return db.query(models.Synonym).filter(models.Synonym.id == synonym_id).first()

def update_synonym_by_id(db: Session, synonym_id: int, new_synonym: str, word_id: int):
    synonym_to_update = get_synonym_by_id(db, synonym_id)
    if synonym_to_update:
        synonym_to_update.synonym = new_synonym
        synonym_to_update.word_id = word_id
        db.commit()
        db.refresh(synonym_to_update)
        return synonym_to_update
    return None

def delete_warning_by_id(db: Session, clerk_id: str, warning_id: int):
    to_delete = db.query(models.Warning).join(models.Words).filter(models.Warning.id == warning_id, models.Words.added_by_user_id == clerk_id).first()
    if not to_delete:
        print("No warning found or user does not have permission to delete it.")
        return None
    db.delete(to_delete)
    db.commit()
    print("Warning deleted successfully.")
    return True  # Indicate successful deletion

def get_warning_by_id(db: Session, warning_id: int):
    return db.query(models.Warning).filter(models.Warning.id == warning_id).first()

def update_warning_by_id(db: Session, warning_id: int, new_warning: str, word_id: int):
    warning_to_update = get_warning_by_id(db, warning_id)
    if warning_to_update:
        warning_to_update.warning_message = new_warning
        warning_to_update.word_id = word_id
        db.commit()
        db.refresh(warning_to_update)
        return warning_to_update
    return None

def add_synonym(db: Session, word_id: int, synonym: str):
    db_synonym = models.Synonym(word_id=word_id, synonym=synonym)
    db.add(db_synonym)
    db.commit()
    db.refresh(db_synonym)
    return db_synonym
