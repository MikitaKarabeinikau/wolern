from pydantic import BaseModel, Field
from typing import Optional

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserExampleBase(BaseModel):
    '''Base schema for user examples.'''
    part_of_speech: str = Field(..., example="noun")  
    example: str = Field(..., example="The cat sat on the mat.")  

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserExampleCreate(UserExampleBase):
    '''Schema for creating a user example.'''
    user_word_status_id: int = Field(..., example=1)

# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserExampleUpdate(BaseModel):
    '''Schema for updating a user example.'''
    part_of_speech: Optional[str] = Field(None, example="noun")  
    example: Optional[str] = Field(None, example="She runs every morning.")

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserExampleResponse(UserExampleBase):  
    '''Schema for user example response.'''
    id: int
    user_word_status_id: int

    class Config:
        from_attributes = True