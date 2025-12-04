from sqlalchemy.orm import Session
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