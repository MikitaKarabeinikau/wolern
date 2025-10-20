from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def get_word_synonyms_from_db(db: Session, word: str, clerk_id: str):
    """Get all synonyms associated with a word for a specific user."""
    try:
        synonyms = (
            db.query(models.Synonym)
            .join(models.Words)
            .filter(
                models.Words.word == word.strip(),
                models.Words.added_by_user_id == clerk_id,
            )
            .all()
        )
        if not synonyms:
            logger.info(f"No synonyms found for word '{word}' and user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(synonyms)} synonyms for word '{word}' and user '{clerk_id}'.")
        return synonyms
    except Exception as e:
        logger.error(
            f"Error getting synonyms for word '{word}' and user '{clerk_id}': {e}",
            exc_info=True,
        )
        raise

def get_all_synonyms_for_user_from_db(db: Session, clerk_id: str):
    """Get all synonyms for a specific user."""
    try:
        synonyms = (
            db.query(models.Synonym)
            .join(models.Words)
            .filter(models.Words.added_by_user_id == clerk_id)
            .all()
        )
        if not synonyms:
            logger.info(f"No synonyms found for user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(synonyms)} synonyms for user '{clerk_id}'.")
        return synonyms
    except Exception as e:
        logger.error(f"Error getting synonyms for user '{clerk_id}': {e}", exc_info=True)
        raise

def delete_synonym_by_id(db: Session, clerk_id: str, synonym_id: int):
    """Delete a synonym by its ID, ensuring the user has permission."""
    try:
        to_delete = (
            db.query(models.Synonym)
            .join(models.Words)
            .filter(
                models.Synonym.id == synonym_id,
                models.Words.added_by_user_id == clerk_id,
            )
            .first()
        )
        if not to_delete:
            logger.warning(
                f"Synonym with ID '{synonym_id}' not found for user '{clerk_id}', or user does not have permission."
            )
            return False
        db.delete(to_delete)
        db.commit()
        logger.info(f"Synonym with ID '{synonym_id}' deleted successfully by user '{clerk_id}'.")
        return True
    except Exception as e:
        logger.error(
            f"Error deleting synonym with ID '{synonym_id}' for user '{clerk_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def get_synonym_by_id(db: Session, synonym_id: int):
    """Get a synonym by its ID."""
    try:
        synonym = db.query(models.Synonym).filter(models.Synonym.id == synonym_id).first()
        if not synonym:
            logger.info(f"Synonym with ID '{synonym_id}' not found.")
            return None
        logger.info(f"Synonym with ID '{synonym_id}' found.")
        return synonym
    except Exception as e:
        logger.error(f"Error getting synonym with ID '{synonym_id}': {e}", exc_info=True)
        raise

def update_synonym_by_id(db: Session, synonym_id: int, new_synonym: str, word_id: int):
    """Update a synonym by its ID."""
    try:
        synonym_to_update = get_synonym_by_id(db, synonym_id)
        if not synonym_to_update:
            logger.info(f"Synonym with ID '{synonym_id}' not found.")
            return None

        synonym_to_update.synonym = new_synonym
        synonym_to_update.word_id = word_id
        db.commit()
        db.refresh(synonym_to_update)
        logger.info(f"Synonym with ID '{synonym_id}' updated successfully.")
        return synonym_to_update
    except Exception as e:
        logger.error(f"Error updating synonym with ID '{synonym_id}': {e}", exc_info=True)
        db.rollback()
        raise

def synonym_exists(db: Session, word_id: int, synonym: str):
    """Check if a synonym exists for a given word."""
    try:
        exists = db.query(models.Synonym).filter(models.Synonym.word_id == word_id, models.Synonym.synonym == synonym).first()
        return exists is not None
    except Exception as e:
        logger.error(f"Error checking if synonym exists for word_id '{word_id}' and synonym '{synonym}': {e}", exc_info=True)
        raise

def add_synonym(db: Session, word_id: int, synonym: str):
    """Add a synonym for a given word."""
    try:
        if synonym_exists(db, word_id, synonym):
            logger.info(f"Synonym '{synonym}' already exists for word_id '{word_id}'.")
            return None
        db_synonym = models.Synonym(word_id=word_id, synonym=synonym)
        db.add(db_synonym)
        db.commit()
        db.refresh(db_synonym)
        logger.info(f"Synonym '{synonym}' added successfully for word_id '{word_id}'.")
        return db_synonym
    except Exception as e:
        logger.error(f"Error adding synonym '{synonym}' for word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise