from sqlalchemy.orm import Session
from .. import models
import logging
from datetime import datetime, timezone
from sqlalchemy.orm.exc import NoResultFound
logger = logging.getLogger(__name__)


def create_user_exercise_progress(db:Session,id:int) -> models.UserExerciseProgress:
    """Create a new user exercise progress entry."""
    try:
        exercise = db.query(models.UserExerciseProgress).filter(models.UserExerciseProgress.id == id).first()
        if exercise:
            logger.warning(f"User exercise progress for user_exercise_id '{id}' already exists.")
            return exercise
        db_user_exercise_progress = models.UserExerciseProgress(
            user_exercise_id=id,
        )
        db.add(db_user_exercise_progress)
        db.commit()
        db.refresh(db_user_exercise_progress)
        
        logger.info(f"Successfully created user exercise progress for user_exercise_id '{id}'.")

        return db_user_exercise_progress
    except Exception as e:
        logger.error(f"Error creating user exercise progress for user_exercise_id '{id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_user_exercise_progress_by_id(db:Session, id:int) -> models.UserExerciseProgress:
    """Get a user exercise progress by its ID."""
    try:
        user_exercise_progress = db.query(models.UserExerciseProgress).filter(models.UserExerciseProgress.id == id).one()
        logger.info(f"User exercise progress with id '{id}' retrieved successfully.")
        return user_exercise_progress
    except NoResultFound:
        logger.warning(f"User exercise progress with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting user exercise progress with id '{id}': {e}", exc_info=True)
        raise

def increase_correct_count(db:Session, id:int) -> models.UserExerciseProgress:
    """Increase the correct count for a user exercise progress."""
    try:
        user_exercise_progress = db.query(models.UserExerciseProgress).filter(models.UserExerciseProgress.id == id).one()
        user_exercise_progress.correct_count += 1
        user_exercise_progress.last_attempted = datetime.now(timezone.utc)  # Update last_attempted timestamp
        db.commit()
        db.refresh(user_exercise_progress)
        
        logger.info(f"Correct count for user exercise progress with id '{id}' increased successfully.")

        return user_exercise_progress
    except NoResultFound:
        logger.warning(f"User exercise progress with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error increasing correct count for user exercise progress with id '{id}': {e}", exc_info=True)
        db.rollback()
        raise
        
def increase_incorrect(db:Session, id:int) -> models.UserExerciseProgress:
    """Increase the incorrect count for a user exercise progress."""
    try:
        user_exercise_progress = db.query(models.UserExerciseProgress).filter(models.UserExerciseProgress.id == id).one()
        user_exercise_progress.incorrect_count += 1
        user_exercise_progress.last_attempted = datetime.now(timezone.utc)  # Update last_attempted timestamp
        db.commit()
        db.refresh(user_exercise_progress)
        
        logger.info(f"Incorrect count for user exercise progress with id '{id}' increased successfully.")

        return user_exercise_progress
    except NoResultFound:
        logger.warning(f"User exercise progress with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error increasing incorrect count for user exercise progress with id '{id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_user_exercise_progress(db:Session, id:int) -> bool:
    """Delete a user exercise progress by its ID."""
    try:
        user_exercise_progress = db.query(models.UserExerciseProgress).filter(models.UserExerciseProgress.id == id).one()
        if not user_exercise_progress:
            logger.warning(f"User exercise progress with id '{id}' does not exist.")
            db.rollback()
            return False
        db.delete(user_exercise_progress)
        db.commit()
        
        logger.info(f"User exercise progress with id '{id}' deleted successfully.")

        return True
    except NoResultFound:
        logger.warning(f"User exercise progress with id '{id}' not found for deletion.")
        return False
    except Exception as e:
        logger.error(f"Error deleting user exercise progress with id '{id}': {e}", exc_info=True)
        db.rollback()
        raise