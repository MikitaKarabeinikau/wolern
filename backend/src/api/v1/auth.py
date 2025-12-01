from fastapi import APIRouter, Depends
from backend.src.api.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    This endpoint validates the Clerk JWT token and returns user details.
    On first login, it auto-creates the user in the database.
    """
    return {
        "success": True,
        "user": {
            "id": user["id"],
            "clerk_id": user["clerk_id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "native_language": user["native_language"],
            "preferred_language": user["preferred_language"]
        }
    }


@router.get("/test")
async def test_public():
    """Public endpoint - no authentication required."""
    return {
        "message": "Auth system is operational",
        "auth_required": False
    }


@router.get("/admin-test")
async def test_admin(user: dict = Depends(require_admin)):
    """Admin-only endpoint for testing authorization."""
    return {
        "message": "Admin access confirmed",
        "user": user["username"]
    }