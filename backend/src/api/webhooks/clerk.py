from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
import logging
from svix import WebhookVerificationError
from svix.webhooks import Webhook
import os
from dotenv import load_dotenv
from backend.src.config import settings
from backend.src.database.database import get_db
from backend.src.database.models import Users
from backend.src.database.crud.users import create_user, get_all_users

router = APIRouter()
logger = logging.getLogger(__name__)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",'..', ".env"))
load_dotenv(env_path)

logger.info(f"Loading .env from: {env_path}")
logger.info(f"CLERK_WEBHOOK_SECRET loaded: {bool(os.getenv('CLERK_WEBHOOK_SECRET'))}")

@router.post("/clerk")
async def clerk_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Clerk webhook events."""
    logger.info("=" * 50)
    logger.info("WEBHOOK RECEIVED!")
    
    try:
        # Get webhook secret from environment
        webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
        logger.info(f"Webhook secret exists: {bool(webhook_secret)}")
        
        if not webhook_secret:
            logger.error("CLERK_WEBHOOK_SECRET not configured")
            raise HTTPException(status_code=500, detail="Webhook secret not configured")

        # Get headers
        svix_id = request.headers.get("svix-id")
        svix_timestamp = request.headers.get("svix-timestamp")
        svix_signature = request.headers.get("svix-signature")

        logger.info(f"Headers - ID: {svix_id}, TS: {svix_timestamp}, Sig: {bool(svix_signature)}")

        if not all([svix_id, svix_timestamp, svix_signature]):
            logger.error(f"Missing headers - ID: {svix_id}, TS: {svix_timestamp}, Sig: {bool(svix_signature)}")
            raise HTTPException(status_code=400, detail="Missing required headers")

        # Get body
        body = await request.body()
        logger.info(f"Body received: {len(body)} bytes")

        # Verify webhook signature
        try:
            wh = Webhook(webhook_secret)
            payload = wh.verify(body, {
                "svix-id": svix_id,
                "svix-timestamp": svix_timestamp,
                "svix-signature": svix_signature,
            })
            logger.info("✅ Webhook signature verified")
        except WebhookVerificationError as e:
            logger.error(f"❌ Webhook verification failed: {e}")
            raise HTTPException(status_code=400, detail="Invalid webhook signature")

        # Parse event
        event_type = payload.get("type")
        logger.info(f"Event type: {event_type}")

        if event_type == "user.created":
            logger.info("Processing user.created event")
            result = await handle_user_created(db, payload)
            logger.info(f"User created result: {result}")
            return result
        
        logger.info(f"Ignoring event: {event_type}")
        return {"status": "ignored", "event": event_type}

    except HTTPException as he:
        logger.error(f"HTTP Exception: {he.detail}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error in webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


async def handle_user_created(db: Session, data: dict) -> dict:
    """Handle user.created webhook event from Clerk."""
    logger.info("=" * 50)
    logger.info("HANDLING USER CREATED EVENT")
    
    try:
        user_data = data.get("data", {})
        clerk_user_id = user_data.get("id")
        logger.info(f"Clerk User Data: {user_data}")
        
        logger.info(f"Clerk User ID: {clerk_user_id}")

        # Extract email
        email_addresses = user_data.get("email_addresses", [])
        logger.info(f"[IMPORTANT] :Email Addresses: {email_addresses}")
        email = email_addresses[0].get("email_address") if email_addresses else None
        logger.info(f"Email: {email}")

        # Extract username
        username = user_data.get("username") or (email.split("@")[0] if email else None)
        logger.info(f"Username: {username}")

        if not clerk_user_id:
            logger.error("No clerk_id in webhook data")
            raise HTTPException(status_code=400, detail="Invalid webhook data: missing clerk_id")

        # Check if user already exists
        existing_user = db.query(Users).filter(Users.clerk_id == clerk_user_id).first()

        if existing_user:
            logger.info(f"User {clerk_user_id} already exists with DB ID {existing_user.id}")
            return {
                "success": True,
                "message": "User already exists",
                "user_id": existing_user.id
            }

        # Create new user
        logger.info(f"Creating new user: {clerk_user_id}")
        new_user = create_user(
            db=db,
            clerk_id=clerk_user_id,
            username=username,
            email=email
        )

        logger.info(f"✅ User created successfully - DB ID: {new_user.id}")
        return {
            "success": True,
            "message": "User created successfully",
            "user_id": new_user.id
        }

    except IntegrityError as e:
        db.rollback()
        logger.warning(f"User creation conflict for {clerk_user_id}: {e}")
        return {"success": True, "message": "User creation conflict, assuming already created"}

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error creating user {clerk_user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")