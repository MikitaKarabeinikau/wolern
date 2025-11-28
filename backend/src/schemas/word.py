from pydantic import BaseModel, Field
from typing import List, Optional,Literal,Dict
from src.schemas.definitions import DefinitionResponse
from src.schemas.examples import ExampleResponse
from src.schemas.translations import TranslationResponse
from src.schemas.synonyms import SynonymResponse
from src.schemas.warnings import WarningResponse
from src.schemas.tags import TagResponse

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
    word: str = Field(..., min_length=1, max_length=100, example="hello")
    language: str = Field(..., min_length=2, max_length=15, example="english")
    audio_url: Optional[str] = Field(None, example="https://example.com/audio/hello.mp3")
    frequency: Optional[float] = Field(None, example=0.1234)
    
    definition: Dict[str, List[str]] = Field(..., example={"noun": ["a greeting"]})
    synonyms: List[str] = Field(default=[], example=["hi", "hey"])
    examples: Dict[str, List[str]] = Field(..., example={"noun": ["Hello, world!"]})
    translation: Dict[str, List[str]] = Field(..., example={"polish": ["cześć"]})
    tags: List[str] = Field(default=[], example=["basic", "greeting"])
    warnings: List[str] = Field(default=[], example=[])

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
    
    class Config:
        from_attributes = True

class WordPublic(BaseModel):
    """Public word information (minimal data)."""
    id: int
    word: str
    
    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True