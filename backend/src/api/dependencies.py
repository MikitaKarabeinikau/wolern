from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.src.database.database import get_db
from backend.src.database.crud import users
from backend.src.database.utils import authenticate_and_get_user_details


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> dict:
    """
    FastAPI dependency to get current authenticated user.
    
    Usage:
        @router.get("/protected")
        def protected_route(user: dict = Depends(get_current_user)):
            return {"message": f"Hello {user['username']}"}
    
    Returns:
        dict: User information including user_id, email, username
        
    Raises:
        HTTPException: 401 if authentication fails
    """
    # Authenticate with Clerk
    clerk_user = authenticate_and_get_user_details(request)
    clerk_user_id = clerk_user["user_id"]
    
    
    # Get or create user in your database
    user = users.get_user_by_clerk_id(db, clerk_user_id)

    if not user:
        user = users.create_user(
            db=db,
            clerk_id=clerk_user_id,
            email=clerk_user.get("email"),
        )
    
    return {
        "id": user.id,  
        "clerk_id": user.clerk_id,
        "email": user.email
    }

