from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserHiddenBaseTag(BaseModel):
    """Base schema for user hidden tags"""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})
    tag_id : int = Field(..., gt=0, json_schema_extra={"example": 10})


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserHiddenBaseTagCreate(UserHiddenBaseTag):
    """Schema for creating a new user hidden base tag"""
    pass

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserHiddenBaseTagResponse(BaseModel):
    """Schema for user hidden base tag response"""

    id: int
    user_word_status_id: int
    tag_id : int

    model_config = ConfigDict(from_attributes=True)
