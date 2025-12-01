from pydantic import BaseModel, Field, field_validator
from backend.src.config import settings

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class TranslationBase(BaseModel):
    language: str = Field(..., example="english")
    translation: str = Field(..., example="kot")
    
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
    word_id: int = Field(...,example=1)
    
# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class TranslationResponse(TranslationBase):
    id: int = Field(...,example=1)
    word_id: int = Field(...,example=1)
    

    class Config:
        from_attributes = True