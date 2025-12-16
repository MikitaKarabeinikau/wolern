from sqlalchemy import (
    JSON,
    Integer,
    String,
    Column,
    DateTime,
    UniqueConstraint,
    text,
    ForeignKey,
    Float,
    event,
    Boolean,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base, engine


class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True, nullable=False, unique=True)
    language = Column(String, nullable=False)
    audio_url = Column(String, nullable=True)
    frequency = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
    is_active = Column(Boolean, default=True, nullable=False)

    definitions = relationship("Definitions", back_populates="word", lazy="joined", cascade="all, delete-orphan")
    examples = relationship("Examples", back_populates="word", lazy="joined", cascade="all, delete-orphan")
    synonyms = relationship("Synonyms", back_populates="word", lazy="joined", cascade="all, delete-orphan")
    translations = relationship("Translations", back_populates="word", lazy="joined", cascade="all, delete-orphan")
    tags = relationship("Tags", back_populates="word", lazy="joined", cascade="all, delete-orphan")
    warnings = relationship("Warnings", back_populates="word", lazy="joined", cascade="all, delete-orphan")
    vocabulary_words = relationship("VocabularyWords", back_populates="word")
    exercises = relationship("Exercise", back_populates="word")


# Event listener to convert language to lowercase
@event.listens_for(Words, "before_insert")
@event.listens_for(Words, "before_update")
def lowercase_word(mapper, connection, target):
    """Convert word to lowercase before insert or update."""
    if target.word:
        target.word = target.word.lower()


class Definitions(Base):
    __tablename__ = "definitions"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    part_of_speech = Column(String, nullable=False)
    definition = Column(String, nullable=False)

    word = relationship("Words", back_populates="definitions")


class Examples(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    part_of_speech = Column(String, nullable=False)
    example = Column(String, nullable=False)

    word = relationship("Words", back_populates="examples")


class Synonyms(Base):
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    synonym = Column(String, nullable=False)

    word = relationship("Words", back_populates="synonyms")


@event.listens_for(Synonyms, "before_insert")
def validate_and_format_synonym(mapper, connection, target):
    """Validate and format synonym before insert."""
    # Convert synonym to lowercase
    if target.synonym:
        target.synonym = target.synonym.lower()

    # Check for empty tag
    if not target.synonym or target.synonym.strip() == "":
        raise ValueError("Synonym cannot be empty.")

    # Check for duplicate tag per word
    result = connection.execute(
        text("SELECT id FROM synonyms WHERE word_id = :word_id AND synonym = :synonym"),
        {"word_id": target.word_id, "synonym": target.synonym},
    ).fetchone()

    if result:
        return target


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    tag = Column(String, nullable=False)

    word = relationship("Words", back_populates="tags")


@event.listens_for(Tags, "before_insert")
def validate_and_format_tag(mapper, connection, target):
    """Validate and format tag before insert."""
    # Convert tag to lowercase
    if target.tag:
        target.tag = target.tag.lower()

    # Check for empty tag
    if not target.tag or target.tag.strip() == "":
        raise ValueError("Tag cannot be empty.")

    # Check for duplicate tag per word
    result = connection.execute(
        text("SELECT id FROM tags WHERE word_id = :word_id AND tag = :tag"),
        {"word_id": target.word_id, "tag": target.tag},
    ).fetchone()

    if result:
        return target


class Translations(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    language = Column(String, nullable=False)
    translation = Column(String, nullable=False)

    word = relationship("Words", back_populates="translations")


@event.listens_for(Translations, "before_insert")
def validate_and_format_translation(mapper, connection, target):
    """Validate and format translation before insert."""
    # Convert translation to lowercase
    if target.translation:
        target.translation = target.translation.lower()

    # Check for empty translation
    if not target.translation or target.translation.strip() == "":
        raise ValueError("Translation cannot be empty.")

    if not target.language or target.language.strip() == "":
        raise ValueError("Language cannot be empty.")

    # Check for duplicate translation per word and language
    result = connection.execute(
        text("SELECT id FROM translations WHERE word_id = :word_id AND language = :language"),
        {"word_id": target.word_id, "language": target.language.lower()},
    ).fetchone()

    if result:
        return target


class Warnings(Base):
    __tablename__ = "warnings"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    warning_message = Column(String, nullable=False)

    word = relationship("Words", back_populates="warnings")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=True, default="user")
    native_language = Column(String, nullable=True, default="polish")
    preferred_language = Column(String, nullable=True, default="english")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    vocabulary = relationship("Vocabulary", back_populates="user", cascade="all, delete-orphan")
    quota = relationship(
        "UserQuota", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    user_exercises = relationship(
        "UserExercises", back_populates="user", cascade="all, delete-orphan"
    )


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    vocabulary_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("Users", back_populates="vocabulary")
    vocabulary_words = relationship(
        "VocabularyWords", back_populates="vocabulary", cascade="all, delete-orphan"
    )


@event.listens_for(Vocabulary, "before_insert")
def validate_user_exists(mapper, connection, target):
    """Ensure user exists before adding vocabulary."""
    if not target.user_id:
        raise ValueError("User ID must be provided for vocabulary.")

    # Check if the user exists in the database
    result = connection.execute(
        text("SELECT id FROM users WHERE id = :user_id"), {"user_id": target.user_id}
    ).fetchone()

    if not result:
        raise ValueError(f"User with ID {target.user_id} does not exist.")


class VocabularyWords(Base):
    __tablename__ = "vocabulary_words"

    id = Column(Integer, primary_key=True, index=True)
    vocabulary_id = Column(
        Integer, ForeignKey("vocabulary.vocabulary_id", ondelete="CASCADE"), nullable=False
    )
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    added_at = Column(DateTime, default=datetime.now(timezone.utc))

    vocabulary = relationship("Vocabulary", back_populates="vocabulary_words")
    word = relationship("Words", back_populates="vocabulary_words")
    user_word_status = relationship(
        "UserWordStatus", back_populates="vocabulary_words", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("vocabulary_id", "word_id", name="unique_vocab_word"),)


class UserWordStatus(Base):
    __tablename__ = "user_word_status"

    id = Column(Integer, primary_key=True, index=True)
    vocabulary_word_id = Column(Integer, ForeignKey("vocabulary_words.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user_synonyms = relationship(
        "UserSynonyms", back_populates="user_word_status",lazy="joined", cascade="all, delete-orphan"
    )
    user_examples = relationship(
        "UserExamples", back_populates="user_word_status",lazy="joined", cascade="all, delete-orphan"
    )
    user_tags = relationship(
        "UserTags", back_populates="user_word_status",lazy="joined", cascade="all, delete-orphan"
    )
    user_definitions = relationship(
        "UserDefinitions", back_populates="user_word_status",lazy="joined", cascade="all, delete-orphan"
    )
    user_translations = relationship(
        "UserTranslations", back_populates="user_word_status",lazy="joined", cascade="all, delete-orphan"
    )

    hidden_base_translations = relationship(
        "UserHiddenBaseTranslation",
        back_populates="user_word_status",
        cascade="all, delete-orphan",
        lazy="joined",
        primaryjoin="UserWordStatus.id == UserHiddenBaseTranslation.user_word_status_id"
    )
    hidden_base_definitions = relationship(
        "UserHiddenBaseDefinition",
        back_populates="user_word_status",
        cascade="all, delete-orphan",
        lazy="joined",
        primaryjoin="UserWordStatus.id == UserHiddenBaseDefinition.user_word_status_id"
    )
    hidden_base_examples = relationship(
        "UserHiddenBaseExample",
        back_populates="user_word_status",
        cascade="all, delete-orphan",
        lazy="joined",
        primaryjoin="UserWordStatus.id == UserHiddenBaseExample.user_word_status_id"
    )
    hidden_base_synonyms = relationship(
        "UserHiddenBaseSynonym",
        back_populates="user_word_status",
        cascade="all, delete-orphan",
        lazy="joined",
        primaryjoin="UserWordStatus.id == UserHiddenBaseSynonym.user_word_status_id"
    )
    hidden_base_tags = relationship(
        "UserHiddenBaseTag",
        back_populates="user_word_status",
        cascade="all, delete-orphan",
        lazy="joined",
        primaryjoin="UserWordStatus.id == UserHiddenBaseTag.user_word_status_id"
    )

    user_quiz_progress = relationship(
        "UserQuizProgress", back_populates="user_word_status",lazy="joined",uselist=False, cascade="all, delete-orphan"
    )
    vocabulary_words = relationship("VocabularyWords", back_populates="user_word_status")


class UserQuota(Base):
    __tablename__ = "user_quotas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    subscription_type = Column(String, nullable=True, default="free")
    quota_remaining = Column(Integer, nullable=False)
    last_reset = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("Users", back_populates="quota")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)
    difficulty = Column(String, nullable=False)
    part_of_speech = Column(String, nullable=False)
    question = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    hints = Column(JSON, nullable=False)

    word = relationship("Words", back_populates="exercises")
    user_exercises = relationship(
        "UserExercises", back_populates="exercise", cascade="all, delete-orphan"
    )
    multiple_choice = relationship(
        "MultipleChoiceExercise",
        back_populates="exercise",
        uselist=False,
        cascade="all, delete-orphan",
    )


class UserExercises(Base):
    __tablename__ = "user_exercises"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(
        Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    word_id = Column(Integer, ForeignKey("words.id", ondelete="RESTRICT"), nullable=False)

    user = relationship("Users", back_populates="user_exercises")
    exercise = relationship("Exercise", back_populates="user_exercises")
    progress = relationship(
        "UserExerciseProgress",
        back_populates="user_exercise",
        uselist=False,
        cascade="all, delete-orphan",
    )

    __table_args__ = (UniqueConstraint("user_id", "exercise_id", name="unique_user_exercise"),)


class MultipleChoiceExercise(Base):

    __tablename__ = "multiple_choice_exercises"

    id = Column(Integer, primary_key=True, index=True)
    options = Column(JSON, nullable=False)
    correct_answer = Column(Integer, nullable=False)
    exercise_id = Column(
        Integer, ForeignKey("exercises.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    exercise = relationship("Exercise", back_populates="multiple_choice")


class UserExerciseProgress(Base):
    __tablename__ = "user_exercise_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_exercise_id = Column(
        Integer, ForeignKey("user_exercises.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    correct = Column(Integer, nullable=False, default=0)
    wrong = Column(Integer, nullable=False, default=0)
    last_attempted = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user_exercise = relationship("UserExercises", back_populates="progress")


class UserQuizProgress(Base):
    __tablename__ = "user_quiz_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer, ForeignKey("user_word_status.id", ondelete="CASCADE"), nullable=False
    )
    learning_stage = Column(Integer, nullable=False, default=1)
    correct = Column(Integer, nullable=False, default=0)
    wrong = Column(Integer, nullable=False, default=0)
    correct_streak = Column(Integer, nullable=False, default=0)
    wrong_streak = Column(Integer, nullable=False, default=0)
    last_attempted = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    time_to_repeat = Column(DateTime, nullable=True)

    user_word_status = relationship("UserWordStatus", back_populates="user_quiz_progress")


class UserSynonyms(Base):
    __tablename__ = "user_synonyms"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer, ForeignKey("user_word_status.id", ondelete="CASCADE"), nullable=False
    )
    synonym = Column(String, nullable=False)

    user_word_status = relationship("UserWordStatus", back_populates="user_synonyms")


class UserExamples(Base):
    __tablename__ = "user_examples"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer, ForeignKey("user_word_status.id", ondelete="CASCADE"), nullable=False
    )
    part_of_speech = Column(String, nullable=False)  # Part of speech for the example
    example = Column(String, nullable=False)  # Example sentence added by the user

    user_word_status = relationship("UserWordStatus", back_populates="user_examples")


class UserTags(Base):
    __tablename__ = "user_tags"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer, ForeignKey("user_word_status.id", ondelete="CASCADE"), nullable=False
    )
    tag = Column(String, nullable=False)  # Tag added by the user

    user_word_status = relationship("UserWordStatus", back_populates="user_tags")


class UserDefinitions(Base):
    __tablename__ = "user_definitions"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer, ForeignKey("user_word_status.id", ondelete="CASCADE"), nullable=False
    )
    part_of_speech = Column(String, nullable=False)  # Part of speech for the definition
    definition = Column(String, nullable=False)  # Definition added by the user

    user_word_status = relationship("UserWordStatus", back_populates="user_definitions")

class UserTranslations(Base):
    __tablename__ = "user_translations"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer, ForeignKey("user_word_status.id", ondelete="CASCADE"), nullable=False
    )
    language = Column(String, nullable=False)  # Language of the translation
    translation = Column(String, nullable=False)  # Translation added by the user

    user_word_status = relationship("UserWordStatus", back_populates="user_translations")





# ============================================================================
# HIDDEN BASE CONTENT MODELS - Track which base items user wants to hide
# ============================================================================

class UserHiddenBaseTranslation(Base):
    """Track which base translations are hidden by the user."""
    __tablename__ = "user_hidden_base_translations"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer,
        ForeignKey("user_word_status.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    translation_id = Column(
        Integer,
        ForeignKey("translations.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    hidden_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationships
    user_word_status = relationship("UserWordStatus", back_populates="hidden_base_translations")
    translation = relationship("Translations")

    # Unique constraint: Can only hide each translation once per word status
    __table_args__ = (
        UniqueConstraint(
            "user_word_status_id",
            "translation_id",
            name="unique_hidden_translation_per_word_status"
        ),
    )


class UserHiddenBaseDefinition(Base):
    """Track which base definitions are hidden by the user."""
    __tablename__ = "user_hidden_base_definitions"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer,
        ForeignKey("user_word_status.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    definition_id = Column(
        Integer,
        ForeignKey("definitions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    hidden_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user_word_status = relationship("UserWordStatus", back_populates="hidden_base_definitions")
    definition = relationship("Definitions")

    __table_args__ = (
        UniqueConstraint(
            "user_word_status_id",
            "definition_id",
            name="unique_hidden_definition_per_word_status"
        ),
    )


class UserHiddenBaseExample(Base):
    """Track which base examples are hidden by the user."""
    __tablename__ = "user_hidden_base_examples"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer,
        ForeignKey("user_word_status.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    example_id = Column(
        Integer,
        ForeignKey("examples.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    hidden_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user_word_status = relationship("UserWordStatus", back_populates="hidden_base_examples")
    example = relationship("Examples")

    __table_args__ = (
        UniqueConstraint(
            "user_word_status_id",
            "example_id",
            name="unique_hidden_example_per_word_status"
        ),
    )


class UserHiddenBaseSynonym(Base):
    """Track which base synonyms are hidden by the user."""
    __tablename__ = "user_hidden_base_synonyms"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer,
        ForeignKey("user_word_status.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    synonym_id = Column(
        Integer,
        ForeignKey("synonyms.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    hidden_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user_word_status = relationship("UserWordStatus", back_populates="hidden_base_synonyms")
    synonym = relationship("Synonyms")

    __table_args__ = (
        UniqueConstraint(
            "user_word_status_id",
            "synonym_id",
            name="unique_hidden_synonym_per_word_status"
        ),
    )


class UserHiddenBaseTag(Base):
    """Track which base tags are hidden by the user."""
    __tablename__ = "user_hidden_base_tags"

    id = Column(Integer, primary_key=True, index=True)
    user_word_status_id = Column(
        Integer,
        ForeignKey("user_word_status.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    tag_id = Column(
        Integer,
        ForeignKey("tags.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    hidden_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user_word_status = relationship("UserWordStatus", back_populates="hidden_base_tags")
    tag = relationship("Tags")

    __table_args__ = (
        UniqueConstraint(
            "user_word_status_id",
            "tag_id",
            name="unique_hidden_tag_per_word_status"
        ),
    )
def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()
