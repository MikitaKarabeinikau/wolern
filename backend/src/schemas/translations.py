from pydantic import BaseModel, Field, field_validator, ConfigDict
from backend.src.config import settings

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class TranslationBase(BaseModel):
    language: str = Field(..., json_schema_extra={"example": "english"})
    translation: str = Field(..., json_schema_extra={"example": "kot"})
    
    @field_validator('language')
    def validate_language(cls, value):
        allowed_languages = settings.SUPPORTED_LANGUAGES
        if value not in allowed_languages:
            raise ValueError(f"Language must be one of {allowed_languages}")
        return value

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class TranslationCreate(TranslationBase):
    word_id: int = Field(..., json_schema_extra={"example": 1})
    
# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class TranslationResponse(TranslationBase):
    id: int = Field(..., json_schema_extra={"example": 1})
    word_id: int = Field(..., json_schema_extra={"example": 1})
    

    model_config = ConfigDict(from_attributes=True)