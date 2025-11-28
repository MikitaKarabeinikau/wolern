from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
logger = logging.getLogger(__name__)

def create_tag(db: Session, word_id: int, tag: str) -> models.Tags:
    """Create a new tag for a word."""
    try:
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            raise ValueError(f"Word with id '{word_id}' does not exist.")
        
        existing_tag = db.query(models.Tags).filter(
            models.Tags.word_id == word_id,
            models.Tags.tag == tag
        ).first()
        if existing_tag:
            logger.info(f"Tag already exists for word_id '{word_id}'.")
            return existing_tag

        db_tag = models.Tags(
            word_id=word_id,
            tag=tag
        )
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        
        logger.info(f"Successfully created tag for word_id '{word_id}'.")

        return db_tag
    except Exception as e:
        logger.error(f"Error creating tag for word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_tags_by_word_id(db: Session, word_id: int) -> list[models.Tags]:
    """Get all tags for a specific word by its ID."""
    try:
        tags = db.query(models.Tags).filter(models.Tags.word_id == word_id).all()
        logger.info(f"Retrieved {len(tags)} tags for word_id '{word_id}'.")
        return tags
    except Exception as e:
        logger.error(f"Error getting tags for word_id '{word_id}': {e}", exc_info=True)
        raise

def get_tag_by_id(db: Session, id: int) -> models.Tags:
    """Get a tag by its ID."""
    try:
        tag = db.query(models.Tags).filter(models.Tags.id == id).one()
        logger.info(f"Tag with id '{id}' retrieved successfully.")
        return tag
    except NoResultFound:
        logger.warning(f"Tag with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting tag with id '{id}': {e}", exc_info=True)
        raise