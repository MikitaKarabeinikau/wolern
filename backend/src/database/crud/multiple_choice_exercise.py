from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
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