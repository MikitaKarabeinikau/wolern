from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
import logging
from svix.webhooks import Webhook

from backend.src.config import settings
from backend.src.database.database import get_db
from backend.src.database.models import Users
from backend.src.database.crud.users import create_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/clerk")
async def handle_clerk_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle Clerk webhook events.
    Currently handles: user.created
    """
    # Get webhook secret from config
    webhook_secret = settings.CLERK_WEBHOOK_SECRET
    if not webhook_secret:
        logger.error("Clerk webhook secret not configured")
        raise HTTPException(
            status_code=500,
            detail="Webhook secret not configured"
        )
    
    # Get request body and headers
    body = await request.body()
    payload = body.decode('utf-8')
    headers = dict(request.headers)
    
    try:
        # Verify webhook signature
        webhook = Webhook(webhook_secret)
        webhook.verify(payload, headers)
        
        # Parse webhook data
        data = json.loads(payload)
        event_type = data.get("type")
        
        # Handle user.created event
        if event_type == "user.created":
            return await handle_user_created(db, data)
        
        # Log unhandled event types
        logger.info(f"Unhandled event type: {event_type}")
        return {
            "success": True,
            "message": f"Event type {event_type} acknowledged but not handled"
        }
        
    except Exception as e:
        logger.error(f"Error handling Clerk webhook: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


async def handle_user_created(db: Session, data: dict) -> dict:
    """
    Handle user.created webhook event from Clerk.
    Creates a new user in the database.
    """
    user_data = data.get("data", {})
    clerk_user_id = user_data.get("id")
    
    # Extract email
    email_addresses = user_data.get("email_addresses", [])
    email = email_addresses[0].get("email_address") if email_addresses else None
    
    # Extract username (if available)
    username = user_data.get("username") or email.split("@")[0] if email else None
    
    if not clerk_user_id:
        logger.error("No clerk_id in webhook data")
        raise HTTPException(status_code=400, detail="Invalid webhook data")
    
    try:
        # Check if user already exists
        existing_user = db.query(Users).filter(
            Users.clerk_id == clerk_user_id
        ).first()
        
        if existing_user:
            logger.info(f"User {clerk_user_id} already exists")
            return {
                "success": True,
                "message": "User already exists",
                "user_id": existing_user.id
            }
        
        # Create new user
        new_user = create_user(
            db=db,
            clerk_id=clerk_user_id,
            username=username,
            email=email
        )
        
        logger.info(f"Created user {clerk_user_id} successfully")
        return {
            "success": True,
            "message": "User created successfully",
            "user_id": new_user.id
        }
        
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"User creation conflict for {clerk_user_id}: {e}")
        return {
            "success": True,
            "message": "User creation conflict, assuming already created"
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user {clerk_user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )