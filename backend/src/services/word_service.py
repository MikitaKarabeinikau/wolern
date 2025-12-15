from typing import Optional

from backend.src.database.crud.words import get_word_by_id

from backend.src.database import models

from sqlalchemy.orm import Session, joinedload
import logging

logger = logging.getLogger(__name__)

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

def get_full_word_data_by_id(db: Session, word_id: int) -> Optional[models.Words]:
    """
    Get complete word data by ID with all relationships eagerly loaded.

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
        .filter(models.Words.id == word_id)
        .first()
    )

def is_word_in_user_vocabularies(db: Session, user_id: int, word_id: int) -> bool:
    """
    Check if a word is present in the user's vocabularies.

    Returns True if the word is found in the user's vocabularies, otherwise False.
    """

    result = (
        db.query(models.VocabularyWords)
        .join(models.Vocabulary, models.VocabularyWords.vocabulary_id == models.Vocabulary.vocabulary_id)
        .filter(models.Vocabulary.user_id == user_id, models.VocabularyWords.word_id == word_id)
        .first()
    )

    return result is not None

def get_user_vocabularies_names_by_word_id(db: Session, user_id: int, word_id: int) -> list[str]:
    """
    Get the names of vocabularies that contain the specified word for a given user.

    Returns a list of vocabulary names.
    """

    vocabularies = (
        db.query(models.Vocabulary.name)
        .join(models.VocabularyWords, models.Vocabulary.vocabulary_id == models.VocabularyWords.vocabulary_id)
        .filter(models.Vocabulary.user_id == user_id, models.VocabularyWords.word_id == word_id)
        .all()
    )

    return [vocabulary.name for vocabulary in vocabularies]

def get_number_of_user_vocabularies_containing_word(db: Session, user_id: int, word_id: int) -> int:
    """
    Get the number of vocabularies that contain the specified word for a given user.

    Returns the count of vocabularies.
    """

    count = (
        db.query(models.VocabularyWords)
        .join(models.Vocabulary, models.VocabularyWords.vocabulary_id == models.Vocabulary.vocabulary_id)
        .filter(models.Vocabulary.user_id == user_id, models.VocabularyWords.word_id == word_id)
        .count()
    )

    return count

def get_word_relations_with_user_vocabularies(db: Session, user_id: int, word_id: int) -> list[models.VocabularyWords]:
    """
    Get VocabularyWords relations for a specific word that belong to the user's vocabularies.

    Returns a list of VocabularyWords entries.
    """

    relations = {
        "word_id": word_id,
        "word": get_word_by_id(db, word_id).word,
        "vocabulary_count": get_number_of_user_vocabularies_containing_word(db, user_id, word_id),
        "vocabulary_names": get_user_vocabularies_names_by_word_id(db, user_id, word_id)

    }
    return relations

def change_vocabulary(db: Session, word_id, new_vocabulary_id: int, old_vocabulary_id: int):
    """
    Change the vocabulary association of a word from old_vocabulary_id to new_vocabulary_id.
    """
    word = get_word_by_id(db, word_id)
    if not word:
        raise ValueError(f"Word with ID '{word_id}' not found.")
    create_vocabulary_word = models.VocabularyWords(
        vocabulary_id=new_vocabulary_id,
        word_id=word_id
    )
    db.add(create_vocabulary_word)
    delete_vocabulary_word = (
        db.query(models.VocabularyWords)
        .filter(
            models.VocabularyWords.vocabulary_id == old_vocabulary_id,
            models.VocabularyWords.word_id == word_id
        )
        .first()
    )
    if delete_vocabulary_word:
        db.delete(delete_vocabulary_word)
    db.commit()
    return create_vocabulary_word

def get_word_translations(db: Session, word_id: int) -> Optional[models.Words]:
    """
    Get complete word data with translations eagerly loaded.

    Returns SQLAlchemy model with translations relationship loaded in a single query.
    """
    try:
        return (
            db.query(models.Words)
            .options(
                joinedload(models.Words.translations)
            )
            .filter(models.Words.id == word_id)
            .first()
        )
    except Exception as e:
        logger.error(
            f"Error fetching word translations for word_id '{word_id}': {e}"
        )
        logger.debug(
            f"Stack trace:", exc_info=True)
        raise

def get_word_examples(db: Session, word_id: int) -> Optional[models.Words]:
    """
    Get complete word data with examples eagerly loaded.

    Returns SQLAlchemy model with examples relationship loaded in a single query.
    """
    try:
        return (
            db.query(models.Words)
            .options(
                joinedload(models.Words.examples)
            )
            .filter(models.Words.id == word_id)
            .first()
        )
    except Exception as e:
        logger.error(
            f"Error fetching word examples for word_id '{word_id}': {e}"
        )
        logger.debug(
            f"Stack trace:", exc_info=True)
        raise

def get_word_definitions(db: Session, word_id: int) -> Optional[models.Words]:
    """
    Get complete word data with definitions eagerly loaded.

    Returns SQLAlchemy model with definitions relationship loaded in a single query.
    """
    try:
        return (
            db.query(models.Words)
            .options(
                joinedload(models.Words.definitions)
            )
            .filter(models.Words.id == word_id)
            .first()
        )
    except Exception as e:
        logger.error(
            f"Error fetching word definitions for word_id '{word_id}': {e}"
        )
        logger.debug(
            f"Stack trace:", exc_info=True)
        raise

def get_word_synonyms(db: Session, word_id: int) -> Optional[models.Words]:
    """
    Get complete word data with synonyms eagerly loaded.

    Returns SQLAlchemy model with synonyms relationship loaded in a single query.
    """
    try:
        return (
            db.query(models.Words)
            .options(
                joinedload(models.Words.synonyms)
            )
            .filter(models.Words.id == word_id)
            .first()
        )
    except Exception as e:
        logger.error(
            f"Error fetching word synonyms for word_id '{word_id}': {e}"
        )
        logger.debug(
            f"Stack trace:", exc_info=True)
        raise

def get_word_tags(db: Session, word_id: int) -> Optional[models.Words]:
    """
    Get complete word data with tags eagerly loaded.

    Returns SQLAlchemy model with tags relationship loaded in a single query.
    """
    try:
        return (
            db.query(models.Words)
            .options(
                joinedload(models.Words.tags)
            )
            .filter(models.Words.id == word_id)
            .first()
        )
    except Exception as e:
        logger.error(
            f"Error fetching word tags for word_id '{word_id}': {e}"
        )
        logger.debug(
            f"Stack trace:", exc_info=True)
        raise
