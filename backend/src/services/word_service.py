from typing import Optional

from backend.src.database import models

from sqlalchemy.orm import Session, joinedload

def get_full_word_data_by_word(db: Session, word: str) -> Optional[models.Words]:
    """
    Get complete word data with all relationships eagerly loaded.

    Returns SQLAlchemy model with all relationships loaded in a single query.
    """
    return (
        db.query(models.Words)
        .options(
            joinedload(models.Words.definitions),
            joinedload(models.Words.examples),
            joinedload(models.Words.synonyms),
            joinedload(models.Words.translations),
            joinedload(models.Words.tags),
            joinedload(models.Words.warnings)
        )
        .filter(models.Words.word == word.lower())
        .first()
    )
