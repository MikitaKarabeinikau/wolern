from sqlalchemy import JSON, Integer, String, Column, DateTime, create_engine, func,text,ForeignKey,Float
from sqlalchemy.orm import relationship
# Importing declarative_base to define the base class for our models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .database import engine

Base = declarative_base()

class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String, unique=True, index=True, nullable=False)
    base_id = Column(Integer, ForeignKey("word_base.id"))
    added_by_user_id = Column(String,ForeignKey("users.clerk_id", ondelete="CASCADE"), nullable=False)
    audio_url = Column(String, nullable=True,default=None)
    frequency = Column(Float, default=0)
    difficulty = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vocabulary = Column(String, nullable=False, default="new")
    
    user = relationship("Users", back_populates="vocabulary")
    translations = relationship("Translation", back_populates="word")
    synonyms = relationship("Synonym", back_populates="word")
    definitions = relationship("Definition", back_populates="word")
    examples = relationship("Example", back_populates="word")
    tags = relationship("Tag", back_populates="word")
    warnings = relationship("Warning", back_populates="word")
    word_base = relationship("Word_Base", back_populates="words")
    quiz_progress = relationship("User_Quiz_Progress", back_populates="word")
    exercises = relationship("Exercise", back_populates="word")

class Definition_Base(Base):
    __tablename__ = "definition_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    base_id = Column(Integer, ForeignKey("word_base.id"), nullable=False)
    part_of_speech = Column(String, nullable=False)
    definition = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    word_base = relationship("Word_Base")

class Translation_Base(Base):
    __tablename__ = "translation_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    base_id = Column(Integer, ForeignKey("word_base.id"), nullable=False)
    translation = Column(String, nullable=False)
    language = Column(String, nullable=False, default="russian")
    added_at = Column(DateTime, default=datetime.utcnow)

    word_base = relationship("Word_Base")

class Synonym_Base(Base):
    __tablename__ = "synonym_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    base_id = Column(Integer, ForeignKey("word_base.id"), nullable=False)
    synonym = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
  
    word_base = relationship("Word_Base")

class Example_Base(Base):
    __tablename__ = "example_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    base_id = Column(Integer, ForeignKey("word_base.id"), nullable=False)
    example_sentence = Column(String, nullable=False)
    part_of_speech = Column(String, nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)

    word_base = relationship("Word_Base")

class User_Quiz_Progress(Base):
    __tablename__ = "user_quiz_progress"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.clerk_id", ondelete="CASCADE"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    correct_answers = Column(Integer, nullable=False, default=0)
    wrong_answers = Column(Integer, nullable=False, default=0)
    correct_answers_in_a_row = Column(Integer, nullable=False, default=0)
    wrong_answers_in_a_row = Column(Integer, nullable=False, default=0)
    learning_stage = Column(Integer, nullable=False, default=0)
    time_to_repeat = Column(DateTime, default=datetime.utcnow)
    last_quiz_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("Users")
    word = relationship("Words", back_populates="quiz_progress")

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    language = Column(String, nullable=False,default="russian")
    translation = Column(String, nullable=False)

    word = relationship("Words", back_populates="translations")

class Synonym(Base):
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    synonym = Column(String, nullable=False)

    word = relationship("Words", back_populates="synonyms")

class Definition(Base):
    __tablename__ = "definitions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    part_of_speech = Column(String, nullable=False)
    definition = Column(String, nullable=False)

    word = relationship("Words", back_populates="definitions")

class Example(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    part_of_speech = Column(String, nullable=True)
    example_sentence = Column(String, nullable=False)

    word = relationship("Words", back_populates="examples")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    tag = Column(String, nullable=False)

    word = relationship("Words", back_populates="tags")

class Warning(Base):
    __tablename__ = "warnings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    warning_message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    word = relationship("Words", back_populates="warnings")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    vocabulary = relationship("Words", back_populates="user")
    exercise_quota = relationship("ExerciseQuota", back_populates="user", uselist=False, cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="user")


    def __repr__(self):
        return f"<User(id={self.id}, clerk_id={self.clerk_id}, username={self.username}, email={self.email})>"
class Exercise(Base):

    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, comment="ID of the target word being tested.")
    difficulty = Column(String, nullable=False) 
    part_of_speech = Column(String, nullable=False) # e.g., 'Noun', 'Verb', 'Adverb'
    question = Column(String, nullable=False, comment="The sentence with the missing word/phrase (the prompt).")
    explanation = Column(String, nullable=False, comment="Explanation shown after the user answers.")
    created_by = Column(String, ForeignKey("users.clerk_id"), nullable=False, comment="Foreign key to the user who created this exercise.")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    hints = Column(JSON, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) # Add this line

    word = relationship("Words", back_populates="exercises")
    user = relationship("Users", back_populates="exercises")
    multiple_choice_exercises = relationship("MultipleChoiceExercise", back_populates="exercise_base")
    
    def __repr__(self):
        return f"<Exercise(id={self.id}, word_id={self.word_id}, difficulty='{self.difficulty}')>"


# class User_Exercise_Progress(Base):
#     __tablename__ = "user_exercise_progress"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(String, ForeignKey("users.clerk_id", ondelete="CASCADE"), nullable=False)
#     exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
#     attempts = Column(Integer, nullable=False, default=0)
#     correct_attempts = Column(Integer, nullable=False, default=0)
#     last_attempt_date = Column(DateTime, default=datetime.utcnow)

#     user = relationship("Users")
#     exercise = relationship("Exercise")

class Word_Base(Base):
    __tablename__ = "word_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String, nullable=False, unique=True)
    added_at = Column(DateTime, default=datetime.utcnow)

    words = relationship("Words", back_populates="word_base")
    exercises = relationship("ExerciseBase", back_populates="word_base")


class ExerciseBase(Base):
    __tablename__ = "exercise_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    base_word_id = Column(Integer, ForeignKey("word_base.id"), nullable=False)
    difficulty = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    hints = Column(String, nullable=True)  
    question = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    part_of_speech = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)


    word_base = relationship("Word_Base", back_populates="exercises")
    multiple_choice_exercise_base = relationship("MultipleChoiceExerciseBase", back_populates="exercise_base")

class MultipleChoiceExercise(Base):

    __tablename__ = 'multiple_choice_exercises'

    id = Column(Integer, primary_key=True, index=True)
    options = Column(String, nullable=False, comment="List of 4 answer options (strings).")
    correct_answer = Column(String, nullable=False, comment="The value of the correct answer.") 
    exercise_id = Column(Integer, ForeignKey('exercises.id'), unique=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    exercise_base= relationship("Exercise", back_populates="multiple_choice_exercises")

class MultipleChoiceExerciseBase(Base):
    __tablename__ = "multiple_choice_exercise_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String, nullable=False)
    base_exercise_id = Column(Integer, ForeignKey("exercise_base.id"), unique=True, nullable=False)
    options = Column(String, nullable=False, comment="JSON string representing a list of 4 answer options (strings).")
    correct_answer = Column(String, nullable=False, comment="The value of the correct answer.")

   
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    exercise_base = relationship("ExerciseBase", back_populates="multiple_choice_exercise_base")


# How many exercises a user can generate per day
class ExerciseQuota(Base):
    __tablename__ = "exercise_quotas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.clerk_id", ondelete="CASCADE"), nullable=False, unique=True)
    last_reset_date = Column(DateTime, default=datetime.utcnow)
    exercises_remaining = Column(Integer, default=10)

    user = relationship("Users", back_populates="exercise_quota")
    
    

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
