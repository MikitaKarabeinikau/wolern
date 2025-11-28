from pydantic import BaseModel, Field
from typing import Optional

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class VocabularyBase(BaseModel):
    """Base vocabulary schema with common fields."""
    name: Optional[str] = Field(None, min_length=3, max_length=50, example="English Basics")
    
    
# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class VocabularyCreate(VocabularyBase):
    """Schema for creating a new vocabulary."""
    name: str = Field(..., min_length=3, max_length=50, example="English Basics")


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class VocabularyUpdateName(BaseModel):
    """Schema for updating vocabulary name."""
    name: str = Field(..., min_length=3, max_length=50, example="Advanced English")

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class VocabularyResponse(BaseModel):
    """Schema for user response"""
    vocabulary_id: int
    name: str
    user_id: int

    class Config:
        from_attributes = True