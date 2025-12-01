from pydantic import BaseModel, Field, field_validator  # ✅ Removed EmailStr
from typing import Optional
from backend.src.config import settings

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserTranslationBase(BaseModel):
    '''Base schema for user translations'''
    language: str = Field(..., example='english')
    translation: str = Field(..., example="cat")  

    @field_validator('language')
    def validate_language(cls, value):
        if not value.isalpha():
            raise ValueError('Language must contain only alphabetic characters')
        if value not in settings.SUPPORTED_LANGUAGES:
            raise ValueError(f'Language must be one of {settings.SUPPORTED_LANGUAGES}')
        return value.lower()

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserTranslationCreate(UserTranslationBase):
    user_word_status_id: int = Field(..., example=1)

# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserTranslationUpdate(BaseModel):
    language: Optional[str] = Field(None, example='english')
    translation: Optional[str] = Field(None, example="cat")  

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserTranslationResponse(UserTranslationBase):
    id: int = Field(..., example=1)
    user_word_status_id: int = Field(..., example=1)

    class Config:
        from_attributes = True