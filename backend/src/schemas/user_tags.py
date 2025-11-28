from pydantic import BaseModel, Field
from typing import Optional

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserTagBase(BaseModel):
    '''Base schema for user tags'''
    tag: str = Field(..., example='animals')

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserTagCreate(UserTagBase):
    '''Schema for creating a new user tag'''
    user_word_status_id: int = Field(..., example=1)

# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserTagUpdate(BaseModel):
    '''Schema for updating a user tag'''
    tag: Optional[str] = Field(None, example='nature')

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserTagResponse(UserTagBase):
    '''Schema for user tag response'''
    id: int
    user_word_status_id: int

    class Config:
        from_attributes = True