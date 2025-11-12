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
        user_id=clerk_id,
        exercises_remaining=10,
        last_reset_date=datetime.utcnow()
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