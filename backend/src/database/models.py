from sqlalchemy import JSON, Integer, String, Column, DateTime, UniqueConstraint, create_engine, func,text,ForeignKey,Float,event, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime,timezone
from .database import Base, engine



class Words(Base):
    __tablename__ = 'words'
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True, nullable=False, unique=True)
    language = Column(String, nullable=False)
    audio_url = Column(String, nullable=True)
    frequency = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    definitions = relationship("Definitions", back_populates="word", cascade="all, delete-orphan")
    examples = relationship("Examples", back_populates="word", cascade="all, delete-orphan")
    synonyms = relationship("Synonyms", back_populates="word", cascade="all, delete-orphan")
    translations = relationship("Translations", back_populates="word", cascade="all, delete-orphan")
    tags = relationship("Tags", back_populates="word", cascade="all, delete-orphan")
    warnings = relationship("Warnings", back_populates="word", cascade="all, delete-orphan")
    vocabulary_words = relationship("VocabularyWords", back_populates="word")
    exercises = relationship("Exercise", back_populates="word")
    
    
    
class Definitions(Base):
    __tablename__ = 'definitions'
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id', ondelete="RESTRICT"), nullable=False)
    part_of_speech = Column(String, nullable=False)
    definition = Column(String, nullable=False)
    
    
    word = relationship("Words", back_populates="definitions")

class Examples(Base):
    __tablename__ = 'examples'
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id', ondelete="RESTRICT"), nullable=False)
    part_of_speech = Column(String, nullable=False)
    example = Column(String, nullable=False)
  
    
    word = relationship("Words", back_populates="examples")

class Synonyms(Base):
    __tablename__ = 'synonyms'
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id', ondelete="RESTRICT"), nullable=False)
    synonym = Column(String, nullable=False)  

    
    word = relationship("Words", back_populates="synonyms")


class Tags(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id', ondelete="RESTRICT"), nullable=False)
    tag = Column(String, nullable=False)  

    
    word = relationship("Words", back_populates="tags")

class Translations(Base):
    __tablename__ = 'translations'
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id', ondelete="RESTRICT"), nullable=False)
    language = Column(String, nullable=False)
    translation = Column(String, nullable=False)

    
    word = relationship("Words", back_populates="translations")
    
class Warnings(Base):
    __tablename__ = 'warnings'
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id', ondelete="RESTRICT"), nullable=False)
    warning_message = Column(String, nullable=False)
    
    
    word = relationship("Words", back_populates="warnings")

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=True, default="user")
    native_language = Column(String, nullable=True, default="polish")
    preferred_language = Column(String, nullable=True, default="english")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    
    vocabulary = relationship("Vocabulary", back_populates="user", cascade="all, delete-orphan")
    quota = relationship("UserQuota", back_populates="user", cascade="all, delete-orphan", uselist=False)
    user_exercises = relationship("UserExercises", back_populates="user", cascade="all, delete-orphan")
    
class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    
    vocabulary_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    user = relationship("Users", back_populates="vocabulary")
    vocabulary_words = relationship("VocabularyWords", back_populates="vocabulary",cascade="all, delete-orphan")
    
class VocabularyWords(Base):
    __tablename__ = 'vocabulary_words'
    
    id = Column(Integer, primary_key=True, index=True)
    vocabulary_id = Column(Integer, ForeignKey('vocabulary.vocabulary_id', ondelete="CASCADE"), nullable=False)
    word_id = Column(Integer, ForeignKey('words.id', ondelete="RESTRICT"), nullable=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    vocabulary = relationship("Vocabulary", back_populates="vocabulary_words")
    word = relationship("Words", back_populates="vocabulary_words")
    user_word_status = relationship("UserWordStatus", back_populates="vocabulary_words", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('vocabulary_id', 'word_id', name='unique_vocab_word'),
    )
    
class UserWordStatus(Base):
    __tablename__ = 'user_word_status'

    id = Column(Integer, primary_key=True, index=True)
    vocabulary_word_id = Column(Integer, ForeignKey("vocabulary_words.id"), nullable=False)
    last_updated = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    user_synonyms = relationship("UserSynonyms", back_populates="user_word_status", cascade="all, delete-orphan")
    user_examples = relationship("UserExamples", back_populates="user_word_status", cascade="all, delete-orphan")
    user_tags = relationship("UserTags", back_populates="user_word_status", cascade="all, delete-orphan")
    user_definitions = relationship("UserDefinitions", back_populates="user_word_status", cascade="all, delete-orphan")
    user_translations = relationship("UserTranslations", back_populates="user_word_status", cascade="all, delete-orphan") 
    
    user_quiz_progress = relationship("UserQuizProgress", back_populates="user_word_status", cascade="all, delete-orphan")
    vocabulary_words = relationship("VocabularyWords", back_populates="user_word_status")
    
    
class UserQuota(Base):
    __tablename__ = 'user_quotas'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"),unique=True, nullable=False)
    subscription_type = Column(String, nullable=True, default="free")
    quota_remaining = Column(Integer, nullable=False)
    last_reset = Column(DateTime, default=datetime.now(timezone.utc))
    
    user = relationship("Users", back_populates="quota")

class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    difficulty = Column(String, nullable=False) 
    part_of_speech = Column(String, nullable=False) 
    question = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    hints = Column(JSON, nullable=False)
    
    word = relationship("Words", back_populates="exercises")
    user_exercises = relationship("UserExercises", back_populates="exercise", cascade="all, delete-orphan")
    multiple_choice = relationship("MultipleChoiceExercise", back_populates="exercise", uselist=False, cascade="all, delete-orphan")
    
class UserExercises(Base):
    __tablename__ = 'user_exercises'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, unique=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    

    user = relationship("Users", back_populates="user_exercises")
    exercise = relationship("Exercise", back_populates="user_exercises")
    progress = relationship("UserExerciseProgress", back_populates="user_exercise",uselist=False, cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'exercise_id', name='unique_user_exercise'),
    )
    
class MultipleChoiceExercise(Base):
    
    __tablename__ = 'multiple_choice_exercises'

    id = Column(Integer, primary_key=True, index=True)
    options = Column(JSON, nullable=False)
    correct_answer = Column(Integer, nullable=False) 
    exercise_id = Column(Integer, ForeignKey('exercises.id', ondelete="CASCADE"), unique=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    exercise = relationship("Exercise", back_populates="multiple_choice")

    
class UserExerciseProgress(Base):
    __tablename__ = 'user_exercise_progress'

    id = Column(Integer, primary_key=True, index=True)
    user_exercise_id = Column(Integer, ForeignKey("user_exercises.id", ondelete="CASCADE"), nullable=False, unique=True)
    correct = Column(Integer, nullable=False, default=0)
    wrong = Column(Integer, nullable=False, default=0)
    last_attempted = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    user_exercise = relationship("UserExercises", back_populates="progress")

class UserQuizProgress(Base):
    __tablename__ = 'user_quiz_progress'

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(Integer, ForeignKey("user_word_status.id", ondelete="CASCADE"), nullable=False)
    learning_stage = Column(Integer, nullable=False, default=1)
    correct = Column(Integer, nullable=False, default=0)
    wrong = Column(Integer, nullable=False, default=0)
    correct_streak = Column(Integer, nullable=False, default=0)
    wrong_streak = Column(Integer, nullable=False, default=0)
    last_attempted = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    time_to_repeat = Column(DateTime, nullable=True)
    
    user_word_status = relationship("UserWordStatus", back_populates="user_quiz_progress")
    

    
    
class UserSynonyms(Base):
    __tablename__ = 'user_synonyms'
    
    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(Integer, ForeignKey('user_word_status.id', ondelete="CASCADE"), nullable=False)
    synonym = Column(String, nullable=False)
    
    user_word_status = relationship("UserWordStatus", back_populates="user_synonyms")

class UserExamples(Base):
    __tablename__ = 'user_examples'
    
    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(Integer, ForeignKey('user_word_status.id', ondelete="CASCADE"), nullable=False)
    part_of_speech = Column(String, nullable=False)  # Part of speech for the example
    example = Column(String, nullable=False)  # Example sentence added by the user
    
    user_word_status = relationship("UserWordStatus", back_populates="user_examples")
    
class UserTags(Base):
    __tablename__ = 'user_tags'
    
    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(Integer, ForeignKey('user_word_status.id', ondelete="CASCADE"), nullable=False)
    tag = Column(String, nullable=False)  # Tag added by the user
    
    user_word_status = relationship("UserWordStatus", back_populates="user_tags")
    
class UserDefinitions(Base):
    __tablename__ = 'user_definitions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(Integer, ForeignKey('user_word_status.id',ondelete="CASCADE"), nullable=False)
    part_of_speech = Column(String, nullable=False)  # Part of speech for the definition
    definition = Column(String, nullable=False)  # Definition added by the user
    
    user_word_status = relationship("UserWordStatus", back_populates="user_definitions")
    
class UserTranslations(Base):
    __tablename__ = 'user_translations'
    
    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(Integer, ForeignKey('user_word_status.id', ondelete="CASCADE"), nullable=False)
    language = Column(String, nullable=False)  # Language of the translation
    translation = Column(String, nullable=False)  # Translation added by the user
    
    user_word_status = relationship("UserWordStatus", back_populates="user_translations")
    

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()