from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserHiddenBaseExample(BaseModel):
    """Base schema for user hidden base examples"""

    user_word_status_id: int = Field(..., gt=0, json_schema_extra={"example": 1})
    example_id : int = Field(..., gt=0, json_schema_extra={"example": 10})
# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserHiddenBaseExampleCreate(UserHiddenBaseExample):
    """Schema for creating a new user hidden base example"""
    pass

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserHiddenBaseExampleResponse(BaseModel):
    """Schema for user hidden base example response"""

    id: int
    user_word_status_id: int
    example_id : int

    model_config = ConfigDict(from_attributes=True)
