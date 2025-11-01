from sqlalchemy import Session
from datetime import datetime, timedelta
from . import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_exercise_quota(db: Session, user_clerk_id: str) -> int:
    """
    Returns the number of exercises a user can generate per day.
    This is a placeholder function and should be replaced with actual logic.
    """
    return (db.query(models.ExerciseQuota)
            .filter(models.ExerciseQuota.clerk_id == user_clerk_id)
            .first())

def create_exercise_quota(db: Session, user_clerk_id: str):
    """
    Creates a new exercise quota for a user.
    """
    quota = models.ExerciseQuota(
        clerk_id=user_clerk_id
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
    user_clerk_id: str,
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
        created_by=user_clerk_id
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    logger.info(f"Created new exercise with ID {exercise.exercise_id} for user {user_clerk_id}")
    
    # Also create an entry in ExerciseBase 
    create_exercise_base(
        db,
        base_id=word_id,
        difficulty=difficulty,
        exercise_type=exercise_type,
        question=question,
        options=options,
        hints=hints,
        correct_answer=correct_answer,
        explanation=explanation,
        part_of_speech=part_of_speech,
    )
    return exercise

def create_exercise_base(
    db: Session,
    base_id: int,
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
        base_id=base_id,
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

def create_multiple_choice_exercise(
    db: Session,
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
    create_multiple_choice_exercise_base(
        db,
        exercise_id=exercise_id,
        options=options,
        correct_answer=correct_answer
    )
    logger.info(f"Created new multiple-choice exercise with ID {mc_exercise.id}")
    return mc_exercise

def create_multiple_choice_exercise_base(
    db: Session,
    exercise_id: int,
    options: str,
    correct_answer: str,
):
    """
    Creates a new multiple-choice exercise base in the database.
    """
    mc_exercise_base = models.MultipleChoiceExerciseBase(
        exercise_id=exercise_id,
        options=options,
        correct_answer=correct_answer
    )
    db.add(mc_exercise_base)
    db.commit()
    db.refresh(mc_exercise_base)
    logger.info(f"Created new multiple-choice exercise base with ID {mc_exercise_base.id}")
    return mc_exercise_base

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