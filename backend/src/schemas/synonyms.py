from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# BASE SCHEMAS
# ============================================================================

class SynonymBase(BaseModel):
    """Base schema for a synonym entry."""
    synonym: str = Field(..., min_length=1, max_length=100, json_schema_extra={"example": "joyful"})
    
# ============================================================================
# CREATE SCHEMAS
# ============================================================================

class SynonymCreate(SynonymBase):
    """Schema for creating a new synonym."""
    word_id: int = Field(..., json_schema_extra={"example": 1})

# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class SynonymResponse(BaseModel):
    """Schema for synonym response."""
    id: int
    word_id: int
    synonym: str

    model_config = ConfigDict(from_attributes=True)

    
    
    
    
    
    
    