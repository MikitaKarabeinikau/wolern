from pydantic import BaseModel, Field

# ============================================================================
# BASE SCHEMAS
# ============================================================================

class SynonymBase(BaseModel):
    """Base schema for a synonym entry."""
    synonym: str = Field(..., min_length=1, max_length=100, example="joyful")
    
# ============================================================================
# CREATE SCHEMAS
# ============================================================================

class SynonymCreate(SynonymBase):
    """Schema for creating a new synonym."""
    word_id: int = Field(..., example=1)

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class SynonymResponse(BaseModel):
    """Schema for synonym response."""
    id: int
    word_id: int
    synonym: str

    class Config:
        from_attributes = True

    
    
    
    
    
    
    