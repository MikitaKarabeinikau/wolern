from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
logger = logging.getLogger(__name__)

def create_translation(db: Session, word_id: int, language: str, translation: str) -> models.Translations:
    """Create a new translation for a word."""
    try:
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            raise ValueError(f"Word with id '{word_id}' does not exist.")
        
        existing_translation = db.query(models.Translations).filter(
            models.Translations.word_id == word_id,
            models.Translations.language == language,
            models.Translations.translation == translation
        ).first()
        if existing_translation:
            logger.info(f"Translation already exists for word_id '{word_id}', language '{language}'.")
            return existing_translation
        
        db_translation = models.Translations(
            word_id=word_id,
            language=language,
            translation=translation
        )
        db.add(db_translation)
        db.commit()
        db.refresh(db_translation)
        
        logger.info(f"Successfully created translation for word_id '{word_id}'.")

        return db_translation
    except Exception as e:
        logger.error(f"Error creating translation for word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_translations_by_word_id(db: Session, word_id: int) -> list[models.Translations]:
    """Get all translations for a specific word by its ID."""
    try:
        translations = db.query(models.Translations).filter(models.Translations.word_id == word_id).all()
        logger.info(f"Retrieved {len(translations)} translations for word_id '{word_id}'.")
        return translations
    except Exception as e:
        logger.error(f"Error getting translations for word_id '{word_id}': {e}", exc_info=True)
        raise

def get_translation_by_id(db: Session, id: int) -> models.Translations:
    """Get a translation by its ID."""
    try:
        translation = db.query(models.Translations).filter(models.Translations.id == id).one()
        logger.info(f"Translation with id '{id}' retrieved successfully.")
        return translation
    except NoResultFound:
        logger.warning(f"Translation with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting translation with id '{id}': {e}", exc_info=True)
        raise
    
