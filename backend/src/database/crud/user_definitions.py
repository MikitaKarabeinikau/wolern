from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


def create_user_definition(
    db: Session, user_word_status_id: int, part_of_speech: str, definition: str
) -> models.UserDefinitions:
    """Create a new user definition for a user word status."""
    try:
        word_status = (
            db.query(models.UserWordStatus)
            .filter(models.UserWordStatus.id == user_word_status_id)
            .first()
        )
        if not word_status:
            raise ValueError(f"UserWordStatus with id '{user_word_status_id}' does not exist.")

        existing_definition = (
            db.query(models.UserDefinitions)
            .filter(
                models.UserDefinitions.user_word_status_id == user_word_status_id,
                models.UserDefinitions.part_of_speech == part_of_speech,
                models.UserDefinitions.definition == definition,
            )
            .first()
        )
        if existing_definition:
            logger.warning(
                f"Definition '{definition}' for user_word_status_id '{user_word_status_id}'\\\
                     and part_of_speech '{part_of_speech}' already exists."
            )
            return existing_definition

        db_user_definition = models.UserDefinitions(
            user_word_status_id=user_word_status_id,
            part_of_speech=part_of_speech,
            definition=definition,
        )
        db.add(db_user_definition)
        db.commit()
        db.refresh(db_user_definition)

        logger.info(
            f"Successfully created user definition for user_word_status_id '{user_word_status_id}'."
        )

        return db_user_definition
    except Exception as e:
        logger.error(
            f"Error creating user definition for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise


def get_user_definitions_by_user_word_status_id(
    db: Session, user_word_status_id: int
) -> list[models.UserDefinitions]:
    """Get all user definitions for a specific user word status by its ID."""
    try:
        user_definitions = (
            db.query(models.UserDefinitions)
            .filter(models.UserDefinitions.user_word_status_id == user_word_status_id)
            .all()
        )
        logger.info(
            f"Retrieved {len(user_definitions)} user definitions \\\
                for user_word_status_id '{user_word_status_id}'."
        )
        return user_definitions
    except Exception as e:
        logger.error(
            f"Error getting user definitions for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise


def get_user_definition_by_id(db: Session, id: int) -> models.UserDefinitions:
    """Get a user definition by its ID."""
    try:
        user_definition = (
            db.query(models.UserDefinitions).filter(models.UserDefinitions.id == id).one()
        )
        logger.info(f"User definition with id '{id}' retrieved successfully.")
        return user_definition
    except NoResultFound:
        logger.warning(f"User definition with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting user definition with id '{id}': {e}", exc_info=True)
        raise


def update_user_definition(db: Session, id: int, new_definition: str, part_of_speech: str) -> models.UserDefinitions:
    """Update an existing user definition."""
    try:
        user_definition = (
            db.query(models.UserDefinitions).filter(models.UserDefinitions.id == id).one()
        )
        user_definition.definition = new_definition
        user_definition.part_of_speech = part_of_speech
        db.commit()
        db.refresh(user_definition)
        logger.info(f"User definition with id '{id}' updated successfully.")
        return user_definition
    except NoResultFound:
        logger.warning(f"User definition with id '{id}' not found for update.")
        return None
    except Exception as e:
        logger.error(f"Error updating user definition with id '{id}': {e}", exc_info=True)
        db.rollback()
        raise


def delete_user_definition(db: Session, id: int) -> bool:
    """Delete a user definition by its ID."""
    try:
        user_definition = (
            db.query(models.UserDefinitions).filter(models.UserDefinitions.id == id).one()
        )
        db.delete(user_definition)
        db.commit()

        logger.info(f"User definition with id '{id}' deleted successfully.")
        return True
    except NoResultFound:
        logger.warning(f"User definition with id '{id}' not found for deletion.")
        return False
    except Exception as e:
        logger.error(f"Error deleting user definition with id '{id}': {e}", exc_info=True)
        db.rollback()
        raise
