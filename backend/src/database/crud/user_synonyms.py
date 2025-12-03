from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


def create_user_synonym(db: Session, user_word_status_id: int, synonym: str) -> models.UserSynonyms:
    """Create a new UserSynonyms entry for a given UserWordStatus ID."""
    try:
        word_status = (
            db.query(models.UserWordStatus)
            .filter(models.UserWordStatus.id == user_word_status_id)
            .first()
        )
        if not word_status:
            raise ValueError(f"UserWordStatus with id '{user_word_status_id}' does not exist.")

        existing_synonym = (
            db.query(models.UserSynonyms)
            .filter(
                models.UserSynonyms.user_word_status_id == user_word_status_id,
                models.UserSynonyms.synonym == synonym,
            )
            .first()
        )
        if existing_synonym:
            logger.warning(
                f"Synonym '{synonym}' for UserWordStatus ID '{user_word_status_id}' already exists."
            )
            return existing_synonym

        new_synonym = models.UserSynonyms(user_word_status_id=user_word_status_id, synonym=synonym)
        db.add(new_synonym)
        db.commit()
        db.refresh(new_synonym)
        return new_synonym
    except Exception as e:
        logger.error(
            f"Error creating UserSynonyms for UserWordStatus ID '{user_word_status_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise


def get_user_synonyms(db: Session, user_word_status_id: int) -> list[models.UserSynonyms]:
    """Retrieve UserSynonyms by UserWordStatus ID."""
    try:
        synonym = (
            db.query(models.UserSynonyms)
            .filter(models.UserSynonyms.user_word_status_id == user_word_status_id)
            .all()
        )
        return synonym
    except Exception as e:
        logger.error(
            f"Error retrieving UserSynonyms for UserWordStatus ID '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise


def get_user_synonym_by_id(db: Session, user_synonym_id: int) -> models.UserSynonyms:
    """Retrieve a UserSynonyms by its ID."""
    try:
        synonym = (
            db.query(models.UserSynonyms).filter(models.UserSynonyms.id == user_synonym_id).one()
        )
        return synonym
    except NoResultFound:
        logger.warning(f"User synonym with id '{user_synonym_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving UserSynonyms with id '{user_synonym_id}': {e}", exc_info=True
        )
        raise


def update_user_synonym(db: Session, user_synonym_id: int, new_synonym: str) -> models.UserSynonyms:
    """Update an existing UserSynonyms entry."""
    try:
        synonym_entry = (
            db.query(models.UserSynonyms).filter(models.UserSynonyms.id == user_synonym_id).one()
        )
        synonym_entry.synonym = new_synonym
        db.commit()
        db.refresh(synonym_entry)
        return synonym_entry
    except NoResultFound:
        logger.warning(f"User synonym with id '{user_synonym_id}' not found for update.")
        db.rollback()
        return None
    except Exception as e:
        logger.error(f"Error updating UserSynonyms with id '{user_synonym_id}': {e}", exc_info=True)
        db.rollback()
        raise


def delete_user_synonym(db: Session, user_synonym_id: int) -> bool:
    """Delete UserSynonyms by its ID."""
    try:
        synonym_entry = (
            db.query(models.UserSynonyms).filter(models.UserSynonyms.id == user_synonym_id).one()
        )
        db.delete(synonym_entry)
        db.commit()
        return True
    except NoResultFound:
        logger.warning(f"User synonym with id '{user_synonym_id}' not found for deletion.")
        db.rollback()
        return False
    except Exception as e:
        logger.error(f"Error deleting UserSynonyms with id '{user_synonym_id}': {e}", exc_info=True)
        db.rollback()
        raise
