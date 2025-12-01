from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
logger = logging.getLogger(__name__)
from backend.src.config import settings

def answer_logic(db:Session, answer:bool, user_quiz_progress_id:int) -> models.UserQuizProgress:
    """Update user quiz progress based on whether the answer was correct or not."""
    try:
        user_quiz_progress = db.query(models.UserQuizProgress).filter(models.UserQuizProgress.id == user_quiz_progress_id).one()
        
        if answer:
            user_quiz_progress.correct += 1
            user_quiz_progress.wrong= 0
            user_quiz_progress.correct_streak += 1
            if user_quiz_progress.correct_streak == settings.CORRECT_STREAK_THRESHOLD:
                if user_quiz_progress.learning_stage < 4:
                    user_quiz_progress.learning_stage += 1
                    user_quiz_progress.correct_streak = 1
        else:
            user_quiz_progress.wrong += 1
            user_quiz_progress.correct_streak = 0
            if user_quiz_progress.wrong == settings.CORRECT_STREAK_THRESHOLD:
                if user_quiz_progress.learning_stage > 1:
                    user_quiz_progress.learning_stage -= 1
                    user_quiz_progress.wrong = 1
            
        db.commit()
        db.refresh(user_quiz_progress)
        return user_quiz_progress
    except NoResultFound:
        logger.warning(f"User quiz progress with id '{user_quiz_progress_id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error updating user quiz progress for id '{user_quiz_progress_id}': {e}", exc_info=True)
        raise

