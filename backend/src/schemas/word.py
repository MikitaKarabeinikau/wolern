from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
from backend.src.schemas.definitions import DefinitionResponse
from backend.src.schemas.examples import ExampleResponse
from backend.src.schemas.translations import TranslationResponse
from backend.src.schemas.synonyms import SynonymResponse
from backend.src.schemas.warnings import WarningResponse
from backend.src.schemas.tags import TagResponse

# ============================================================================
# BASE SCHEMAS
# ============================================================================


class WordBase(BaseModel):
    word: str


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class WordCreate(WordBase):
    """Schema for creating a new word."""

    word: str = Field(..., min_length=1, max_length=100, json_schema_extra={"example": "hello"})
    language: str = Field(
        ..., min_length=2, max_length=15, json_schema_extra={"example": "english"}
    )
    audio_url: Optional[str] = Field(
        None, json_schema_extra={"example": "https://example.com/audio/hello.mp3"}
    )
    frequency: Optional[float] = Field(None, json_schema_extra={"example": 0.1234})
    translation: Dict[str, List[str]] = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {"russian": ["привет", "здравствуйте"], "spanish": ["hola"]}
        },
    )
    synonyms: List[str] = Field(
        default_factory=list, json_schema_extra={"example": ["hi", "greetings"]}
    )
    definition: Dict[str, List[str]] = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {"noun": ["a small domesticated carnivorous mammal"]}
        },
    )
    examples: Dict[str, List[str]] = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {"noun": ["The cat sat on the mat."]}
        },
    )
    tags: List[str] = Field(
        default_factory=list,
        json_schema_extra={"example": ["animal"]}
    )
    warnings: List[str] = Field(
        default_factory=list,
        json_schema_extra={"example": ["rare", "archaic"]}
    )



# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class WordResponse(BaseModel):
    """Schema for word response."""

    id: int
    word: str
    language: str
    audio_url: Optional[str] = None
    frequency: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class WordPublic(BaseModel):
    """Public word information (minimal data)."""

    id: int
    word: str

    model_config = ConfigDict(from_attributes=True)


class WordWithFullDataResponse(BaseModel):
    """Word information with full data."""

    id: int
    word: str
    language: str
    audio_url: Optional[str] = None
    frequency: Optional[float] = None
    definitions: List[DefinitionResponse] = []
    synonyms: List[SynonymResponse] = []
    examples: List[ExampleResponse] = []
    translations: List[TranslationResponse] = []
    tags: List[TagResponse] = []
    warnings: List[WarningResponse] = []

    model_config = ConfigDict(from_attributes=True)
