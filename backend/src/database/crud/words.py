from core.word import Word
from sqlalchemy.orm import Session
from .. import models
import logging
import re
from backend.src.schemas.word import WordCreate
from typing import List, Optional

logger = logging.getLogger(__name__)


def add_word(db: Session, word: Word) -> models.Words:
    """Add a new word."""
    if word is None:
        raise ValueError("Word is required")
    try:
        existing_word = db.query(models.Words).filter(models.Words.word == word.word).first()
        if existing_word:
            logger.info(f"Word '{word.word}' already exists in the database.")
            return existing_word

        db_word = models.Words(
            word=word.word.lower(),
            language=word.language,
            frequency=word.frequency,
            audio_url=word.audio_url if hasattr(word, "audio_url") else None,
        )
        db.add(db_word)
        db.flush()

        logger.info(f"Word '{word.word}' added to database. ")
        for lang, translation in word.translation.items():
            if translation:
                for t in word.translation[lang]:
                    db_translation = models.Translations(
                        word_id=db_word.id, language=lang, translation=t
                    )
                    db.add(db_translation)
                    logger.info(
                        f"Translation '{t}' added for language '{lang}' for word '{word.word}'."
                    )

        for synonym in word.synonyms:
            db_synonym = models.Synonyms(word_id=db_word.id, synonym=synonym)

            db.add(db_synonym)
            logger.info(f"Synonym '{synonym}' added for word '{word.word}'.")

        for part_of_speech, definitions in word.definition.items():
            for definition in definitions:
                db_definition = models.Definitions(
                    word_id=db_word.id, part_of_speech=part_of_speech, definition=definition
                )
                db.add(db_definition)
                logger.info(
                    f"Definition '{definition}' added for part of speech '{part_of_speech}' \\\
                        for word '{word.word}'."
                )

        for part_of_speech, example in word.examples.items():
            for ex in example:
                pattern = r"\b" + re.escape(db_word.word) + r"\b.*"
                if not re.search(pattern, ex, re.IGNORECASE):
                    logger.warning(f"Example '{ex}' does not contain the word '{word.word}'.")
                    continue

                db_example = models.Examples(
                    word_id=db_word.id, part_of_speech=part_of_speech, example=ex
                )
                db.add(db_example)
                logger.info(
                    f"Example '{ex}' added for part of speech '{part_of_speech}' \\\
                        for word '{word.word}'."
                )

        for tag in word.tags:
            db_tag = models.Tags(word_id=db_word.id, tag=tag)
            db.add(db_tag)
            logger.info(f"Tag '{tag}' added for word '{word.word}'.")

        for warning in word.warnings:
            db_warning = models.Warnings(word_id=db_word.id, warning_message=warning)
            db.add(db_warning)
            logger.info(f"Warning '{warning}' added for word '{word.word}'.")

        db.commit()
        logger.info(f"Word '{word.word}' added successfully .")
        return db_word

    except Exception as e:
        logger.debug(f"Error adding word '{word.word}': {e}", exc_info=True)
        db.rollback()
        raise


def get_all_words_from_db(db: Session) -> List[models.Words]:
    """Get all words for a specific user."""
    try:
        words = db.query(models.Words).all()
        return words
    except Exception as e:
        logger.debug(f"Error getting all words: {e}", exc_info=True)
        raise


def get_word_id_by_word(db: Session, word: str) -> Optional[int]:
    """Get the ID of a word."""
    try:
        word_entry = db.query(models.Words.id).filter(models.Words.word == word.strip()).first()
        if word_entry:
            logger.info(f"Found ID for word '{word}': {word_entry.id}")
            return word_entry.id
        else:
            raise ValueError(f"Word '{word}' not found in the database.")
    except Exception as e:
        logger.debug(f"Error getting word ID by word '{word}': {e}", exc_info=True)
        raise


def get_word_by_id(db: Session, word_id: int) -> Optional[models.Words]:
    """Get a word by its ID."""
    try:
        word_entry = db.query(models.Words).filter(models.Words.id == word_id).first()
        if word_entry:
            logger.info(f"Word found for ID '{word_id}': {word_entry.word}")
            return word_entry
        else:
            raise ValueError(f"Word with ID '{word_id}' not found.")
    except Exception as e:
        logger.debug(f"Error getting word by ID '{word_id}': {e}", exc_info=True)
        raise


def get_words_count(db: Session) -> int:
    """Get the total number of words added by a specific user."""
    try:
        count = db.query(models.Words).count()
        logger.info(f"Total words count: {count}.")
        return count
    except Exception as e:
        logger.debug(f"Error getting total words count: {e}", exc_info=True)
        raise


def get_words_by_language(db: Session, language: str) -> List[models.Words]:
    """Get words by language."""
    try:
        words = db.query(models.Words).filter(models.Words.language == language).all()
        logger.info(f"Found {len(words)} words for language '{language}'.")
        return words
    except Exception as e:
        logger.debug(f"Error getting words by language '{language}': {e}", exc_info=True)
        raise


def get_word_audio_url(db: Session, word_id: int) -> Optional[str]:
    """Get the audio URL for a specific word by its ID."""
    try:
        word_entry = db.query(models.Words).filter(models.Words.id == word_id).first()
        if word_entry and word_entry.audio_url:
            logger.info(f"Audio URL found for word ID '{word_id}': {word_entry.audio_url}")
            return word_entry.audio_url
        else:
            logger.warning(f"No audio URL found for word ID '{word_id}'.")
            return None
    except Exception as e:
        logger.debug(f"Error getting audio URL for word ID '{word_id}': {e}", exc_info=True)
        raise

def get_word_by_text(db: Session, word_text: str) -> Optional[models.Words]:
    """Get a word by its text."""
    try:
        word_entry = db.query(models.Words).filter(models.Words.word == word_text.strip()).first()
        if word_entry:
            logger.info(f"Word found for text '{word_text}': ID {word_entry.id}")
            return word_entry
        else:
            raise ValueError(f"Word '{word_text}' not found in the database.")
    except Exception as e:
        logger.debug(f"Error getting word by text '{word_text}': {e}", exc_info=True)
        raise

def get_word_frequency(db: Session, word_id: int) -> Optional[float]:
    """Get the frequency for a specific word by its ID."""
    try:
        word_entry = db.query(models.Words).filter(models.Words.id == word_id).first()
        if word_entry and word_entry.frequency is not None:
            logger.info(f"Frequency found for word ID '{word_id}': {word_entry.frequency}")
            return word_entry.frequency
        else:
            logger.warning(f"No frequency found for word ID '{word_id}'.")
            return 0.0
    except Exception as e:
        logger.debug(f"Error getting frequency for word ID '{word_id}': {e}", exc_info=True)
        raise


def search_words(db: Session, query: str, skip: int = 0, limit: int = 50) -> List[models.Words]:
    """Search words by partial text match."""
    try:
        return (
            db.query(models.Words)
            .filter(models.Words.word.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )
    except Exception as e:
        logger.error(f"Error searching words: {e}", exc_info=True)
        raise


# ============================================================================
# 🔒 IMMUTABILITY ENFORCEMENT - NO UPDATE/DELETE FUNCTIONS
# ============================================================================
# Words are immutable - once created, they cannot be modified or deleted
# This is by design to maintain data integrity
# ============================================================================
