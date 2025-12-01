from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from backend.src.config import settings

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserTranslationBase(BaseModel):
    '''Base schema for user translations'''
    language: str = Field(..., min_length=2, max_length=50, json_schema_extra={"example": "english"})
    translation: str = Field(..., min_length=1, max_length=200, json_schema_extra={"example": "cat"})
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v: str) -> str:
        """Validate language field."""
        if not v.isalpha():
            raise ValueError('Language must contain only alphabetic characters')
        if v.lower() not in settings.SUPPORTED_LANGUAGES:
            raise ValueError(f'Language must be one of {settings.SUPPORTED_LANGUAGES}')
        return v.lower()
    
    @field_validator('translation')
    @classmethod
    def validate_translation(cls, v: str) -> str:
        """Validate translation is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Translation cannot be empty or whitespace")
        return v.strip()


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserTranslationCreate(UserTranslationBase):
    '''Schema for creating user translation'''
    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserTranslationUpdate(BaseModel):
    '''Schema for updating user translation'''
    language: Optional[str] = Field(None, min_length=2, max_length=50, json_schema_extra={"example": "french"})
    translation: Optional[str] = Field(None, min_length=1, max_length=200, json_schema_extra={"example": "chat"})
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v: Optional[str]) -> Optional[str]:
        """Validate language if provided."""
        if v is not None:
            if not v.isalpha():
                raise ValueError('Language must contain only alphabetic characters')
            if v.lower() not in settings.SUPPORTED_LANGUAGES:
                raise ValueError(f'Language must be one of {settings.SUPPORTED_LANGUAGES}')
            return v.lower()
        return None
    
    @field_validator('translation')
    @classmethod
    def validate_translation(cls, v: Optional[str]) -> Optional[str]:
        """Validate translation if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Translation cannot be empty or whitespace")
        return v.strip() if v else None


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserTranslationResponse(BaseModel):
    '''Schema for user translation response'''
    id: int
    user_word_status_id: int
    language: str
    translation: str

    model_config = ConfigDict(from_attributes=True)


class UserTranslationListResponse(BaseModel):
    '''Schema for list of user translations'''
    success: bool = True
    count: int
    translations: list[UserTranslationResponse]