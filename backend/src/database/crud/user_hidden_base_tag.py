from backend.src.database.models import UserHiddenBaseTag
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def create_hidden_tag(
    db: Session,
    user_word_status_id: int,
    tag_id: int,
) -> UserHiddenBaseTag:
    """Create a new UserHiddenBaseTag entry."""
    try:
        hidden_tag = UserHiddenBaseTag(
            user_word_status_id=user_word_status_id,
            tag_id=tag_id,
        )
        db.add(hidden_tag)
        db.commit()
        db.refresh(hidden_tag)
        return hidden_tag
    except Exception as e:
        logger.error(
            f"Error creating hidden tag for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def get_hidden_tags_by_user_word_status_id(
    db: Session,
    user_word_status_id: int,
) -> list[UserHiddenBaseTag]:
    """Retrieve hidden tags for a given user_word_status_id."""
    try:
        hidden_tags = (
            db.query(UserHiddenBaseTag)
            .filter(UserHiddenBaseTag.user_word_status_id == user_word_status_id)
            .all()
        )
        return hidden_tags
    except Exception as e:
        logger.error(
            f"Error retrieving hidden tags for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def delete_from_hidden_tag(
    db: Session,
    hidden_tag_id: int,
) -> None:
    """Delete a UserHiddenBaseTag entry by its ID."""
    try:
        hidden_tag = (
            db.query(UserHiddenBaseTag)
            .filter(UserHiddenBaseTag.id == hidden_tag_id)
            .one()
        )
        db.delete(hidden_tag)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting hidden tag with ID '{hidden_tag_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise
