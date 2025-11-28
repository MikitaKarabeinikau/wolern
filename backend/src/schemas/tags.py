from pydantic import BaseModel, Field

# ============================================================================
# BASE SCHEMAS
# ============================================================================
class TagBase(BaseModel):
    """Base schema for tag entities."""
    tag: str = Field(..., min_length=1, max_length=50, example="Sample Tag")
    
# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class TagCreate(TagBase):
    """Schema for creating a new tag."""
    word_id: int = Field(..., example=1)
    
# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class TagResponse(BaseModel):
    """Schema for tag response."""
    id: int
    word_id: int
    tag: str

    class Config:
        from_attributes = True