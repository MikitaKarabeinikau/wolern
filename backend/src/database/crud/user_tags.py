from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


def create_user_tag(db: Session, user_word_status_id: int, tag: str) -> models.UserTags:
    """Create a new UserTags entry for a given user ID."""
    try:
        word_status = (
            db.query(models.UserWordStatus)
            .filter(models.UserWordStatus.id == user_word_status_id)
            .first()
        )
        if not word_status:
            raise ValueError(f"UserWordStatus with id '{user_word_status_id}' does not exist.")

        existing_tag = (
            db.query(models.UserTags)
            .filter(
                models.UserTags.user_word_status_id == user_word_status_id,
                models.UserTags.tag == tag,
            )
            .first()
        )
        if existing_tag:
            logger.warning(
                f"Tag '{tag}' for user_word_status_id '{user_word_status_id}' already exists."
            )
            return existing_tag

        new_tag = models.UserTags(user_word_status_id=user_word_status_id, tag=tag)
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        return new_tag
    except Exception as e:
        logger.error(
            f"Error creating UserTags for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise


def get_user_definitions_by_user_word_status_id(
    db: Session, user_word_status_id: int
) -> list[models.UserTags]:
    """Retrieve UserTags by user_word_status_id."""
    try:
        tags = (
            db.query(models.UserTags)
            .filter(models.UserTags.user_word_status_id == user_word_status_id)
            .all()
        )
        return tags
    except Exception as e:
        logger.error(
            f"Error retrieving UserTags for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise


def get_user_tags(db: Session, user_word_status_id: int) -> list[models.UserTags]:
    """Retrieve UserTags by user_word_status_id."""
    try:
        tags = (
            db.query(models.UserTags)
            .filter(models.UserTags.user_word_status_id == user_word_status_id)
            .all()
        )
        return tags
    except Exception as e:
        logger.error(
            f"Error retrieving UserTags for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise


def get_user_tag_by_id(db: Session, user_tag_id: int) -> models.UserTags:
    """Retrieve a UserTags by its ID."""
    try:
        tag = db.query(models.UserTags).filter(models.UserTags.id == user_tag_id).one()
        return tag
    except NoResultFound:
        logger.warning(f"User tag with id '{user_tag_id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving UserTags with id '{user_tag_id}': {e}", exc_info=True)
        raise


def update_user_tag(db: Session, user_tag_id: int, new_tag: str) -> models.UserTags:
    """Update an existing UserTags entry."""
    try:
        tag_entry = db.query(models.UserTags).filter(models.UserTags.id == user_tag_id).one()
        tag_entry.tag = new_tag
        db.commit()
        db.refresh(tag_entry)
        return tag_entry
    except NoResultFound:
        logger.warning(f"User tag with id '{user_tag_id}' not found for update.")
        db.rollback()
        return None
    except Exception as e:
        logger.error(f"Error updating UserTags with id '{user_tag_id}': {e}", exc_info=True)
        db.rollback()
        raise


def delete_user_tag(db: Session, user_tag_id: int) -> bool:
    """Delete UserTags by its ID."""
    try:
        tag_entry = db.query(models.UserTags).filter(models.UserTags.id == user_tag_id).one()
        db.delete(tag_entry)
        db.commit()
        return True
    except NoResultFound:
        logger.warning(f"User tag with id '{user_tag_id}' not found for deletion.")
        return False
    except Exception as e:
        logger.error(f"Error deleting UserTags with id '{user_tag_id}': {e}", exc_info=True)
        db.rollback()
        raise
