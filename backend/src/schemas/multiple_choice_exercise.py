from pydantic import BaseModel, Field, field_validator,ConfigDict
from typing import List, Optional
from datetime import datetime

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class MultipleChoiceExerciseBase(BaseModel):
    '''Base schema for multiple choice exercise'''
    options: List[str] = Field(..., min_length=2, max_length=10, json_schema_extra={"example": ["option1", "option2", "option3", "option4"]})
    correct_answer: int = Field(..., ge=0, json_schema_extra={"example": 2})

    @field_validator('correct_answer')
    @classmethod
    def validate_correct_answer(cls, value, info):
        # Pydantic v2 syntax
        options = info.data.get('options', [])
        if options and not (0 <= value < len(options)):
            raise ValueError('correct_answer must be a valid index in options list')
        return value

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class MultipleChoiceExerciseCreate(MultipleChoiceExerciseBase):
    '''Schema for creating multiple choice exercise'''
    exercise_id: int = Field(..., json_schema_extra={"example": 1})

# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class MultipleChoiceExerciseUpdate(BaseModel):
    '''Schema for updating multiple choice exercise'''
    options: Optional[List[str]] = Field(None, min_length=2, max_length=10, json_schema_extra={"example": ["option1", "option2", "option3", "option4"]})
    correct_answer: Optional[int] = Field(None, ge=0, json_schema_extra={"example": 2})

    @field_validator('correct_answer')
    @classmethod
    def validate_correct_answer(cls, value, info):
        if value is not None:
            options = info.data.get('options')
            if options and not (0 <= value < len(options)):
                raise ValueError('correct_answer must be a valid index in options list')
        return value

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class MultipleChoiceExerciseResponse(MultipleChoiceExerciseBase):
    '''Schema for multiple choice exercise response'''
    id: int
    exercise_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ============================================================================
# SAFE RESPONSE (for quizzes - hides correct answer)
# ============================================================================
class MultipleChoiceExerciseSafeResponse(BaseModel):
    '''Schema for quiz display without revealing answer'''
    id: int
    exercise_id: int
    options: List[str]
    # correct_answer intentionally omitted for quiz purposes
    
    model_config = ConfigDict(from_attributes=True)