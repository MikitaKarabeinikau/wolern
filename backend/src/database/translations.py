from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def add_translation(db: Session, word_id: int, language: str, translation: str):
    """Add a new translation."""
    try:
        db_translation = models.Translation(word_id=word_id,
                                            language=language,
                                            translation=translation)
        db.add(db_translation)
        db.commit()
        db.refresh(db_translation)
        logger.info(f"Translation added for word_id '{word_id}' in language '{language}'.")
        return db_translation
    except Exception as e:
        logger.error(f"Error adding translation for word_id '{word_id}' in language '{language}': {e}", exc_info=True)
        db.rollback()
        raise

def get_translations_for_quiz(db: Session, clerk_id: str):
    """Get all translations for quiz words for a specific user."""
    try:
        translations = (
            db.query(models.Translation)
            .join(models.Words)
            .filter(
                models.Words.added_by_user_id == clerk_id,
                (models.Words.vocabulary == "learning") | (models.Words.vocabulary == "new")
            )
            .all()
        )
        if not translations:
            logger.info(f"No translations found for quiz words for user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(translations)} translations for quiz words for user '{clerk_id}'.")
        return translations
    except Exception as e:
        logger.error(f"Error getting translations for quiz words for user '{clerk_id}': {e}", exc_info=True)
        raise

def get_word_translations_from_db(db: Session, word: str, clerk_id: str):
    """Get all translations associated with a word for a specific user."""
    try:
        translations = (
            db.query(models.Translation)
            .join(models.Words)
            .filter(
                models.Words.word == word.strip(),
                models.Words.added_by_user_id == clerk_id,
            )
            .all()
        )
        if not translations:
            logger.info(f"No translations found for word '{word}' and user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(translations)} translations for word '{word}' and user '{clerk_id}'.")
        return translations
    except Exception as e:
        logger.error(
            f"Error getting translations for word '{word}' and user '{clerk_id}': {e}",
            exc_info=True,
        )
        raise

def get_all_translations_for_user_from_db(db: Session, clerk_id: str):
    """Get all translations for a specific user."""
    try:
        translations = (
            db.query(models.Translation)
            .join(models.Words)
            .filter(models.Words.added_by_user_id == clerk_id)
            .all()
        )
        if not translations:
            logger.info(f"No translations found for user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(translations)} translations for user '{clerk_id}'.")
        return translations
    except Exception as e:
        logger.error(f"Error getting translations for user '{clerk_id}': {e}", exc_info=True)
        raise

def get_translation_by_id(db: Session, translation_id: int):
    """Get a translation by its ID."""
    try:
        translation = db.query(models.Translation).filter(models.Translation.id == translation_id).first()
        if not translation:
            logger.info(f"Translation with ID '{translation_id}' not found.")
            return None
        logger.info(f"Translation with ID '{translation_id}' found.")
        return translation
    except Exception as e:
        logger.error(f"Error getting translation with ID '{translation_id}': {e}", exc_info=True)
        raise

def update_translation_by_id(db: Session, translation_id: int, new_translation: str, word_id: int):
    """Update a translation by its ID."""
    try:
        translation_to_update = get_translation_by_id(db, translation_id)
        if not translation_to_update:
            logger.info(f"Translation with ID '{translation_id}' not found.")
            return None

        translation_to_update.translation = new_translation
        translation_to_update.word_id = word_id
        db.commit()
        db.refresh(translation_to_update)
        logger.info(f"Translation with ID '{translation_id}' updated successfully.")
        return translation_to_update
    except Exception as e:
        logger.error(f"Error updating translation with ID '{translation_id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_translation_by_id(db: Session, clerk_id: str, translation_id: int):
    """Delete a translation by its ID, ensuring the user has permission."""
    try:
        to_delete = (
            db.query(models.Translation)
            .join(models.Words)
            .filter(
                models.Translation.id == translation_id,
                models.Words.added_by_user_id == clerk_id,
            )
            .first()
        )
        if not to_delete:
            logger.warning(
                f"Translation with ID '{translation_id}' not found for user '{clerk_id}', or user does not have permission."
            )
            return False
        db.delete(to_delete)
        db.commit()
        logger.info(f"Translation with ID '{translation_id}' deleted successfully by user '{clerk_id}'.")
        return True
    except Exception as e:
        logger.error(
            f"Error deleting translation with ID '{translation_id}' for user '{clerk_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise