from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserHiddenBaseDefinition(BaseModel):
    """Base schema for user hidden base definitions"""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})
    definition_id : int = Field(..., gt=0, json_schema_extra={"example": 10})
# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserHiddenBaseDefinitionCreate(UserHiddenBaseDefinition):
    """Schema for creating a new user hidden base definition"""
    pass

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserHiddenBaseDefinitionResponse(BaseModel):
    """Schema for user hidden base definition response"""

    id: int
    user_word_status_id: int
    definition_id : int

    model_config = ConfigDict(from_attributes=True)
