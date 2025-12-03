from database.crud.users import get_preferred_language_by_user_id
from database.crud.vocabulary import get_user_by_vocabulary_id
from database.crud.vocabulary_words import create_vocabulary_word
from database.crud.words import add_word
from backend.src.core.word import Word
from sqlalchemy.orm import Session
from backend.src.database import models
import logging

logger = logging.getLogger(__name__)

def add_new_vocabulary_word(db: Session, word: Word, vocabulary_id: int) -> models.VocabularyWords:
    """Add a new vocabulary word to the database."""
    try:
        #Check if the word already exists in the base words table
        existing_word = db.query(models.Words).filter(models.Words.word == word.word).first()
        #If not, create it
        if not existing_word:
            new_word = add_word(db, word)
        #Get the word ID from existing or newly created word
        word_id = existing_word.id if existing_word else new_word.id
        # Check if the vocabulary word already exists
        existing_vocab_word = (
            db.query(models.VocabularyWords)
            .filter(
                models.VocabularyWords.vocabulary_id == vocabulary_id,
                models.VocabularyWords.word_id == word_id,
            )
            .first()
        )
        if existing_vocab_word:
            logger.info(f"Vocabulary word '{word}' already exists in vocabulary_id '{vocabulary_id}'.")
            return existing_vocab_word
        db_vocab_word = create_vocabulary_word(db, vocabulary_id, word_id)
        db.add(db_vocab_word)
        logger.info(f"Vocabulary word '{word}' added to session.")
        db.commit()
        db.refresh(db_vocab_word)
        return db_vocab_word
    except Exception as e:
        logger.error(f"Error adding vocabulary word '{word}' in vocabulary_id '{vocabulary_id}': {e}", exc_info=True)
        db.rollback()
        raise
