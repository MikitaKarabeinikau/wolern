from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

from .user_examples import UserExampleResponse
from .user_quiz_progress import UserQuizProgressResponse
from .user_tags import UserTagResponse
from .user_translations import UserTranslationResponse
from .user_definitions import UserDefinitionResponse
from .user_synonyms import UserSynonymResponse
from .word import WordWithFullDataResponse


# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserWordStatusBase(BaseModel):
    """Base schema for user word status"""

    vocabulary_word_id: int = Field(..., json_schema_extra={"example": 1})


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserWordStatusCreate(UserWordStatusBase):
    """Schema for creating a user word status"""

    pass


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserWordStatusUpdate(BaseModel):
    """Schema for updating user word status"""

    vocabulary_word_id: Optional[int] = Field(None, json_schema_extra={"example": 1})


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserWordStatusResponse(UserWordStatusBase):
    """Schema for user word status response"""

    id: int
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# DETAILED RESPONSE WITH ALL RELATIONSHIPS
# ============================================================================
class UserWordStatusFullInfo(UserWordStatusResponse):
    """Schema for user word status with full info"""

    word_info: Optional[WordWithFullDataResponse] = None
    user_definitions: Optional[List[UserDefinitionResponse]] = []
    user_examples: Optional[List[UserExampleResponse]] = []
    user_translations: Optional[List[UserTranslationResponse]] = []
    user_tags: Optional[List[UserTagResponse]] = []
    user_synonyms: Optional[List[UserSynonymResponse]] = []
    user_quiz_progress: Optional[UserQuizProgressResponse] = None

    model_config = ConfigDict(from_attributes=True)

class UserWordStatusHiddenInfoResponse(UserWordStatusResponse):
    pass