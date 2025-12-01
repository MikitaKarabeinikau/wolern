from sqlalchemy.orm import Session
from .. import models
import logging
from backend.src.config import settings
from typing import Optional,List
import os 
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)
logger = logging.getLogger(__name__)


def create_user(db: Session, clerk_id: str, username: str = None,native_language: str = None, preferred_language: str = None, email: str = None,role: str = "user") -> models.Users:
    """Create a new user and their associated exercise quota."""
    try:
        admin_emails = os.getenv("ADMINS_EMAIL", "").split(",")
        admin_emails = [email.strip() for email in admin_emails if email.strip()]
        role = "admin" if email in admin_emails else "user"

        db_user = models.Users(clerk_id=clerk_id, username=username, native_language=native_language, preferred_language=preferred_language, email=email, role=role)
        if role == "admin":
            db_user.user_quota = models.UserQuota(
                quota_remaining=settings.ADMIN_QUOTA
            )
        else:
            db_user.user_quota = models.UserQuota(
                quota_remaining=settings.DEFAULT_USER_QUOTA
            )
        db.add(db_user)
        db.flush()
        logger.info(f"Successfully created user with clerk_id '{clerk_id}'.")
        for default_vocab in settings.DEFAULT_VOCABULARIES:
            db_vocabulary = models.Vocabulary(
                user_id=db_user.id,
                name=default_vocab
            )
            db.add(db_vocabulary)
            logger.info(f"Default vocabulary '{default_vocab}' for user_id '{db_user.id}' added to session.")
        db.commit()  # Commit first to get ID
        db.refresh(db_user)  # Then refresh

        logger.info(f"Successfully created user and quota for clerk_id '{clerk_id}'.")

        return db_user
    except Exception as e:
        logger.error(f"Error creating user with clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise
    
def get_all_users(db: Session) -> List[models.Users]:
    """Get all users."""
    try:
        users = db.query(models.Users).all()
        logger.info(f"Retrieved {len(users)} users from the database.")
        return users
    except Exception as e:
        logger.error(f"Error getting all users: {e}", exc_info=True)
        raise

def get_user_by_username(db: Session, username: str)-> Optional[models.Users]:
    """Get a user by username."""
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if user:
        logger.info(f"User with username '{username}' found.")
    else:
        logger.info(f"User with username '{username}' not found.")
    return user

def get_user_role(db: Session, clerk_id: str) -> Optional[str]:
    """Get a user's role by clerk_id."""
    try:
        user = db.query(models.Users).filter(models.Users.clerk_id == clerk_id).first()
        if not user:
            raise ValueError(f"User with clerk_id '{clerk_id}' not found.")
        logger.info(f"User with clerk_id '{clerk_id}' found with role '{user.role}'.")
        return user.role
    except Exception as e:
        logger.error(f"Error getting user role by clerk_id '{clerk_id}': {e}", exc_info=True)
        raise
def get_user_by_id(db: Session, user_id: int) -> Optional[models.Users]:
    """Get a user by their ID."""
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        logger.debug(f"User with ID '{user_id}' found.")
    else:
        logger.debug(f"User with ID '{user_id}' not found.")
    return user 

def get_user_id_by_clerk_id(db: Session, clerk_id: str) -> Optional[int]:
    """Get a user's ID by clerk_id."""
    try:
        user = db.query(models.Users.id).filter(models.Users.clerk_id == clerk_id).first()
        if not user:
            raise ValueError(f"User with clerk_id '{clerk_id}' not found.")
        logger.info(f"User ID for clerk_id '{clerk_id}' found: {user.id}")
        return user.id
    except Exception as e:
        logger.error(f"Error getting user ID by clerk_id '{clerk_id}': {e}", exc_info=True)
        raise

def get_user_by_clerk_id(db: Session, clerk_id: str) -> Optional[models.Users]:
    """Get a user by clerk_id."""
    try:
        user = db.query(models.Users).filter(models.Users.clerk_id == clerk_id).first()
        if not user:
            raise ValueError(f"User with clerk_id '{clerk_id}' not found.")
        logger.info(f"User with clerk_id '{clerk_id}' found.")
        return user
    except Exception as e:
        logger.error(f"Error getting user by clerk_id '{clerk_id}': {e}", exc_info=True)
        raise
    
def update_username(db: Session, clerk_id: str, new_username: str) -> Optional[models.Users]:
    """Update a user's username."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)
        if not user:
            raise ValueError(f"User with clerk_id '{clerk_id}' not found.")
        user.username = new_username
        db.commit()
        db.refresh(user)
        logger.info(f"Username updated for user with clerk_id '{clerk_id}'.")
        return user
    except Exception as e:
        logger.error(f"Error updating username for clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise
def update_native_language(db: Session, clerk_id: str, new_native_language: str) -> Optional[models.Users]:
    """Update a user's native language."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)
        if not user:
            raise ValueError(f"User with clerk_id '{clerk_id}' not found.")
        user.native_language = new_native_language
        db.commit()
        db.refresh(user)
        logger.info(f"Native language updated for user with clerk_id '{clerk_id}'.")
        return user
    except Exception as e:
        logger.error(f"Error updating native language for clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise

def update_preferred_language(db: Session, clerk_id: str, new_preferred_language: str) -> models.Users:
    """Update a user's preferred language."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)
        if not user:
            raise ValueError(f"User with clerk_id '{clerk_id}' not found.")
        user.preferred_language = new_preferred_language
        db.commit()
        db.refresh(user)
        logger.info(f"Preferred language updated for user with clerk_id '{clerk_id}'.")
        return user
    except Exception as e:
        logger.error(f"Error updating preferred language for clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_user(db: Session, clerk_id: str) -> bool:
    """Delete a user by clerk_id."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)
        if not user:
            raise ValueError(f"User with clerk_id '{clerk_id}' not found.")
        db.delete(user)
        db.commit()
        logger.info(f"User with clerk_id '{clerk_id}' deleted.")
        return True
    except Exception as e:
        logger.error(f"Error deleting user with clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise