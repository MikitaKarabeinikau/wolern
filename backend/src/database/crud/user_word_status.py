from sqlalchemy.orm import Session
from backend.src.database import models

from sqlalchemy.orm.exc import NoResultFound
from .user_quiz_progress import create_user_quiz_progress
import logging

logger = logging.getLogger(__name__)


def create_user_word_status(db: Session, vocabulary_word_id: int) -> models.UserWordStatus:
    """Create a new UserWordStatus entry for a VocabularyWords ID."""
    try:
        new_status = models.UserWordStatus(vocabulary_word_id=vocabulary_word_id)
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        # Initialize quiz progress for the new word status
        create_user_quiz_progress(db, new_status.id)
        return new_status
    except Exception as e:
        logger.error(
            f"Error creating UserWordStatus for vocabulary_word_id '{vocabulary_word_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise


def get_user_word_status(db: Session, vocabulary_word_id: int) -> models.UserWordStatus:
    """Retrieve UserWordStatus by vocabulary_word_id."""
    try:
        status = (
            db.query(models.UserWordStatus)
            .filter(models.UserWordStatus.vocabulary_word_id == vocabulary_word_id)
            .one()
        )
        return status
    except NoResultFound:
        logger.warning(f"UserWordStatus for vocabulary_word_id '{vocabulary_word_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving UserWordStatus for vocabulary_word_id '{vocabulary_word_id}': {e}",
            exc_info=True,
        )
        raise


def delete_user_word_status(db: Session, user_word_status_id: int) -> bool:
    """Delete UserWordStatus by its ID."""
    try:
        status = (
            db.query(models.UserWordStatus)
            .filter(models.UserWordStatus.id == user_word_status_id)
            .one()
        )
        db.delete(status)
        db.commit()
        return True
    except NoResultFound:
        logger.warning(f"UserWordStatus with id '{user_word_status_id}' not found for deletion.")
        return False
    except Exception as e:
        logger.error(
            f"Error deleting UserWordStatus with id '{user_word_status_id}': {e}", exc_info=True
        )
        db.rollback()
        raise
