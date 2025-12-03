from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from .. import models
import logging
from sqlalchemy.orm.exc import NoResultFound
from backend.src.config import settings

logger = logging.getLogger(__name__)


def get_user_quota(db: Session, user_id: int):
    """Get the exercise quota for a user by user ID."""
    try:
        quota = db.query(models.UserQuota).filter(models.UserQuota.user_id == user_id).one()
        logger.info(f"Exercise quota for user_id '{user_id}' retrieved.")
        return quota
    except NoResultFound:
        logger.warning(f"Exercise quota for user_id '{user_id}' not found.")
        return None
    except Exception as e:
        logger.error(f"Error getting exercise quota for user_id '{user_id}': {e}", exc_info=True)
        db.rollback()
        raise


def reset_quota_if_needed(db: Session, quota: models.UserQuota):
    """
    Resets the user's exercise quota if a day has passed since the last reset.
    """
    try:
        now = datetime.now(timezone.utc)
        if now - quota.last_reset > timedelta(hours=settings.QUOTA_RESET_HOURS):
            quota.quota_remaining = settings.DEFAULT_USER_QUOTA
            quota.last_reset = now
            db.commit()
            db.refresh(quota)
            logger.info(f"Reset exercise quota for user {quota.user_id}")
    except Exception as e:
        logger.error(f"Error resetting exercise quota for user {quota.user_id}: {e}", exc_info=True)
        db.rollback()
        raise
    return quota
