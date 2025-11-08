from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models
import logging
from backend.src.database.words import get_word_by_id
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_exercise_quota(db: Session, clerk_id: str) -> int:
    """
    Returns the number of exercises a user can generate per day.
    This is a placeholder function and should be replaced with actual logic.
    """
    return (db.query(models.ExerciseQuota)
            .filter(models.ExerciseQuota.user_id == clerk_id)
            .first())

def create_exercise_quota(db: Session, clerk_id: str):
    """
    Creates a new exercise quota for a user.
    """
    quota = models.ExerciseQuota(
        user_id=clerk_id
    )
    db.add(quota)
    db.commit()
    db.refresh(quota)
    return quota

def reset_quota_if_needed(db: Session, quota: models.ExerciseQuota):
    """
    Resets the user's exercise quota if a day has passed since the last reset.
    """
    now = datetime.utcnow()
    if now - quota.last_reset_date > timedelta(hours=24):
        quota.exercises_remaining = 10
        quota.last_reset_date = now
        db.commit()
        db.refresh(quota)
        logger.info(f"Reset exercise quota for user {quota.clerk_id}")
    return quota

def create_exercise(
    db: Session,
    created_by: str,
    word_id: int,
    difficulty: str,
    question: str,
    hints: str,
    explanation: str,
    part_of_speech: str,
):
    """
    Creates a new exercise in the database.
    """
    exercise = models.Exercise(
        word_id=word_id,
        difficulty=difficulty,
        question=question,
        hints=hints,
        explanation=explanation,
        part_of_speech=part_of_speech,
        created_by=created_by
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    logger.info(f"Created new exercise with ID {exercise.id} for user {created_by}")
    return exercise

def create_exercise_base(
    db: Session,
    word: str,
    difficulty: str,
    question: str,
    hints: str,
    explanation: str,
    part_of_speech: str,
):
    """
    Creates a new exercise base in the database.
    """
    exercise_base = models.ExerciseBase(
        word=word,
        difficulty=difficulty,       
        question=question,
        hints=hints,
        explanation=explanation,
        part_of_speech=part_of_speech
    )
    db.add(exercise_base)
    db.commit()
    db.refresh(exercise_base)
    logger.info(f"Created new exercise base with ID {exercise_base.id}")
    return exercise_base


def get_exercise_by_id(db: Session, exercise_id: int):
    """
    Retrieves an exercise by its ID.
    """
    exercise = db.query(models.Exercise).filter(models.Exercise.exercise_id == exercise_id).first()
    logger.info(f"Retrieved exercise with ID {exercise_id}")
    return exercise

def create_multiple_choice_exercise(
    db: Session,
    word_id: int,
    exercise_id: int,
    options: str,
    correct_answer: str,
):
    """
    Creates a new multiple-choice exercise in the database.
    """
    mc_exercise = models.MultipleChoiceExerciseBase(
        exercise_id=exercise_id,
        options=options,
        correct_answer=correct_answer
    )
    db.add(mc_exercise)
    db.commit()
    db.refresh(mc_exercise)
    
    logger.info(f"Created new multiple-choice exercise with ID {mc_exercise.id}")
    return mc_exercise

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

def get_user_exercises(db: Session, user_clerk_id: str):
    """
    Retrieves all exercises created by a specific user.
    """
    exercises = (db.query(models.Exercise)
                 .filter(models.Exercise.created_by == user_clerk_id)
                 .all())
    logger.info(f"Retrieved {len(exercises)} exercises for user {user_clerk_id}")
    return exercises

def get_user_exercise_from_base(db: Session, user_clerk_id: str, base_id: int):
    """
    Retrieves exercises from ExerciseBase created by a specific user for a given base_id.
    """
    exercises = (db.query(models.ExerciseBase)
                 .join(models.Words, models.ExerciseBase.base_id == models.Words.id)
                 .filter(models.Words.created_by == user_clerk_id)
                 .filter(models.ExerciseBase.base_id == base_id)
                 .all())
    logger.info(f"Retrieved {len(exercises)} exercises from base ID {base_id} for user {user_clerk_id}")
    return exercises

def get_random_word_for_exercise(db: Session, clerk_id: str):
    """
    Get a word for exercise with the following priority:
    1. Learning stage (lowest first, starting from 1)
    2. Number of existing exercises for that word (lowest first)
    3. Wrong answers in a row (highest first)
    4. Total wrong answers (highest first)
    """
    result = (db.query(models.Words).join(models.User_Quiz_Progress, models.Words.id == models.User_Quiz_Progress.word_id).filter(
        models.Words.added_by_user_id == clerk_id
    ).order_by(
        models.User_Quiz_Progress.learning_stage.desc(),
        models.User_Quiz_Progress.wrong_answers_in_a_row.desc(),
        models.User_Quiz_Progress.wrong_answers.desc()
    ).first())
    return result