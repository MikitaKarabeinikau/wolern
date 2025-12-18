from database.crud.user_quiz_progress import get_user_quiz_progress_by_id
from sqlalchemy.orm import Session
from backend.src.database import models
import logging
from sqlalchemy.orm.exc import NoResultFound
from backend.src.config import settings
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)


def answer_logic(db: Session, answer: bool, user_quiz_progress_id: int) -> models.UserQuizProgress:
    """Update user quiz progress based on whether the answer was correct or not."""
    try:
        user_quiz_progress = get_user_quiz_progress_by_id(db, user_quiz_progress_id)

        if answer:
            user_quiz_progress.correct += 1
            user_quiz_progress.wrong_streak = 0
            user_quiz_progress.correct_streak += 1
            if user_quiz_progress.correct_streak == settings.CORRECT_STREAK_THRESHOLD:
                if user_quiz_progress.learning_stage < 5:
                    user_quiz_progress.learning_stage += 1
                    user_quiz_progress.correct_streak = 1
                    logger.info(f"User quiz progress id '{user_quiz_progress_id}' advanced to learning stage '{user_quiz_progress.learning_stage}'.")
        else:
            user_quiz_progress.wrong += 1
            user_quiz_progress.correct_streak = 0
            user_quiz_progress.wrong_streak += 1
            if user_quiz_progress.wrong_streak == settings.CORRECT_STREAK_THRESHOLD:
                if user_quiz_progress.learning_stage > 1:
                    user_quiz_progress.learning_stage -= 1
                    user_quiz_progress.wrong_streak = 1
        updated_time = set_new_time_to_repeat(db, user_quiz_progress, answer)
        user_quiz_progress.time_to_repeat = updated_time.time_to_repeat
        db.commit()
        db.refresh(user_quiz_progress)
        return user_quiz_progress
    except NoResultFound:
        logger.warning(f"User quiz progress with id '{user_quiz_progress_id}' not found.")
        return None
    except Exception as e:
        logger.error(
            f"Error updating user quiz progress for id '{user_quiz_progress_id}': {e}",
            exc_info=True,
        )
        raise

def set_new_time_to_repeat(db:Session, user_quiz_progress:models.UserQuizProgress, answer: bool) -> models.UserQuizProgress:
    """Set a new time to repeat for the user quiz progress."""
    try:
        if answer:
            if user_quiz_progress.correct_streak < settings.CORRECT_STREAK_THRESHOLD:
                streak = user_quiz_progress.correct_streak
            else:
                streak = settings.CORRECT_STREAK_THRESHOLD
        else:
            streak = 0

        learning_stage = user_quiz_progress.learning_stage

        if learning_stage <= 1:
            new_time = settings.REPEAT_INTERVALS[learning_stage][streak]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(minutes=new_time)
        elif learning_stage == 2:
            new_time = settings.REPEAT_INTERVALS[learning_stage][streak]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(hours=new_time)
        elif learning_stage == 3:
            new_time = settings.REPEAT_INTERVALS[learning_stage][streak]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(days=new_time)
        elif learning_stage == 4:
            new_time = settings.REPEAT_INTERVALS[learning_stage][streak]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(weeks=new_time)
        else:  # learning_stage == 5
            new_time = settings.REPEAT_INTERVALS[4][0]
            new_repeat_time = datetime.now(timezone.utc) + timedelta(weeks=new_time * streak)
        logger.info(f"Setting new time to repeat for UserQuizProgress ID '{user_quiz_progress.id}' to '{new_repeat_time}' based on learning stage '{learning_stage}' and streak '{streak}'.")
        user_quiz_progress.time_to_repeat = new_repeat_time
        db.commit()
        db.refresh(user_quiz_progress)
        return user_quiz_progress
    except Exception as e:
        logger.error(
            f"Error setting new time to repeat for UserQuizProgress ID '{user_quiz_progress.id}': {e}",
            exc_info=True,
        )
        raise
