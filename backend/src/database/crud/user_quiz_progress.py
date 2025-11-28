from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
logger = logging.getLogger(__name__)

def create_user_quiz_progress(db:Session, user_word_status_id:int) -> models.UserQuizProgress:
    """Create a new UserQuizProgress entry for a given UserWordStatus ID."""
    try:
        new_progress = models.UserQuizProgress(
            user_word_status_id=user_word_status_id,
            learning_stage=1  # Initial learning stage
        )
        db.add(new_progress)
        db.commit()
        db.refresh(new_progress)
        return new_progress
    except Exception as e:
        logger.error(f"Error creating UserQuizProgress for UserWordStatus ID '{user_word_status_id}': {e}", exc_info=True)
        raise
    
def get_user_quiz_progress(db:Session, user_word_status_id:int) -> models.UserQuizProgress:
    """Retrieve UserQuizProgress by UserWordStatus ID."""
    try:
        progress = db.query(models.UserQuizProgress).filter(models.UserQuizProgress.user_word_status_id == user_word_status_id).one()
        return progress
    except NoResultFound:
        logger.warning(f"User quiz progress for UserWordStatus ID '{user_word_status_id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving UserQuizProgress for UserWordStatus ID '{user_word_status_id}': {e}", exc_info=True)
        raise
    
def delete_user_quiz_progress(db:Session, user_quiz_progress_id:int) -> bool:
    """Delete UserQuizProgress by its ID."""
    try:
        progress = db.query(models.UserQuizProgress).filter(models.UserQuizProgress.id == user_quiz_progress_id).one()
        db.delete(progress)
        db.commit()
        return True
    except NoResultFound:
        logger.warning(f"User quiz progress with id '{user_quiz_progress_id}' not found for deletion.")
        return False
    except Exception as e:
        logger.error(f"Error deleting UserQuizProgress with id '{user_quiz_progress_id}': {e}", exc_info=True)
        raise