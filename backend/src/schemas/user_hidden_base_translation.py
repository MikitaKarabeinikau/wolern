from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserHiddenBaseTranslation(BaseModel):
    """Base schema for user hidden base translations"""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})
    translation_id: int = Field(..., gt=0, json_schema_extra={"example": 42})

# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserHiddenBaseTranslationCreate(UserHiddenBaseTranslation):
    """Schema for creating a new user hidden base translation"""
    pass

# ===========================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserHiddenBaseTranslationResponse(BaseModel):
    """Schema for user hidden base translation response"""

    id: int
    user_word_status_id: int
    translation_id: int

    model_config = ConfigDict(from_attributes=True)