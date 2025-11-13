from sqlalchemy.orm import Session
from . import models
from backend.schemas import AddWordRequest
import logging
logger = logging.getLogger(__name__)
from .warnings import get_number_of_warnings_for_word
from .base import get_last_word_base_id,get_translations_from_base, is_word_in_base, get_word_base_id, get_definitions_from_base, get_synonyms_from_base, get_examples_from_base
import re


def add_word(db: Session, word: AddWordRequest, clerk_id: str):
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

        if is_word_in_base(db, word.word):
            logger.info(f"Word '{word.word}' found in base words.")
            word_base_id = get_word_base_id(db, word.word)
            print("\n\n\n",get_translations_from_base(db, word_base_id),"\n\n\n")
            for base_translation in get_translations_from_base(db, word_base_id):
                db_translation = models.Translation(
                    word_id=db_word.id,
                    language=base_translation.language,
                    translation=base_translation.translation
                )
                db.add(db_translation)
                logger.info(f"Base translation '{base_translation.translation}' added for language '{base_translation.language}' for word '{word.word}'.")
            for base_definition in get_definitions_from_base(db, word_base_id):
                db_definition = models.Definition(
                    word_id=db_word.id,
                    part_of_speech=base_definition.part_of_speech,
                    definition=base_definition.definition
                )
                db.add(db_definition)
                logger.info(f"Base definition '{base_definition.definition}' added for part of speech '{base_definition.part_of_speech}' for word '{word.word}'.")
            for base_synonym in get_synonyms_from_base(db, word_base_id):
                db_synonym = models.Synonym(
                    word_id=db_word.id,
                    synonym=base_synonym.synonym
                )
                db.add(db_synonym)
                logger.info(f"Base synonym '{base_synonym.synonym}' added for word '{word.word}'.")
            for base_example in get_examples_from_base(db, word_base_id):
                db_example = models.Example(
                    word_id=db_word.id,
                    part_of_speech=base_example.part_of_speech,
                    example_sentence=base_example.example_sentence
                )
                db.add(db_example)
                logger.info(f"Base example '{base_example.example_sentence}' added for part of speech '{base_example.part_of_speech}' for word '{word.word}'.")
            db.commit()
            return True
        
        db_word_base = models.Word_Base(
            word=word.word
        )
        db.add(db_word_base)
        db.flush()

        for lang, translation in word.translation.items():
            if translation:
                for t in word.translation[lang]:
                    db_translation = models.Translation(
                        word_id=db_word.id,
                        language=lang,
                        translation=t
                    )
                    db_translation_base = models.Translation_Base(
                        base_id=db_word_base.id,
                        language=lang,
                        translation=t
                    )
                    db.add(db_translation)
                    db.add(db_translation_base)
                    logger.info(f"Translation '{t}' added for language '{lang}' for word '{word.word}'.")

        for synonym in word.synonyms:
            db_synonym = models.Synonym(
                word_id=db_word.id,
                synonym=synonym
            )
            db_synonym_base = models.Synonym_Base(
                base_id=db_word_base.id,
                synonym=synonym
            )
            db.add(db_synonym_base)
            db.add(db_synonym)
            logger.info(f"Synonym '{synonym}' added for word '{word.word}'.")

        for part_of_speech, definitions in word.definition.items():
            for definition in definitions:
                db_definition = models.Definition(
                    word_id=db_word.id,
                    part_of_speech=part_of_speech,
                    definition=definition
                )
                db_definition_base = models.Definition_Base(
                    base_id=db_word_base.id,
                    part_of_speech=part_of_speech,
                    definition=definition
                )
                db.add(db_definition_base)
                db.add(db_definition)
                logger.info(f"Definition '{definition}' added for part of speech '{part_of_speech}' for word '{word.word}'.")

        for part_of_speech, example in word.examples.items():
            for ex in example:
                pattern = r'\b' + re.escape(db_word.word) + r'\b.*'
                if not re.search(pattern, ex, re.IGNORECASE): 
                    logger.warning(f"Example '{ex}' does not contain the word '{word.word}'.")
                    continue

                db_example = models.Example(
                    word_id=db_word.id,
                    part_of_speech=part_of_speech,
                    example_sentence=ex
                )
                db_example_base = models.Example_Base(
                    base_id=db_word_base.id,
                    part_of_speech=part_of_speech,
                    example_sentence=ex
                )
                db.add(db_example_base)
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
        db_user_progress = models.User_Quiz_Progress(
            user_id=clerk_id,
            word_id=db_word.id
        )
        db.add(db_user_progress)
        
        

        db.commit()
        logger.info(f"Word '{word.word}' added successfully for user '{clerk_id}'.")
        if get_number_of_warnings_for_word(db, db_word.id) >= 3:
            logger.warning(f"Word '{word.word}' has warnings associated with it.")
            db_word.vocabulary = "strange"
            db.commit()
        return True

    except Exception as e:
        logger.error(f"Error adding word '{word.word}' for user '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise


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
        result = set([v[0] for v in vocabularies])
        logger.info(f"Found {len(result)} vocabularies for user '{user_id}'.")
        return result
    except Exception as e:
        logger.error(f"Error getting vocabularies for user '{user_id}': {e}", exc_info=True)
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
                    # Find all exercise IDs related to the word first
                    exercise_ids_to_delete = [e.id for e in db.query(models.Exercise.id).filter(models.Exercise.word_id == word_id).all()]

        if word_to_delete:
            # Delete dependent rows explicitly to avoid nulling non-null FK columns
            db.query(models.Translation).filter(models.Translation.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Synonym).filter(models.Synonym.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Definition).filter(models.Definition.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Example).filter(models.Example.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Tag).filter(models.Tag.word_id == word_id).delete(synchronize_session=False)
            db.query(models.Warning).filter(models.Warning.word_id == word_id).delete(synchronize_session=False)
            db.query(models.User_Quiz_Progress).filter(models.User_Quiz_Progress.word_id == word_id, models.User_Quiz_Progress.user_id == clerk_id).delete(synchronize_session=False)
            db.query(models.Exercise).filter(models.Exercise.id.in_(exercise_ids_to_delete)).delete(synchronize_session=False)
            db.query(models.MultipleChoiceExercise).filter(models.MultipleChoiceExercise.exercise_id.in_(exercise_ids_to_delete)).delete(synchronize_session=False)
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



def change_word_vocabulary(db: Session, word_id: int, new_vocabulary: str, clerk_id: str):
    """Change the vocabulary of a word."""
    try:
        word = get_word_by_id(db, word_id, clerk_id)
        if word:
            word.vocabulary = new_vocabulary
            db.commit()
            logger.info(f"Vocabulary for word with ID '{word_id}' changed to '{new_vocabulary}' by user '{clerk_id}'.")
            return True
        else:
            logger.warning(f"Word with ID '{word_id}' not found for user '{clerk_id}', or user does not have permission.")
            return False
    except Exception as e:
        logger.error(f"Error changing vocabulary for word with ID '{word_id}' for user '{clerk_id}': {e}", exc_info=True)
        db.rollback()
        raise

def delete_word(db: Session, word: str, clerk_id: str):
    """Delete a word."""
    try:
        logger.info(f"Attempting to delete word '{word}' for user '{clerk_id}'.")
        word_to_delete = get_word_by_id(db, word, clerk_id)
        if word_to_delete:
            logger.info(f"Word to delete: {word_to_delete.word}, ID: {word_to_delete.id}")
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