from database.crud.users import get_preferred_language_by_user_id
from database.crud.vocabulary import get_user_by_vocabulary_id
from database.crud.vocabulary_words import create_vocabulary_word
from database.crud.words import add_word
from services.word_service import get_full_word_data_by_id
from backend.src.core.word import Word
from sqlalchemy.orm import Session
from backend.src.database import models
import logging
from backend.src.schemas.word import WordWithFullDataResponse

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

def create_vocabulary_word_secure(db: Session, vocabulary_id: int, word: models.Words) -> models.VocabularyWords:
    """Create a vocabulary word securely by checking user ownership."""
    user = get_user_by_vocabulary_id(db, vocabulary_id)
    if not user:
        raise ValueError("Vocabulary does not belong to any user.")
    preferred_language = get_preferred_language_by_user_id(db, user.id)
    vocab_word = create_vocabulary_word(db, vocabulary_id, word.id)
    return vocab_word

def delete_word_from_vocabulary_secure(db: Session, vocabulary_id: int, word_id: int):
    """Delete a word from a vocabulary securely by checking user ownership."""
    user = get_user_by_vocabulary_id(db, vocabulary_id)
    if not user:
        raise ValueError("Vocabulary does not belong to any user.")
    vocab_word = (
        db.query(models.VocabularyWords)
        .filter(
            models.VocabularyWords.vocabulary_id == vocabulary_id,
            models.VocabularyWords.word_id == word_id
        )
        .first()
    )
    if not vocab_word:
        raise ValueError("Word not found in the specified vocabulary.")
    db.delete(vocab_word)
    db.commit()
    return vocab_word

def get_all_vocabulary_words_by_vocabulary_id(db: Session, vocabulary_id: int) -> list[models.VocabularyWords]:
    """Get all vocabulary words for a specific vocabulary ID."""
    vocab_words = (
        db.query(models.VocabularyWords)
        .filter(models.VocabularyWords.vocabulary_id == vocabulary_id)
        .all()
    )
    return vocab_words

def get_all_words_in_vocabulary_with_data(db: Session, vocabulary_id: int) -> list[dict]:
    """Get all words in a vocabulary along with their data."""
    vocab_words = get_all_vocabulary_words_by_vocabulary_id(db, vocabulary_id)
    words_data = {}
    for vocab_word in vocab_words:
        word_data = get_full_word_data_by_id(db, vocab_word.word_id)
        word_schema = WordWithFullDataResponse.model_validate(word_data)
        words_data[word_schema.word] = word_schema.model_dump()
    return words_data
