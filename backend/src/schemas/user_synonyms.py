from pydantic import BaseModel, Field
from typing import Optional

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserSynonymBase(BaseModel):
    '''Base schema for user synonyms'''
    synonym: str = Field(..., min_length=1, max_length=100, example='fast')

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserSynonymCreate(UserSynonymBase):
    '''Schema for creating user synonym'''
    user_word_status_id: int = Field(..., example=1)

# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserSynonymUpdate(BaseModel):
    '''Schema for updating user synonym'''
    synonym: Optional[str] = Field(None, min_length=1, max_length=100, example='fast')

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserSynonymResponse(UserSynonymBase):  # ✅ Inherits synonym from base
    '''Schema for user synonym response'''
    id: int
    user_word_status_id: int
    
    class Config:
        from_attributes = True