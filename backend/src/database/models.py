from sqlalchemy import Integer, String, Column, DateTime, create_engine,text,ForeignKey,Float
from sqlalchemy.orm import relationship
# Importing declarative_base to define the base class for our models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .database import engine

Base = declarative_base()



#TODO: Add more fields as necessary
#Create schema for words table
# Define the Words model
class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String, unique=True, index=True, nullable=False)
    added_by_user_id = Column(String,ForeignKey("users.clerk_id"), nullable=False)
    last_reviewed = Column(DateTime, default=datetime.utcnow)
    repeats_number = Column(Integer, default=0)
    time_to_reapet = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    audio_url = Column(String, nullable=True,default=None)
    frequency = Column(Float, default=0)
    difficulty = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("Users", back_populates="vocabulary")
    translations = relationship("Translation", back_populates="word")
    synonyms = relationship("Synonym", back_populates="word")
    definitions = relationship("Definition", back_populates="word")
    examples = relationship("Example", back_populates="word")
    tags = relationship("Tag", back_populates="word")
    warnings = relationship("Warning", back_populates="word")



class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    language = Column(String, nullable=False,default="russian")
    translation = Column(String, nullable=False)

    word = relationship("Words", back_populates="translations")

class Synonym(Base):
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
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
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    part_of_speech = Column(String, nullable=True)
    example = Column(String, nullable=False)

    word = relationship("Words", back_populates="examples")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    tag = Column(String, nullable=False)

    word = relationship("Words", back_populates="tags")

class Warning(Base):
    __tablename__ = "warnings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
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

    def __repr__(self):
        return f"<User(id={self.id}, clerk_id={self.clerk_id}, username={self.username}, email={self.email})>"


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
