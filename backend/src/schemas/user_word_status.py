from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

from schemas.user_hidden_base_example import UserHiddenBaseExampleResponse
from schemas.user_hidden_base_synonym import UserHiddenBaseSynonymResponse
from schemas.user_hidden_base_tag import UserHiddenBaseTagResponse
from schemas.user_hidden_base_translation import UserHiddenBaseTranslationResponse
from schemas.user_hidden_base_definition import UserHiddenBaseDefinitionResponse

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
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# DETAILED RESPONSE WITH ALL RELATIONSHIPS
# ============================================================================
class UserWordStatusFullInfo(UserWordStatusResponse):
    """Schema for user word status with full info"""

    # word_info: Optional[WordWithFullDataResponse] = None
    user_definitions: List[UserDefinitionResponse] = []
    user_examples: List[UserExampleResponse] = []
    user_translations: List[UserTranslationResponse] = []
    user_tags: List[UserTagResponse] = []
    user_synonyms: List[UserSynonymResponse] = []
    user_quiz_progress: Optional[UserQuizProgressResponse] = None

    hidden_base_translations: List[UserHiddenBaseTranslationResponse] = []
    hidden_base_examples: List[UserHiddenBaseExampleResponse] = []
    hidden_base_tags: List[UserHiddenBaseTagResponse] = []
    hidden_base_synonyms: List[UserHiddenBaseSynonymResponse] = []
    hidden_base_definitions: List[UserHiddenBaseDefinitionResponse] = []

    model_config = ConfigDict(from_attributes=True)

class UserWordStatusHiddenInfoResponse(UserWordStatusResponse):
    """Schema for user word status with hidden info"""


    model_config = ConfigDict(from_attributes=True)
