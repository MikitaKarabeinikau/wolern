from fastapi import APIRouter
from . import auth

api_router = APIRouter()

api_router.include_router(auth.router)


@api_router.get("/health")
async def health_check():
    """API health check endpoint."""
    return {"status": "healthy", "version": "1.0.0", "message": "Wolern API is running"}
