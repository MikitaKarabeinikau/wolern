from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from backend.src.config import settings


# ============================================================================
# BASE SCHEMAS
# ============================================================================
class UserBase(BaseModel):
    """Base user schema with common fields."""

    username: Optional[str] = Field(
        None, min_length=3, max_length=25, json_schema_extra={"example": "johndoe"}
    )
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "johndoe@example.com"})

    @field_validator("username")
    def validate_username(cls, v):
        """Validate username contains only alphanumeric characters and underscores."""
        if v is not None and not v.isidentifier():
            raise ValueError("Username must contain only alphanumeric characters and underscores")
        return v

    @field_validator("email")
    def validate_email(cls, v):
        """Validate email domain is allowed."""
        allowed_domains = settings.ALLOWED_EMAIL_DOMAINS
        if v is None:
            return v
        domain = v.split("@")[-1]
        if domain not in allowed_domains:
            raise ValueError(f"Email domain must be one of {allowed_domains}")
        return v


# ============================================================================
# CREATE SCHEMAS
# ============================================================================
class UserCreate(UserBase):
    """Schema for creating a new user."""

    clerk_id: str = Field(..., min_length=1, json_schema_extra={"example": "user_2abc123xyz"})
    role: str = Field(default="user", json_schema_extra={"example": "user"})
    native_language: Optional[str] = Field(
        default="polish", json_schema_extra={"example": "polish"}
    )
    preferred_language: Optional[str] = Field(
        default="english", json_schema_extra={"example": "english"}
    )

    @field_validator("role")
    def validate_role(cls, v):
        """Validate role is either 'user' or 'admin'."""
        allowed_roles = ["user", "admin"]
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return v


# ============================================================================
# UPDATE SCHEMAS
# ============================================================================
class UserUpdateUsername(BaseModel):
    """Schema for updating username."""

    username: str = Field(
        ..., min_length=3, max_length=25, json_schema_extra={"example": "newusername"}
    )


class UserUpdateNativeLanguage(BaseModel):
    """Schema for updating native language."""

    native_language: str = Field(
        ..., min_length=2, max_length=15, json_schema_extra={"example": "french"}
    )


class UserUpdatePreferredLanguage(BaseModel):
    """Schema for updating preferred language."""

    preferred_language: str = Field(
        ..., min_length=2, max_length=15, json_schema_extra={"example": "spanish"}
    )


class UserUpdateRole(BaseModel):
    """Schema for updating user role (admin only)."""

    role: str = Field(..., json_schema_extra={"example": "teacher"})

    @field_validator("role")
    def validate_role(cls, v):
        """Validate role is either 'user','admin', 'teacher', or 'student'."""
        allowed_roles = settings.VALID_USER_ROLES
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return v


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================
class UserResponse(UserBase):
    """Schema for user responses."""

    id: int
    clerk_id: str
    role: str
    native_language: Optional[str] = None
    preferred_language: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    """Public user information (minimal data)."""

    username: Optional[str] = None
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserWithQuota(UserResponse):
    """User response with quota information."""

    quota_remaining: Optional[int] = None
    quota_reset_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
