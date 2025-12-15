from backend.src.database.models import UserHiddenBaseSynonym
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def create_hidden_synonym(
    db: Session,
    user_word_status_id: int,
    synonym_id: int,
) -> UserHiddenBaseSynonym:
    """Create a new UserHiddenBaseSynonym entry."""
    try:
        hidden_synonym = UserHiddenBaseSynonym(
            user_word_status_id=user_word_status_id,
            synonym_id=synonym_id,
        )
        db.add(hidden_synonym)
        db.commit()
        db.refresh(hidden_synonym)
        return hidden_synonym
    except Exception as e:
        logger.error(
            f"Error creating hidden synonym for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def get_hidden_synonyms_by_user_word_status_id(
    db: Session,
    user_word_status_id: int,
) -> list[UserHiddenBaseSynonym]:
    """Retrieve hidden synonyms for a given user_word_status_id."""
    try:
        hidden_synonyms = (
            db.query(UserHiddenBaseSynonym)
            .filter(UserHiddenBaseSynonym.user_word_status_id == user_word_status_id)
            .all()
        )
        return hidden_synonyms
    except Exception as e:
        logger.error(
            f"Error retrieving hidden synonyms for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def delete_from_hidden_synonym(
    db: Session,
    hidden_synonym_id: int,
) -> None:
    """Delete a UserHiddenBaseSynonym entry by its ID."""
    try:
        hidden_synonym = (
            db.query(UserHiddenBaseSynonym)
            .filter(UserHiddenBaseSynonym.id == hidden_synonym_id)
            .one()
        )
        db.delete(hidden_synonym)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting hidden synonym with ID '{hidden_synonym_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise