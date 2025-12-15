from backend.src.database.models import UserHiddenBaseExample
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def create_hidden_example(
    db: Session,
    user_word_status_id: int,
    example_id: int,
) -> UserHiddenBaseExample:
    """Create a new UserHiddenBaseExample entry."""
    try:
        hidden_example = UserHiddenBaseExample(
            user_word_status_id=user_word_status_id,
            example_id=example_id,
        )
        db.add(hidden_example)
        db.commit()
        db.refresh(hidden_example)
        return hidden_example
    except Exception as e:
        logger.error(
            f"Error creating hidden example for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def get_hidden_examples_by_user_word_status_id(
    db: Session,
    user_word_status_id: int,
) -> list[UserHiddenBaseExample]:
    """Retrieve hidden examples for a given user_word_status_id."""
    try:
        hidden_examples = (
            db.query(UserHiddenBaseExample)
            .filter(UserHiddenBaseExample.user_word_status_id == user_word_status_id)
            .all()
        )
        return hidden_examples
    except Exception as e:
        logger.error(
            f"Error retrieving hidden examples for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def delete_from_hidden_example(
    db: Session,
    hidden_example_id: int,
) -> None:
    """Delete a UserHiddenBaseExample entry by its ID."""
    try:
        hidden_example = (
            db.query(UserHiddenBaseExample)
            .filter(UserHiddenBaseExample.id == hidden_example_id)
            .one()
        )
        db.delete(hidden_example)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting hidden example with ID '{hidden_example_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise
