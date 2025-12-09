from typing import Optional
from services.word_service import get_full_word_data_by_id
from sqlalchemy.orm import Session, joinedload
from backend.src.database import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


def get_word_learning_stage(db: Session, user_word_status_id: int) -> int:
    """Retrieve the learning stage for a given user word status."""
    try:
        user_quiz_progress = (
            db.query(models.UserQuizProgress)
            .filter(models.UserQuizProgress.user_word_status_id == user_word_status_id)
            .one()
        )
        return user_quiz_progress.learning_stage
    except NoResultFound:
        logger.warning(f"User quiz progress for word status id '{user_word_status_id}' not found.")
        return 0
    except Exception as e:
        logger.error(
            f"Error retrieving learning stage for word status id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise


def get_all_words_by_learning_stage(
    db: Session, user_id: int, learning_stage: int
) -> list[models.UserWordStatus]:
    """Retrieve all user word statuses for a user at a specific learning stage."""
    try:
        word_statuses = (
            db.query(models.UserWordStatus)
            .join(models.UserQuizProgress)
            .filter(
                models.UserWordStatus.user_id == user_id,
                models.UserQuizProgress.learning_stage == learning_stage,
            )
            .all()
        )
        return word_statuses
    except Exception as e:
        logger.error(
            f"Error retrieving word statuses for user id \\\
                '{user_id}' at learning stage '{learning_stage}': {e}",
            exc_info=True,
        )
        raise

def get_user_word_status_by_vocabulary_word_id(db: Session, vocabulary_word_id: int) -> models.UserWordStatus:
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

def get_word_id_by_user_word_status_id(db: Session, user_word_status_id: int) -> int:
    """Retrieve word_id associated with a given user_word_status_id."""
    try:
        result = (
            db.query(models.VocabularyWords.word_id)
            .join(models.UserWordStatus, models.VocabularyWords.vocabulary_word_id == models.UserWordStatus.vocabulary_word_id)
            .filter(models.UserWordStatus.user_word_status_id == user_word_status_id)
            .one()
        )
        return result.word_id
    except NoResultFound:
        logger.warning(f"Word ID for user_word_status_id '{user_word_status_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error retrieving word ID for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def get_full_user_word_data_by_user_word_status_id(db: Session, user_word_status_id: int) -> Optional[models.UserWordStatus]:
    return db.query(models.UserWordStatus).options(
            joinedload(models.Words.definitions),
            joinedload(models.Words.examples),
            joinedload(models.Words.synonyms),
            joinedload(models.Words.translations),
            joinedload(models.Words.tags),
            joinedload(models.Words.warnings)
        )

def get_base_hidden_translations_id(db: Session, user_word_status_id: int) -> list[int]:
    """Retrieve IDs of base unhidden translations for a given user_word_status_id."""
    try:
        translation_ids = (
            db.query(models.UserHiddenTranslations).join(
                models.UserWordStatus, models.UserHiddenTranslations.user_word_status_id == models.UserWordStatus.user_word_status_id
            )
            .filter(models.UserWordStatus.user_word_status_id == user_word_status_id)
            .all()
        )
        return [tid.translation_id for tid in translation_ids]

    except Exception as e:
        logger.error(
            f"Error retrieving hidden translation IDs for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise

def get_base_unhidden_translations_by_user_word_status_id(db: Session, user_word_status_id: int) -> list[models.Translations]:
    """Retrieve base unhidden translations for a given user_word_status_id."""
    hidden_translation_ids = get_base_hidden_translations_id(db, user_word_status_id)
    word_id = get_word_id_by_user_word_status_id(db, user_word_status_id)
    try:
        translations = (
            db.query(models.Translations)
            .filter(models.Translations.word_id == word_id, models.Translations.id.notin_(hidden_translation_ids))
            .all()
        )
        return translations
    except Exception as e:
        logger.error(
            f"Error retrieving unhidden translations for user_word_status_id '{user_word_status_id}': {e}",
            exc_info=True,
        )
        raise
