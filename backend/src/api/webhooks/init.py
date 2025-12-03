from fastapi import APIRouter
from .clerk import router as clerk_router

# Main webhooks router
router = APIRouter()

# Include all webhook routers
router.include_router(clerk_router, tags=["webhooks:clerk"])
