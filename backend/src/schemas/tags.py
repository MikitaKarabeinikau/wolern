from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# BASE SCHEMAS
# ============================================================================
class TagBase(BaseModel):
    """Base schema for tag entities."""

    tag: str = Field(..., min_length=1, max_length=50, json_schema_extra={"example": "Sample Tag"})


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class TagCreate(TagBase):
    """Schema for creating a new tag."""

    word_id: int = Field(..., gt=0, json_schema_extra={"example": 1})


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class TagResponse(BaseModel):
    """Schema for tag response."""

    id: int
    word_id: int
    tag: str

    model_config = ConfigDict(from_attributes=True)
