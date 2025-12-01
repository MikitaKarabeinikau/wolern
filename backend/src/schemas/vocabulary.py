from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class VocabularyBase(BaseModel):
    """Base vocabulary schema with common fields."""
    name: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "English Basics"})
    
    
# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class VocabularyCreate(VocabularyBase):
    """
    Schema for creating a new vocabulary.
    
    Note: user_id is NOT included here - it's taken from the authenticated user's token.
    """
    pass 


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class VocabularyUpdateName(BaseModel):
    """Schema for updating vocabulary name."""
    name: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "Advanced English"})


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class VocabularyResponse(BaseModel):
    """Schema for vocabulary response."""
    vocabulary_id: int
    name: str
    user_id: int

    model_config = {
        "from_attributes": True
    }


class VocabularyDetailResponse(VocabularyResponse):
    """Extended vocabulary response with additional details."""
    created_at: Optional[datetime] = None
    word_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class VocabularyListResponse(BaseModel):
    """Schema for list of vocabularies."""
    success: bool = True
    count: int
    vocabularies: list[VocabularyDetailResponse]