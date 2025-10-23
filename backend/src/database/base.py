from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def add_translation_in_base(db: Session, word_id: int, language: str, translation: str):
    """Add a translation for a word in the base words."""
    try:
        db_translation = models.Translation_Base(
            base_id=word_id,
            language=language,
            translation=translation
        )
        db.add(db_translation)
        db.commit()
        logger.info(f"Translation added in base words for word ID '{word_id}': {language} -> {translation}")
    except Exception as e:
        logger.error(f"Error adding translation in base words for word ID '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def add_definition_in_base(db: Session, word_id: int, part_of_speech: str, definition: str):
    """Add a definition for a word in the base words."""
    try:
        db_definition = models.Definition_Base(
            base_id=word_id,
            part_of_speech=part_of_speech,
            definition=definition
        )
        db.add(db_definition)
        db.commit()
        logger.info(f"Definition added in base words for word ID '{word_id}': {part_of_speech} -> {definition}")
    except Exception as e:
        logger.error(f"Error adding definition in base words for word ID '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def add_synonym_in_base(db: Session, word_id: int, synonym: str):
    """Add a synonym for a word in the base words."""
    try:
        db_synonym = models.Synonym_Base(
            base_id=word_id,
            synonym=synonym
        )
        db.add(db_synonym)
        db.commit()
        logger.info(f"Synonym added in base words for word ID '{word_id}': {synonym}")
    except Exception as e:
        logger.error(f"Error adding synonym in base words for word ID '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def add_example_in_base(db: Session, word_id: int, example_sentence: str, part_of_speech: str = None):
    """Add an example sentence for a word in the base words."""
    try:
        db_example = models.Example_Base(
            base_id=word_id,
            example_sentence=example_sentence,
            part_of_speech=part_of_speech
        )
        db.add(db_example)
        db.commit()
        logger.info(f"Example added in base words for word ID '{word_id}': {example_sentence}")
    except Exception as e:
        logger.error(f"Error adding example in base words for word ID '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_last_word_base_id(db: Session):
    """Get the last inserted word base ID."""
    try:
        last_word_base = db.query(models.Word_Base).order_by(models.Word_Base.id.desc()).first()
        if last_word_base:
            logger.info(f"Last word base ID retrieved: {last_word_base.id}")
            return last_word_base.id
        else:
            logger.info("No entries found in word base.")
            return None
    except Exception as e:
        logger.error(f"Error getting last word base ID: {e}", exc_info=True)
        raise

def get_translations_from_base(db: Session, word_id: int):
    """Get translations for a word from the base words."""
    try:
        translations = db.query(models.Translation_Base).filter(models.Translation_Base.base_id == word_id).all()
        logger.info(f"Found {len(translations)} translations in base words for word ID '{word_id}'.")
        return translations
    except Exception as e:
        logger.error(f"Error getting translations for word ID '{word_id}' from base words: {e}", exc_info=True)
        raise

def get_definitions_from_base(db: Session, word_id: int):
    """Get definitions for a word from the base words."""
    try:
        definitions = db.query(models.Definition_Base).filter(models.Definition_Base.base_id == word_id).all()
        logger.info(f"Found {len(definitions)} definitions in base words for word ID '{word_id}'.")
        return definitions
    except Exception as e:
        logger.error(f"Error getting definitions for word ID '{word_id}' from base words: {e}", exc_info=True)
        raise

def get_synonyms_from_base(db: Session, word_id: int):
    """Get synonyms for a word from the base words."""
    try:
        synonyms = db.query(models.Synonym_Base).filter(models.Synonym_Base.base_id == word_id).all()
        logger.info(f"Found {len(synonyms)} synonyms in base words for word ID '{word_id}'.")
        return synonyms
    except Exception as e:
        logger.error(f"Error getting synonyms for word ID '{word_id}' from base words: {e}", exc_info=True)
        raise

def get_examples_from_base(db: Session, word_id: int):
    """Get examples for a word from the base words."""
    try:
        examples = db.query(models.Example_Base).filter(models.Example_Base.base_id == word_id).all()
        logger.info(f"Found {len(examples)} examples in base words for word ID '{word_id}'.")
        return examples
    except Exception as e:
        logger.error(f"Error getting examples for word ID '{word_id}' from base words: {e}", exc_info=True)
        raise

def is_word_in_base(db: Session, word: str):
    """Check if a word exists in the Word_Base table."""
    try:
        logger.info(f"Checking if word '{word}' is in base.")
        result = db.query(models.Word_Base.id).filter(models.Word_Base.word == word.strip()).first()
        logger.info(f"Result for word '{word}': {result}")
        return result is not None
    except Exception as e:
        logger.error(f"Error checking if word '{word}' is in base: {e}", exc_info=True)
        raise

def get_word_base_id(db: Session, word: str):
    """Get the base ID of a word from the base words."""
    try:
        word_base = db.query(models.Word_Base).filter(models.Word_Base.word == word.strip()).first()
        if word_base:
            logger.info(f"Found base ID '{word_base.id}' for word '{word}'.")
            return word_base.id
        else:
            logger.info(f"No base entry found for word '{word}'.")
            return None
    except Exception as e:
        logger.error(f"Error getting base ID for word '{word}': {e}", exc_info=True)
        raise