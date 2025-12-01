from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
import json
logger = logging.getLogger(__name__)


def create_multiple_choice_exercise(
    db: Session,
    exercise_id: int,
    options: str,
    correct_answer: str,
):
    """
    Creates a new multiple-choice exercise in the database.
    """
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not exercise:
        logger.error(f"Exercise with ID {exercise_id} does not exist. Cannot create multiple-choice exercise.")
        db.rollback()
        return None
    
    options_json = json.loads(options)
    if correct_answer not in options_json:
        logger.error(f"Correct answer '{correct_answer}' is not in the provided options. Cannot create multiple-choice exercise.")
        db.rollback()
        return None
    
    existing = db.query(models.MultipleChoiceExercise).filter(
        models.MultipleChoiceExercise.exercise_id == exercise_id
    ).first()
    if existing:
        logger.warning(f"Multiple-choice exercise for exercise_id '{exercise_id}' already exists.")
        db.rollback()
        return existing
    
    mc_exercise = models.MultipleChoiceExercise(
        exercise_id=exercise_id,
        options=options,
        correct_answer=correct_answer
    )
    db.add(mc_exercise)
    db.commit()
    db.refresh(mc_exercise)
    
    logger.info(f"Created new multiple-choice exercise with ID {mc_exercise.id}")
    return mc_exercise


def get_multiple_choice_exercise_by_id(db: Session, mc_exercise_id: int):
    """
    Retrieves a multiple-choice exercise by its ID.
    """
    mc_exercise = db.query(models.MultipleChoiceExercise).filter(models.MultipleChoiceExercise.id == mc_exercise_id).first()
    logger.info(f"Retrieved multiple-choice exercise with ID {mc_exercise_id}")
    return mc_exercise