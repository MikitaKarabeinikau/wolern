from sqlalchemy.orm import Session
from .. import models
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


def create_warning(db: Session, word_id: int, warning: str) -> models.Warnings:
    """Create a new warning for a word (immutable)."""
    try:
        # Verify word exists
        word = db.query(models.Words).filter(models.Words.id == word_id).first()
        if not word:
            raise ValueError(f"Word ID {word_id} does not exist")
        
        new_warning = models.Warnings(
            word_id=word_id,
            warning_message=warning
        )
        db.add(new_warning)
        db.commit()
        db.refresh(new_warning)
        
        logger.info(f"Created warning ID {new_warning.id} for word ID {word_id}")
        return new_warning
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error creating warning: {e}", exc_info=True)
        db.rollback()
        raise


def get_warning_by_id(db: Session, warning_id: int) -> Optional[models.Warnings]:
    """Get a warning by its ID."""
    try:
        return db.query(models.Warnings).filter(
            models.Warnings.id == warning_id
        ).first()
    except Exception as e:
        logger.error(f"Error getting warning: {e}", exc_info=True)
        raise


def get_word_warnings(db: Session, word_id: int) -> List[models.Warnings]:
    """Get all warnings for a word."""
    try:
        return db.query(models.Warnings).filter(
            models.Warnings.word_id == word_id
        ).all()
    except Exception as e:
        logger.error(f"Error getting word warnings: {e}", exc_info=True)
        raise


def count_word_warnings(db: Session, word_id: int) -> int:
    """Count warnings for a word."""
    try:
        return db.query(models.Warnings).filter(
            models.Warnings.word_id == word_id
        ).count()
    except Exception as e:
        logger.error(f"Error counting warnings: {e}", exc_info=True)
        raise


# 🔒 IMMUTABLE - No update/delete functions