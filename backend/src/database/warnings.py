from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def create_warning(db: Session, word_id: int, warning_text: str):
    """Create a new warning."""
    try:
        db_warning = models.Warning(word_id=word_id, warning_message=warning_text)
        db.add(db_warning)
        db.commit()
        db.refresh(db_warning)
        logger.info(f"Warning created for word_id '{word_id}'.")
        return db_warning
    except Exception as e:
        logger.error(f"Error creating warning for word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_number_of_warnings_for_word(db: Session, word_id: int):
    """Get the number of warnings associated with a specific word."""
    try:
        count = db.query(models.Warning).filter(models.Warning.word_id == word_id).count()
        logger.info(f"Number of warnings for word_id '{word_id}': {count}")
        return count
    except Exception as e:
        logger.error(f"Error getting number of warnings for word_id '{word_id}': {e}", exc_info=True)
        raise

def get_word_warnings_from_db(db: Session, word: str, clerk_id: str):
    """Get all warnings associated with a word for a specific user."""
    try:
        warnings = db.query(models.Warning).join(models.Words).filter(models.Words.word == word.strip(), models.Words.added_by_user_id == clerk_id).all()
        return warnings
    except Exception as e:
        logger.error(f"Error getting warnings for word '{word}' and clerk_id {clerk_id}: {e}", exc_info=True)
        raise

def get_all_warnings_for_user_from_db(db: Session, clerk_id: str):
    """Get all warnings for a specific user."""
    try:
        warnings = db.query(models.Warning).join(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()
        return warnings
    except Exception as e:
        logger.error(f"Error getting all warnings for user with clerk_id {clerk_id}: {e}", exc_info=True)
        raise

def get_warning_by_id(db: Session, warning_id: int):
    """Get a warning by its ID."""
    try:
        warning = db.query(models.Warning).filter(models.Warning.id == warning_id).first()
        if not warning:
            logger.warning(f"Warning with ID '{warning_id}' not found.")
            return None
        logger.info(f"Fetching warning with ID: {warning_id}")
        return warning
    except Exception as e:
        logger.error(f"Error getting warning with ID '{warning_id}': {e}", exc_info=True)
        raise

def update_warning_by_id(db: Session, warning_id: int, new_warning: str, word_id: int):
    """Update a warning by its ID."""
    try:
        warning_to_update = get_warning_by_id(db, warning_id)
        if not warning_to_update:
            logger.warning(f"Warning with ID '{warning_id}' not found.")
            return None

        warning_to_update.warning_message = new_warning
        warning_to_update.word_id = word_id
        db.commit()
        db.refresh(warning_to_update)
        logger.info(f"Warning with ID '{warning_id}' updated successfully.")
        return warning_to_update
    except Exception as e:
        logger.error(f"Error updating warning with ID '{warning_id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_warning_by_id(db: Session, clerk_id: str, warning_id: int):
    """Delete a warning by its ID, ensuring the user has permission."""
    try:
        to_delete = (
            db.query(models.Warning)
            .join(models.Words)
            .filter(
                models.Warning.id == warning_id,
                models.Words.added_by_user_id == clerk_id,
            )
            .first()
        )
        if not to_delete:
            logger.warning(f"No warning found or user does not have permission to delete it.")
            return False

        db.delete(to_delete)
        db.commit()
        logger.info(f"Warning with ID '{warning_id}' deleted successfully.")
        return True  # Indicate successful deletion
    except Exception as e:
        logger.error(f"Error deleting warning with ID '{warning_id}': {e}", exc_info=True)
        db.rollback()
        raise