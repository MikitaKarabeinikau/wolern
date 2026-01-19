from backend.src.database.models import UserHiddenBaseDefinition, UserHiddenBaseExample
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def create_hidden_definition(
    db: Session,
    user_word_status_id: int,
    definition_id: int,
) -> UserHiddenBaseDefinition:
    """Create a new UserHiddenBaseDefinition entry."""
    try:
        hidden_definition = UserHiddenBaseDefinition(
            user_word_status_id=user_word_status_id,
            definition_id=definition_id,
        )
        db.add(hidden_definition)
        db.commit()
        db.refresh(hidden_definition)
        return hidden_definition
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
) -> list[UserHiddenBaseDefinition]:
    """Retrieve hidden examples for a given user_word_status_id."""
    try:
        hidden_definitions = (
            db.query(UserHiddenBaseDefinition)
            .filter(UserHiddenBaseDefinition.user_word_status_id == user_word_status_id)
            .all()
        )
        return hidden_definitions
    except Exception as e:
        logger.error(
            f"Error retrieving hidden examples for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def delete_from_hidden_definition(
    db: Session,
    hidden_definition_id: int,
) -> None:
    """Delete a UserHiddenBaseDefinition entry by its ID."""
    try:
        hidden_definition = (
            db.query(UserHiddenBaseDefinition)
            .filter(UserHiddenBaseDefinition.id == hidden_definition_id)
            .one()
        )
        db.delete(hidden_definition)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting hidden definition with ID '{hidden_definition_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise
