from sqlalchemy.orm import Session

from .user_exercise_progress import create_user_exercise_progress
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


def create_user_exercise(
    db: Session, user_id: int, exercise_id: int, word_id: int
) -> models.UserExercises:
    """Create a new user exercise record."""
    try:
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            raise ValueError(f"Words with id '{word_id}' does not exist.")

        existing_exercise = (
            db.query(models.UserExercises)
            .filter(
                models.UserExercises.user_id == user_id,
                models.UserExercises.exercise_id == exercise_id,
                models.UserExercises.word_id == word_id,
            )
            .first()
        )
        if existing_exercise:
            logger.warning(
                f"User exercise for user_id '{user_id}', \\\
                    exercise_id '{exercise_id}' already exists."
            )
            return existing_exercise

        db_user_exercise = models.UserExercises(
            user_id=user_id,
            exercise_id=exercise_id,
            word_id=word_id,
        )
        db.add(db_user_exercise)

        db.flush()  # Ensure the ID is generated before calling
        create_user_exercise_progress(db, db_user_exercise.id)
        logger.info(
            f"Successfully created user exercise for user_id '{user_id}', \\\
                exercise_id '{exercise_id}'."
        )
        db.commit()
        db.refresh(db_user_exercise)

        return db_user_exercise
    except Exception as e:
        logger.error(
            f"Error creating user exercise for user_id '{user_id}', \\\
                exercise_id '{exercise_id}': {e}",
            exc_info=True,
        )
        db.rollback()
        raise


def get_user_exercises_by_user_id(db: Session, user_id: int) -> list[models.UserExercises]:
    """Get all user exercises for a specific user by their ID."""
    try:
        user_exercises = (
            db.query(models.UserExercises).filter(models.UserExercises.user_id == user_id).all()
        )
        logger.info(f"Retrieved {len(user_exercises)} user exercises for user_id '{user_id}'.")
        return user_exercises
    except Exception as e:
        logger.error(f"Error getting user exercises for user_id '{user_id}': {e}", exc_info=True)
        raise


def get_user_exercise_by_id(db: Session, id: int) -> models.UserExercises:
    """Get a user exercise by its ID."""
    try:
        user_exercise = db.query(models.UserExercises).filter(models.UserExercises.id == id).one()
        logger.info(f"User exercise with id '{id}' retrieved successfully.")
        return user_exercise
    except NoResultFound:
        logger.warning(f"User exercise with id '{id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting user exercise with id '{id}': {e}", exc_info=True)
        raise


def delete_user_exercise(db: Session, id: int) -> None:
    """Delete a user exercise by its ID."""
    try:
        user_exercise = db.query(models.UserExercises).filter(models.UserExercises.id == id).one()
        db.delete(user_exercise)
        db.commit()

        logger.info(f"User exercise with id '{id}' deleted successfully.")
    except NoResultFound:
        logger.warning(f"User exercise with id '{id}' not found for deletion.")
    except Exception as e:
        logger.error(f"Error deleting user exercise with id '{id}': {e}", exc_info=True)
        db.rollback()
        raise
