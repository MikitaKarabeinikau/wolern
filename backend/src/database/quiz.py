from sqlalchemy.orm import Session
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound


logger = logging.getLogger(__name__)

def get_quiz_words(db: Session, clerk_id: str):
    """Get quiz words for a specific user."""
    try:
        words = db.query(models.Words).filter(models.Words.added_by_user_id == clerk_id, (models.Words.vocabulary == "learning") | (models.Words.vocabulary == "unknown")).order_by(models.Words.time_to_reapet).limit(10).all()
        logger.info(f"Fetched {len(words)} quiz words for user with clerk_id '{clerk_id}'.")
        return words
    except Exception as e:
        logger.error(f"Error getting quiz words for user with clerk_id {clerk_id}: {e}", exc_info=True)
        raise