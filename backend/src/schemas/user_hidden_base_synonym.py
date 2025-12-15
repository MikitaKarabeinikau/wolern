from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserHiddenBaseSynonym(BaseModel):
    """Base schema for user hidden base synonyms"""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})
    synonym_id : int = Field(..., gt=0, json_schema_extra={"example": 10})

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserHiddenBaseSynonymCreate(UserHiddenBaseSynonym):
    """Schema for creating a new user hidden base synonym"""
    pass

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserHiddenBaseSynonymResponse(BaseModel):
    """Schema for user hidden base synonym response"""

    id: int
    user_word_status_id: int
    synonym_id : int

    model_config = ConfigDict(from_attributes=True)