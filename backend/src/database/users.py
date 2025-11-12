import datetime
from sqlalchemy.orm import Session

from backend.src.database.quota import create_exercise_quota
from . import models
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def create_user(db: Session, clerk_id: str, username: str = None, email: str = None):
    """Create a new user and their associated exercise quota."""
    try:
        # 1. Create the user object
        db_user = models.Users(clerk_id=clerk_id, username=username, email=email)
        
        # 2. Create the quota and attach it directly to the user object
        #    SQLAlchemy will automatically handle the foreign key relationship.
        db_user.exercise_quota = models.ExerciseQuota(
            exercises_remaining=10
        )
        
        # 3. Add the user to the session (the quota is added automatically via cascade)
        db.add(db_user)
        logger.info(f"User and quota for clerk_id '{clerk_id}' added to session.")

        # 4. Commit everything in one transaction
        db.commit()

        # 5. Refresh the user to get its ID and the quota's ID from the DB
        db.refresh(db_user)
        
        logger.info(f"Successfully created user and quota for clerk_id '{clerk_id}'.")

        return db_user
    except Exception as e:
        logger.error(f"Error creating user with clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise

def update_username(db: Session, clerk_id: int, new_username: str):
    """Update a user's username."""
    try:
        user = get_user_by_id(db, clerk_id)
        if not user:
            logger.warning(f"User with clerk_id '{clerk_id}' not found.")
            return None
        user.username = new_username
        db.commit()
        db.refresh(user)
        logger.info(f"Username updated for user with clerk_id '{clerk_id}'.")
        return user
    except Exception as e:
        logger.error(f"Error updating username for clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise

def get_user_by_username(db: Session, username: str):
    """Get a user by username."""
    try:
        user = db.query(models.Users).filter(models.Users.username == username).first()
        if not user:
            logger.info(f"User with username '{username}' not found.")
            return None
        logger.info(f"User with username '{username}' found.")
        return user
    except Exception as e:
        logger.error(f"Error getting user by username '{username}': {e}", exc_info=True)
        raise

def get_user_by_id(db: Session, user_id: int):
    """Get a user by ID."""
    try:
        user = db.query(models.Users).filter(models.Users.id == user_id).first()
        if not user:
            logger.info(f"User with ID '{user_id}' not found.")
            return None
        logger.info(f"User with ID '{user_id}' found.")
        return user
    except Exception as e:
        logger.error(f"Error getting user by ID '{user_id}': {e}", exc_info=True)
        raise

def get_user_by_clerk_id(db: Session, clerk_id: str):
    """Get a user by clerk_id."""
    try:
        user = db.query(models.Users).filter(models.Users.clerk_id == clerk_id).first()
        if not user:
            logger.info(f"User with clerk_id '{clerk_id}' not found.")
            return None
        logger.info(f"User with clerk_id '{clerk_id}' found.")
        return user
    except Exception as e:
        logger.error(f"Error getting user by clerk_id '{clerk_id}': {e}", exc_info=True)
        raise