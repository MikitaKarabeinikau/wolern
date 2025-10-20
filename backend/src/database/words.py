from sqlalchemy.orm import Session
from . import models
from ...schemas import Word
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)

def get_all_words_from_db(db: Session, clerk_id: str):
    """Get all words for a specific user."""
    try:
        words = db.query(models.Words).filter(models.Words.added_by_user_id == clerk_id).all()
        logger.info(f"Found {len(words)} words for user '{clerk_id}'.")
        return words
    except Exception as e:
        logger.error(f"Error getting all words for user '{clerk_id}': {e}", exc_info=True)
        raise

def get_word_id_by_word(db: Session, word: str):
    """Get the ID of a word."""
    try:
        word_entry = db.query(models.Words.id).filter(models.Words.word == word.strip()).first()
        if word_entry:
            logger.info(f"Found ID for word '{word}': {word_entry.id}")
            return word_entry.id
        else:
            logger.warning(f"Word '{word}' not found.")
            return None
    except Exception as e:
        logger.error(f"Error getting word ID by word '{word}': {e}", exc_info=True)
        raise

def get_word_by_id(db: Session, word_or_id: str, clerk_id: str):
    """Get a word by its ID or word, ensuring the user has permission."""
    try:
        if isinstance(word_or_id, int) or (isinstance(word_or_id, str) and word_or_id.isdigit()):
            word_id = int(word_or_id)
            word = db.query(models.Words).filter(models.Words.id == word_id, models.Words.added_by_user_id == clerk_id).first()
        else:
            word = db.query(models.Words).filter(models.Words.word == word_or_id.strip(), models.Words.added_by_user_id == clerk_id).first()

        if word:
            logger.info(f"Found word '{word.word}' for user '{clerk_id}'.")
            return word
        else:
            logger.warning(f"Word with ID/word '{word_or_id}' not found for user '{clerk_id}', or user does not have permission.")
            return None
    except Exception as e:
        logger.error(f"Error getting word by ID/word '{word_or_id}' for user '{clerk_id}': {e}", exc_info=True)
        raise

def get_user_vocabularies(db: Session, user_id: str):
    """Get all vocabularies for a specific user."""
    try:
        vocabularies = db.query(models.Words.vocabulary).filter(models.Words.added_by_user_id == user_id).group_by(models.Words.vocabulary).all()
        result = [v[0] for v in vocabularies]
        logger.info(f"Found {len(result)} vocabularies for user '{user_id}'.")
        return result
    except Exception as e:
        logger.error(f"Error getting vocabularies for user '{user_id}': {e}", exc_info=True)
        raise

def add_word(db: Session, word: Word, clerk_id: str):
    """Add a new word."""
    if word is None:
        raise ValueError("Word is required")
    try:
        if any(w.word == word.word for w in get_all_words_from_db(db, clerk_id)):
            raise ValueError("Word already exists in the database")

        db_word = models.Words(
            word=word.word,
            added_by_user_id=clerk_id,
            frequency=word.frequency,
            difficulty=word.difficulty
        )

        db.add(db_word)
        db.commit()
        db.refresh(db_word)
        logger.info(f"Word '{word.word}' added to database for user '{clerk_id}'.")

        for lang, translation in word.translation.items():
            if translation:
                for t in word.translation[lang]:
                    db_translation = models.Translation(
                        word_id=db_word.id,
                        language=lang,
                        translation=t
                    )
                    db.add(db_translation)
                    logger.info(f"Translation '{t}' added for language '{lang}' for word '{word.word}'.")

        for synonym in word.synonyms:
            db_synonym = models.Synonym(
                word_id=db_word.id,
                synonym=synonym
            )
            db.add(db_synonym)
            logger.info(f"Synonym '{synonym}' added for word '{word.word}'.")

        for part_of_speech, definitions in word.definition.items():
            for definition in definitions:
                db_definition = models.Definition(
                    word_id=db_word.id,
                    part_of_speech=part_of_speech,
                    definition=definition
                )
                db.add(db_definition)
                logger.info(f"Definition '{definition}' added for part of speech '{part_of_speech}' for word '{word.word}'.")

        for part_of_speech, example in word.examples.items():
            for ex in example:
                db_example = models.Example(
                    word_id=db_word.id,
                    part_of_speech=part_of_speech,
                    example_sentence=ex
                )
                db.add(db_example)
                logger.info(f"Example '{ex}' added for part of speech '{part_of_speech}' for word '{word.word}'.")

        for tag in word.tags:
            db_tag = models.Tag(
                word_id=db_word.id,
                tag=tag
            )
            db.add(db_tag)
            logger.info(f"Tag '{tag}' added for word '{word.word}'.")

        for warning in word.warnings:
            db_warning = models.Warning(
                word_id=db_word.id,
                warning_message=warning
            )
            db.add(db_warning)
            logger.info(f"Warning '{warning}' added for word '{word.word}'.")

        db.commit()
        return True

    except Exception as e:
        logger.error(f"Error adding word '{word.word}' for user '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_word(db: Session, word: str, clerk_id: str):
    """Delete a word."""
    try:
        word_to_delete = get_word_by_id(db, word, clerk_id)
        if word_to_delete:
            db.delete(word_to_delete)
            db.commit()
            logger.info(f"Word '{word}' deleted successfully for user '{clerk_id}'.")
            return True
        else:
            logger.warning(f"Word '{word}' not found for user '{clerk_id}', or user does not have permission.")
            return False
    except Exception as e:
        logger.error(f"Error deleting word '{word}' for user '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_word_by_id_from_db(db: Session, word_id: int, clerk_id: str):
    """Delete a word by its ID."""
    try:
        logger.info(f"Attempting to delete word with ID {word_id} for user {clerk_id}")
        word_to_delete = db.query(models.Words).filter(models.Words.id == word_id, models.Words.added_by_user_id == clerk_id).first()

        if word_to_delete:
            # Delete dependent rows explicitly to avoid nulling non-null FK columns
            db.query(models.Translation).filter(models.Translation.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Synonym).filter(models.Synonym.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Definition).filter(models.Definition.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Example).filter(models.Example.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Tag).filter(models.Tag.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Warning).filter(models.Warning.word_id == word_id).delete(synchronize_session=False)

            db.delete(word_to_delete)
            db.commit()
            logger.info(f"Word with ID {word_id} deleted successfully for user {clerk_id}.")
            return True
        else:
            logger.warning(f"Word with ID {word_id} not found for user {clerk_id}, or user does not have permission.")
            return False
    except Exception as e:
        logger.error(f"Error deleting word with ID {word_id} for user {clerk_id}: {e}", exc_info=True)
        db.rollback()
        raise