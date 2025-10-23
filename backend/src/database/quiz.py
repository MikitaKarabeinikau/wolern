from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound


logger = logging.getLogger(__name__)

def get_quiz_words(db: Session, clerk_id: str):
    """Get quiz words for a specific user."""
    try:
        words = db.query(models.Words).join(models.User_Quiz_Progress).filter(models.Words.added_by_user_id == clerk_id, (models.Words.vocabulary == "learning") | (models.Words.vocabulary == "unknown")).order_by(models.User_Quiz_Progress.time_to_repeat).limit(10).all()
        logger.info(f"Fetched {len(words)} quiz words for user with clerk_id '{clerk_id}'.")
        return words
    except Exception as e:
        logger.error(f"Error getting quiz words for user with clerk_id {clerk_id}: {e}", exc_info=True)
        raise

def get_quiz_progress(db: Session, clerk_id: str):
    """Get quiz progress for a specific user."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id).all()
        logger.info(f"Fetched quiz progress for user with clerk_id '{clerk_id}'.")
        return progress
    except Exception as e:
        logger.error(f"Error getting quiz progress for user with clerk_id {clerk_id}: {e}", exc_info=True)
        raise

def increase_correct_answers(db: Session, clerk_id: str, word_id: int):
    """Increase correct answers count for a specific user and word."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).one()
        progress.correct_answers += 1
        db.commit()
        db.refresh(progress)
        logger.info(f"Increased correct answers for user '{clerk_id}' and word_id '{word_id}'.")
        return progress
    except NoResultFound:
        logger.warning(f"No quiz progress found for user '{clerk_id}' and word_id '{word_id}'.")
        return None
    except Exception as e:
        logger.error(f"Error increasing correct answers for user '{clerk_id}' and word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def increase_wrong_answers(db: Session, clerk_id: str, word_id: int):
    """Increase wrong answers count for a specific user and word."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).one()
        progress.wrong_answers += 1
        db.commit()
        db.refresh(progress)
        logger.info(f"Increased wrong answers for user '{clerk_id}' and word_id '{word_id}'.")
        return progress
    except NoResultFound:
        logger.warning(f"No quiz progress found for user '{clerk_id}' and word_id '{word_id}'.")
        return None
    except Exception as e:
        logger.error(f"Error increasing wrong answers for user '{clerk_id}' and word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def increase_learning_stage(db: Session, clerk_id: str, word_id: int):
    """Increase learning stage for a specific user and word."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).one()
        progress.learning_stage += 1
        db.commit()
        db.refresh(progress)
        logger.info(f"Increased learning stage for user '{clerk_id}' and word_id '{word_id}'.")
        return progress
    except NoResultFound:
        logger.warning(f"No quiz progress found for user '{clerk_id}' and word_id '{word_id}'.")
        return None
    except Exception as e:
        logger.error(f"Error increasing learning stage for user '{clerk_id}' and word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def decrease_learning_stage(db: Session, clerk_id: str, word_id: int):
    """Decrease learning stage for a specific user and word."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).one()
        if progress.learning_stage > 0:
            progress.learning_stage -= 1
            db.commit()
            db.refresh(progress)
            logger.info(f"Decreased learning stage for user '{clerk_id}' and word_id '{word_id}'.")
        else:
            logger.info(f"Learning stage is already at minimum for user '{clerk_id}' and word_id '{word_id}'.")
        return progress
    except NoResultFound:
        logger.warning(f"No quiz progress found for user '{clerk_id}' and word_id '{word_id}'.")
        return None
    except Exception as e:
        logger.error(f"Error decreasing learning stage for user '{clerk_id}' and word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def increase_correct_answers_in_a_row(db: Session, clerk_id: str, word_id: int):
    """Increase correct answers in a row for a specific user and word."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).one()
        progress.correct_answers_in_a_row += 1
        db.commit()
        db.refresh(progress)
        logger.info(f"Increased correct answers in a row for user '{clerk_id}' and word_id '{word_id}'.")
        return progress
    except NoResultFound:
        logger.warning(f"No quiz progress found for user '{clerk_id}' and word_id '{word_id}'.")
        return None
    except Exception as e:
        logger.error(f"Error increasing correct answers in a row for user '{clerk_id}' and word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def increase_wrong_answers_in_a_row(db: Session, clerk_id: str, word_id: int):
    """Increase wrong answers in a row for a specific user and word."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).one()
        progress.wrong_answers_in_a_row += 1
        db.commit()
        db.refresh(progress)
        logger.info(f"Increased wrong answers in a row for user '{clerk_id}' and word_id '{word_id}'.")
        return progress
    except NoResultFound:
        logger.warning(f"No quiz progress found for user '{clerk_id}' and word_id '{word_id}'.")
        return None
    except Exception as e:
        logger.error(f"Error increasing wrong answers in a row for user '{clerk_id}' and word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def reset_correct_answers_in_a_row(db: Session, clerk_id: str, word_id: int):
    """Reset correct answers in a row for a specific user and word."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).one()
        progress.correct_answers_in_a_row = 0
        db.commit()
        db.refresh(progress)
        logger.info(f"Reset correct answers in a row for user '{clerk_id}' and word_id '{word_id}'.")
        return progress
    except NoResultFound:
        logger.warning(f"No quiz progress found for user '{clerk_id}' and word_id '{word_id}'.")
        return None
    except Exception as e:
        logger.error(f"Error resetting correct answers in a row for user '{clerk_id}' and word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def reset_wrong_answers_in_a_row(db: Session, clerk_id: str, word_id: int):
    """Reset wrong answers in a row for a specific user and word."""
    try:
        progress = db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.user_id == clerk_id, models.User_Quiz_Progress.word_id == word_id).one()
        progress.wrong_answers_in_a_row = 0
        db.commit()
        db.refresh(progress)
        logger.info(f"Reset wrong answers in a row for user '{clerk_id}' and word_id '{word_id}'.")
        return progress
    except NoResultFound:
        logger.warning(f"No quiz progress found for user '{clerk_id}' and word_id '{word_id}'.")
        return None
    except Exception as e:
        logger.error(f"Error resetting wrong answers in a row for user '{clerk_id}' and word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

