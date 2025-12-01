from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class VocabularyWordBase(BaseModel):
    '''Base schema for vocabulary words'''
    vocabulary_id: int = Field(..., json_schema_extra={"example": 1})
    word_id: int = Field(..., json_schema_extra={"example": 1})

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class VocabularyWordCreate(VocabularyWordBase):
    '''Schema for adding a word to vocabulary'''
    pass

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class VocabularyWordResponse(VocabularyWordBase):
    '''Schema for vocabulary word response'''
    id: int
    added_at: datetime

    class Config:
        from_attributes = True

# ============================================================================
# DETAILED RESPONSE
# ============================================================================
class VocabularyWordDetailResponse(VocabularyWordResponse):
    '''Schema for detailed vocabulary word with word data'''
    word: Optional[dict] = None
    
    model_config = ConfigDict(from_attributes=True)