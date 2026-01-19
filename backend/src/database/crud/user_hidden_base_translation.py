from backend.src.database.models import UserHiddenBaseTranslation
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def create_hidden_translation(
    db: Session,
    user_word_status_id: int,
    translation_id: int,
) -> UserHiddenBaseTranslation:
    """Create a new UserHiddenTranslations entry."""
    try:
        hidden_translation = UserHiddenBaseTranslation(
            user_word_status_id=user_word_status_id,
            translation_id=translation_id,
        )
        db.add(hidden_translation)
        db.commit()
        db.refresh(hidden_translation)
        return hidden_translation
    except Exception as e:
        logger.error(
            f"Error creating hidden translation for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise

def get_hidden_translations_by_user_word_status_id(
    db: Session,
    user_word_status_id: int,
) -> list[UserHiddenBaseTranslation]:
    """Retrieve hidden translations for a given user_word_status_id."""
    try:
        hidden_translations = (
            db.query(UserHiddenBaseTranslation)
            .filter(UserHiddenBaseTranslation.user_word_status_id == user_word_status_id)
            .all()
        )
        return hidden_translations
    except Exception as e:
        logger.error(
            f"Error retrieving hidden translations for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def delete_from_hidden_translation(
    db: Session,
    hidden_translation_id: int,
) -> None:
    """Delete a UserHiddenTranslations entry by its ID."""
    try:
        hidden_translation = (
            db.query(UserHiddenBaseTranslation)
            .filter(UserHiddenBaseTranslation.id == hidden_translation_id)
            .one()
        )
        db.delete(hidden_translation)
        db.commit()
    except Exception as e:
        logger.error(
            f"Error deleting hidden translation with id '{hidden_translation_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise
