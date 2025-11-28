from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserQuizProgressBase(BaseModel):
    '''Base schema for user quiz progress'''
    learning_stage: int = Field(default=1, ge=1, example=2)
    correct: int = Field(default=0, ge=0, example=3)
    wrong: int = Field(default=0, ge=0, example=1)
    correct_streak: int = Field(default=0, ge=0, example=2)
    wrong_streak: int = Field(default=0, ge=0, example=0)

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserQuizProgressCreate(BaseModel):
    '''Schema for creating user quiz progress'''
    user_word_status_id: int = Field(..., example=1)
    learning_stage: int = Field(default=1, ge=1, example=1)
    correct: int = Field(default=0, ge=0, example=0)
    wrong: int = Field(default=0, ge=0, example=0)
    correct_streak: int = Field(default=0, ge=0, example=0)
    wrong_streak: int = Field(default=0, ge=0, example=0)

# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserQuizProgressUpdate(BaseModel):
    '''Schema for updating user quiz progress'''
    learning_stage: Optional[int] = Field(None, ge=1, example=2)
    correct: Optional[int] = Field(None, ge=0, example=3)
    wrong: Optional[int] = Field(None, ge=0, example=1)
    correct_streak: Optional[int] = Field(None, ge=0, example=2)
    wrong_streak: Optional[int] = Field(None, ge=0, example=0)

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserQuizProgressResponse(UserQuizProgressBase):
    '''Schema for user quiz progress response'''
    id: int
    user_word_status_id: int
    last_attempted: datetime
    time_to_repeat: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============================================================================
# STATISTICS SCHEMA
# ============================================================================
class UserQuizStatsResponse(BaseModel):
    '''Schema for quiz statistics'''
    user_word_status_id: int
    learning_stage: int
    correct: int
    wrong: int
    correct_streak: int
    wrong_streak: int
    last_attempted: datetime
    time_to_repeat: Optional[datetime] = None
    
    class Config:
        from_attributes = True