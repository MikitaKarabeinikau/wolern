from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
logger = logging.getLogger(__name__)


def create_user_translation(db:Session, user_word_status_id:int,language: str, translation:str) -> models.UserTranslations:
    """Create a new UserTranslations entry for a given UserWordStatus ID."""
    try:
        word_status = db.query(models.UserWordStatus).filter(models.UserWordStatus.id == user_word_status_id).first()
        if not word_status:
            raise ValueError(f"UserWordStatus with id '{user_word_status_id}' does not exist.")
        
        existing_translation = db.query(models.UserTranslations).filter(
                models.UserTranslations.user_word_status_id == user_word_status_id,
                models.UserTranslations.language == language,
                models.UserTranslations.translation == translation
            ).first()     
        if existing_translation:
            logger.warning(f"User translation for UserWordStatus ID '{user_word_status_id}' already exists.")
            return existing_translation
        new_translation = models.UserTranslations(
            user_word_status_id=user_word_status_id,
            language=language,
            translation=translation
        )
        db.add(new_translation)
        db.commit()
        db.refresh(new_translation)
        return new_translation
    except Exception as e:
        logger.error(f"Error creating UserTranslations for UserWordStatus ID '{user_word_status_id}': {e}", exc_info=True)
        db.rollback()
        raise
    
def get_user_translations(db:Session, user_word_status_id:int) -> list[models.UserTranslations]:
    """Retrieve UserTranslations by UserWordStatus ID."""
    try:
        translations = db.query(models.UserTranslations).filter(models.UserTranslations.user_word_status_id == user_word_status_id).all()
        return translations
    except Exception as e:
        logger.error(f"Error retrieving UserTranslations for UserWordStatus ID '{user_word_status_id}': {e}", exc_info=True)
        raise

def get_user_translation_by_word_id(db:Session, user_word_status_id:int) -> models.UserTranslations:
    """Retrieve a UserTranslations by UserWordStatus ID."""
    try:
        translation = db.query(models.UserTranslations).filter(models.UserTranslations.user_word_status_id == user_word_status_id).one()
        return translation
    except NoResultFound:
        logger.warning(f"User translation for UserWordStatus ID '{user_word_status_id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving UserTranslations for UserWordStatus ID '{user_word_status_id}': {e}", exc_info=True)
        raise

def update_user_translation(db:Session, user_translation_id:int, new_translation:str) -> models.UserTranslations:
    """Update an existing UserTranslations entry."""
    try:
        translation_entry = db.query(models.UserTranslations).filter(models.UserTranslations.id == user_translation_id).one()
        translation_entry.translation = new_translation
        db.commit()
        db.refresh(translation_entry)
        return translation_entry
    except NoResultFound:
        logger.warning(f"User translation with id '{user_translation_id}' not found for update.")
        db.rollback()
        return None
    except Exception as e:
        logger.error(f"Error updating UserTranslations with id '{user_translation_id}': {e}", exc_info=True)
        db.rollback()
        raise
    
def delete_user_translation(db:Session, user_translation_id:int) -> bool:
    """Delete UserTranslations by its ID."""
    try:
        translation_entry = db.query(models.UserTranslations).filter(models.UserTranslations.id == user_translation_id).one()
        db.delete(translation_entry)
        db.commit()
        return True
    except NoResultFound:
        logger.warning(f"User translation with id '{user_translation_id}' not found for deletion.")
        db.rollback()
        return False
    except Exception as e:
        logger.error(f"Error deleting UserTranslations with id '{user_translation_id}': {e}", exc_info=True)
        db.rollback()
        raise