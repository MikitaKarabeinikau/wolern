from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def get_all_definitions_for_user_from_db(db: Session, clerk_id: str):
    """Get all definitions for a specific user."""
    try:
        definitions = (
            db.query(models.Definition)
            .join(models.Words)
            .filter(models.Words.added_by_user_id == clerk_id)
            .all()
        )
        if not definitions:
            logger.info(f"No definitions found for user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(definitions)} definitions for user '{clerk_id}'.")
        return definitions
    except Exception as e:
        logger.error(f"Error getting definitions for user '{clerk_id}': {e}", exc_info=True)
        raise


def get_word_part_of_speech_from_db(db: Session, word: str, clerk_id: str):
    """Get part of speech associated with a word for a specific user."""
    try:
        part_of_speech = (
            db.query(models.Words)
            .join(models.Definition.part_of_speech)
            .filter(
                models.Words.word == word.strip(),
                models.Words.added_by_user_id == clerk_id,
            )
            .all()
        )
        if not part_of_speech:
            logger.info(f"No part of speech found for word '{word}' and user '{clerk_id}'.")
            return []
        logger.info(f"Found part of speech for word '{word}' and user '{clerk_id}'.")
        return part_of_speech
    except Exception as e:
        logger.error(
            f"Error getting part of speech for word '{word}' and user '{clerk_id}': {e}",
            exc_info=True,
        )
        raise

def get_definitions_for_quiz(db: Session, clerk_id: str):
    """Get all definitions for quiz words for a specific user."""
    try:
        definitions = (
            db.query(models.Definition)
            .join(models.Words)
            .filter(
                models.Words.added_by_user_id == clerk_id,
                (models.Words.vocabulary == "learning") | (models.Words.vocabulary == "unknown")
            )
            .all()
        )
        if not definitions:
            logger.info(f"No definitions found for quiz words for user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(definitions)} definitions for quiz words for user '{clerk_id}'.")
        return definitions
    except Exception as e:
        logger.error(f"Error getting definitions for quiz words for user '{clerk_id}': {e}", exc_info=True)
        raise

def get_definitions_by_word(db: Session, word: str, clerk_id: str):
    """Get definitions for a specific word and user."""
    try:
        definitions = (
            db.query(models.Definition)
            .join(models.Words)
            .filter(
                models.Words.word == word.strip(),
                models.Words.added_by_user_id == clerk_id,
            )
            .all()
        )
        if not definitions:
            logger.info(f"No definitions found for word '{word}' and user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(definitions)} definitions for word '{word}' and user '{clerk_id}'.")
        return definitions
    except Exception as e:
        logger.error(
            f"Error getting definitions for word '{word}' and user '{clerk_id}': {e}",
            exc_info=True,
        )
        raise

def get_definition_by_id(db: Session, definition_id: int):
    """Get a definition by its ID."""
    try:
        definition = db.query(models.Definition).filter(models.Definition.id == definition_id).first()
        if not definition:
            logger.info(f"Definition with ID '{definition_id}' not found.")
            return None
        logger.info(f"Definition with ID '{definition_id}' found.")
        return definition
    except Exception as e:
        logger.error(f"Error getting definition with ID '{definition_id}': {e}", exc_info=True)
        raise

def update_definition_by_id(db: Session, definition_id: int, new_definition: str):
    """Update a definition by its ID."""
    try:
        definition_to_update = get_definition_by_id(db, definition_id)
        if not definition_to_update:
            logger.info(f"Definition with ID '{definition_id}' not found.")
            return None

        definition_to_update.definition = new_definition
        db.commit()
        db.refresh(definition_to_update)
        logger.info(f"Definition with ID '{definition_id}' updated successfully.")
        return definition_to_update
    except Exception as e:
        logger.error(f"Error updating definition with ID '{definition_id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_definition_by_id(db: Session, clerk_id: str, definition_id: int):
    """Delete a definition by its ID, ensuring the user has permission."""
    try:
        to_delete = (
            db.query(models.Definition)
            .join(models.Words)
            .filter(
                models.Definition.id == definition_id,
                models.Words.added_by_user_id == clerk_id,
            )
            .first()
        )
        if not to_delete:
            logger.warning(
                f"Definition with ID '{definition_id}' not found for user '{clerk_id}', or user does not have permission."
            )
            return False
        db.delete(to_delete)
        db.commit()
        logger.info(f"Definition with ID '{definition_id}' deleted successfully by user '{clerk_id}'.")
        return True
    except Exception as e:
        logger.error(
            f"Error deleting definition with ID '{definition_id}' for user '{clerk_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise