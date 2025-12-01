from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
import json
logger = logging.getLogger(__name__)


def create_exercise(
    db: Session,
    word_id: int,
    difficulty: str,
    part_of_speech: str,
    question: str,
    hints: list,
    explanation: str,
):
    """
    Creates a new exercise in the database.
    """
    try:
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            logger.error(f"Word with ID {word_id} does not exist. Cannot create exercise.")
            db.rollback()
            return None

        exercise = db.query(models.Exercise).filter(
            models.Exercise.word_id == word_id,
            models.Exercise.difficulty == difficulty,
            models.Exercise.question == question
        ).first()
        if exercise:
            logger.warning(f"Exercise for word_id '{word_id}' with the same difficulty and question already exists.")
            db.rollback()
            return exercise

        exercise = models.Exercise(
            word_id=word_id,
            difficulty=difficulty,
            question=question,
            hints=hints,
            explanation=explanation,
            part_of_speech=part_of_speech,
        )
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        logger.info(f"Created new exercise with ID {exercise.id} for user")
        return exercise
    except Exception as e: 
        logger.error(f"Error creating exercise for word_id '{word_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_exercise_by_id(db: Session, id: int):
    """
    Retrieves an exercise by its ID.
    """
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    logger.info(f"Retrieved exercise with ID {id}")
    return exercise

def get_exercises_by_word_id(db: Session, word_id: int):
    """
    Retrieves all exercises for a specific word by its ID.
    """
    exercises = db.query(models.Exercise).filter(models.Exercise.word_id == word_id).all()
    logger.info(f"Retrieved {len(exercises)} exercises for word ID {word_id}")
    return exercises



