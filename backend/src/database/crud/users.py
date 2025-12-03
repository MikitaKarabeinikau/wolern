from sqlalchemy.orm import Session
from .. import models
import logging
from backend.src.config import settings
from typing import Optional, List
import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)
logger = logging.getLogger(__name__)


def create_user(
    db: Session,
    clerk_id: str,
    username: str = None,
    native_language: str = "polish",
    preferred_language: str = "english",
    email: str = None,
    role: str = "user",
) -> models.Users:
    """
    Create a new user and their associated exercise quota.

    Args:
        db: Database session
        clerk_id: Clerk user ID (required)
        username: Username (optional, defaults to email or clerk_id)
        native_language: User's native language (optional)
        preferred_language: User's preferred learning language (optional)
        email: User's email (optional)
        role: User role (defaults to "user")

    Returns:
        Created user object
    """
    try:

        admin_emails = os.getenv("ADMINS_EMAIL", "").split(",")
        admin_emails = [email.strip() for email in admin_emails if email.strip()]
        role = "admin" if email and email in admin_emails else "user"

        if not username:
            username = email if email else f"user_{clerk_id[:8]}"
            logger.info(f"No username provided, using fallback: {username}")

        db_user = models.Users(
            clerk_id=clerk_id,
            username=username,
            native_language=native_language,
            preferred_language=preferred_language,
            email=email,
            role=role,
        )



        db.add(db_user)
        db.flush()
        if role == "admin":
            user_quota = models.UserQuota(user_id=db_user.id, quota_remaining=settings.ADMIN_QUOTA)
            logger.info(f"Created admin user with quota: {settings.ADMIN_QUOTA}")
            db.add(user_quota)
        else:
            user_quota = models.UserQuota(user_id=db_user.id, quota_remaining=settings.DEFAULT_USER_QUOTA)
            logger.info(f"Created regular user with quota: {settings.DEFAULT_USER_QUOTA}")
            db.add(user_quota)

        logger.info(
            f"Successfully created user with clerk_id '{clerk_id}' and username '{username}'."
        )

        for default_vocab in settings.DEFAULT_VOCABULARIES:
            db_vocabulary = models.Vocabulary(user_id=db_user.id, name=default_vocab)
            db.add(db_vocabulary)
            logger.info(f"Default vocabulary '{default_vocab}' added for user_id '{db_user.id}'.")

        db.commit()
        db.refresh(db_user)

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


def get_user_by_id(db: Session, user_id: int) -> Optional[models.Users]:
    """Get a user by ID."""
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        logger.info(f"User with ID '{user_id}' found.")
    else:
        logger.info(f"User with ID '{user_id}' not found.")
    return user


def get_user_by_username(db: Session, username: str) -> Optional[models.Users]:
    """Get a user by username."""
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if user:
        logger.info(f"User with username '{username}' found.")
    else:
        logger.info(f"User with username '{username}' not found.")
    return user


def get_user_id_by_clerk_id(db: Session, clerk_id: str) -> Optional[int]:
    """Get a user's ID by clerk_id."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)

        if not user:
            logger.warning(f"User with clerk_id '{clerk_id}' not found.")
            return None

        logger.info(f"User with clerk_id '{clerk_id}' found with ID '{user.id}'.")
        return user.id

    except Exception as e:
        logger.error(f"Error getting user ID by clerk_id '{clerk_id}': {e}", exc_info=True)
        raise

def get_preferred_language_by_user_id(db: Session, user_id: int) -> Optional[str]:
    """Get a user's preferred language by user ID."""
    try:
        user = get_user_by_id(db, user_id)

        if not user:
            logger.warning(f"User with user_id '{user_id}' not found.")
            return None

        logger.info(
            f"User with user_id '{user_id}' found with preferred language '{user.preferred_language}'."
        )
        return user.preferred_language

    except Exception as e:
        logger.error(
            f"Error getting preferred language by clerk_id '{clerk_id}': {e}", exc_info=True
        )
        raise

def get_native_language_by_user_id(db: Session, user_id: int) -> Optional[str]:
    """Get a user's native language by user ID."""
    try:
        user = get_user_by_id(db, user_id)

        if not user:
            logger.warning(f"User with user_id '{user_id}' not found.")
            return None

        logger.info(
            f"User with user_id '{user_id}' found with native language '{user.native_language}'."
        )
        return user.native_language

    except Exception as e:
        logger.error(
            f"Error getting native language by user_id '{user_id}': {e}", exc_info=True
        )
        raise

def get_user_role(db: Session, clerk_id: str) -> Optional[str]:
    """Get a user's role by clerk_id."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)

        if not user:
            logger.warning(f"User with clerk_id '{clerk_id}' not found.")
            return None

        logger.info(f"User with clerk_id '{clerk_id}' found with role '{user.role}'.")
        return user.role

    except Exception as e:
        logger.error(f"Error getting user role by clerk_id '{clerk_id}': {e}", exc_info=True)
        raise


def get_user_by_clerk_id(db: Session, clerk_id: str) -> Optional[models.Users]:
    """
    Get a user by clerk_id.

    Returns:
        User object if found, None if not found.
    """
    try:
        user = db.query(models.Users).filter(models.Users.clerk_id == clerk_id).first()

        if user:
            logger.info(f"User with clerk_id '{clerk_id}' found.")
        else:
            logger.info(f"User with clerk_id '{clerk_id}' not found.")

        return user

    except Exception as e:
        logger.error(f"Error getting user by clerk_id '{clerk_id}': {e}", exc_info=True)
        raise


def update_username(db: Session, clerk_id: str, new_username: str) -> Optional[models.Users]:
    """Update a user's username."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)

        if not user:
            logger.warning(f"User with clerk_id '{clerk_id}' not found.")
            return None

        user.username = new_username
        db.commit()
        db.refresh(user)
        logger.info(f"Username updated to '{new_username}' for user with clerk_id '{clerk_id}'.")
        return user

    except Exception as e:
        logger.error(f"Error updating username for clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise


def update_native_language(
    db: Session, clerk_id: str, new_native_language: str
) -> Optional[models.Users]:
    """Update a user's native language."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)

        if not user:
            logger.warning(f"User with clerk_id '{clerk_id}' not found.")
            return None

        user.native_language = new_native_language
        db.commit()
        db.refresh(user)
        logger.info(
            f"Native language updated to '{new_native_language}' \\\
                for user with clerk_id '{clerk_id}'."
        )
        return user

    except Exception as e:
        logger.error(
            f"Error updating native language for clerk_id '{clerk_id}': {e}", exc_info=True
        )
        db.rollback()
        raise


def update_preferred_language(
    db: Session, clerk_id: str, new_preferred_language: str
) -> Optional[models.Users]:
    """Update a user's preferred language."""
    try:
        user = get_user_by_clerk_id(db, clerk_id)

        if not user:
            logger.warning(f"User with clerk_id '{clerk_id}' not found.")
            return None

        user.preferred_language = new_preferred_language
        db.commit()
        db.refresh(user)
        logger.info(
            f"Preferred language updated to '{new_preferred_language}' \\\
                for user with clerk_id '{clerk_id}'."
        )
        return user

    except Exception as e:
        logger.error(
            f"Error updating preferred language for clerk_id '{clerk_id}': {e}", exc_info=True
        )
        db.rollback()
        raise


def delete_user(db: Session, clerk_id: str) -> bool:
    """
    Delete a user by clerk_id.

    Returns:
        True if deleted, False if user not found.
    """
    try:
        user = get_user_by_clerk_id(db, clerk_id)

        if not user:
            logger.warning(f"User with clerk_id '{clerk_id}' not found for deletion.")
            return False

        db.delete(user)
        db.commit()
        logger.info(f"User with clerk_id '{clerk_id}' deleted successfully.")
        return True

    except Exception as e:
        logger.error(f"Error deleting user with clerk_id '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise
