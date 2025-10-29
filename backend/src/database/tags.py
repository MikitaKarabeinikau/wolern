from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def add_tag(db: Session, tag: str, word_id: int):
    """Add a new tag to a word."""
    if not isinstance(word_id, int):
        raise ValueError(f"Invalid word_id: {word_id}. Must be an integer.")

    new_tag = models.Tag(tag=tag, word_id=word_id)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    logger.info(f"Tag '{tag}' added successfully to word ID '{word_id}'.")
    return new_tag

def get_word_tags_from_db(db: Session, word: str, clerk_id: str):
    """Get all tags associated with a word for a specific user."""
    try:
        tags = (
            db.query(models.Tag)
            .join(models.Words)
            .filter(
                models.Words.word == word.strip(),
                models.Words.added_by_user_id == clerk_id,
            )
            .all()
        )
        if not tags:
            logger.info(f"No tags found for word '{word}' and user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(tags)} tags for word '{word}' and user '{clerk_id}'.")
        return tags
    except Exception as e:
        logger.error(
            f"Error getting tags for word '{word}' and user '{clerk_id}': {e}",
            exc_info=True,
        )
        raise


def get_all_tags_for_user_from_db(db: Session, clerk_id: str):
    """Get all tags for a specific user."""
    try:
        tags = (
            db.query(models.Tag)
            .join(models.Words)
            .filter(models.Words.added_by_user_id == clerk_id)
            .all()
        )
        if not tags:
            logger.info(f"No tags found for user '{clerk_id}'.")
            return []
        logger.info(f"Found {len(tags)} tags for user '{clerk_id}'.")
        return tags
    except Exception as e:
        logger.error(f"Error getting tags for user '{clerk_id}': {e}", exc_info=True)
        raise


def delete_tag_by_id(db: Session, clerk_id: str, tag_id: int):
    """Delete a tag by its ID, ensuring the user has permission."""
    try:
        to_delete = (
            db.query(models.Tag)
            .join(models.Words)
            .filter(
                models.Tag.id == tag_id, models.Words.added_by_user_id == clerk_id
            )
            .first()
        )
        if not to_delete:
            logger.warning(
                f"Tag with ID '{tag_id}' not found for user '{clerk_id}', or user does not have permission."
            )
            return False
        db.delete(to_delete)
        db.commit()
        logger.info(f"Tag with ID '{tag_id}' deleted successfully by user '{clerk_id}'.")
        return True
    except Exception as e:
        logger.error(
            f"Error deleting tag with ID '{tag_id}' for user '{clerk_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise


def get_tag_by_id(db: Session, tag_id: int):
    """Get a tag by its ID."""
    try:
        tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
        if not tag:
            logger.info(f"Tag with ID '{tag_id}' not found.")
            return None
        logger.info(f"Tag with ID '{tag_id}' found.")
        return tag
    except Exception as e:
        logger.error(f"Error getting tag with ID '{tag_id}': {e}", exc_info=True)
        raise


def update_tag_by_id(db: Session, tag_id: int, new_tag: str, word_id: int):
    """Update a tag by its ID."""
    try:
        tag_to_update = get_tag_by_id(db, tag_id)
        if not tag_to_update:
            logger.info(f"Tag with ID '{tag_id}' not found.")
            return None

        tag_to_update.tag = new_tag
        tag_to_update.word_id = word_id
        db.commit()
        db.refresh(tag_to_update)
        logger.info(f"Tag with ID '{tag_id}' updated successfully.")
        return tag_to_update
    except Exception as e:
        logger.error(f"Error updating tag with ID '{tag_id}': {e}", exc_info=True)
        db.rollback()
        raise