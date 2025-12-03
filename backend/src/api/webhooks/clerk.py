from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
import logging
from svix import WebhookVerificationError
from svix.webhooks import Webhook
import os

from backend.src.config import settings
from backend.src.database.database import get_db
from backend.src.database.models import Users
from backend.src.database.crud.users import create_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/clerk")
async def clerk_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Clerk webhook events."""
    try:
        # Get webhook secret from environment
        webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
        if not webhook_secret:
            logger.error("CLERK_WEBHOOK_SECRET not set in environment")
            raise HTTPException(status_code=500, detail="Webhook secret not configured")

        # Get headers
        svix_id = request.headers.get("svix-id")
        svix_timestamp = request.headers.get("svix-timestamp")
        svix_signature = request.headers.get("svix-signature")

        if not all([svix_id, svix_timestamp, svix_signature]):
            logger.error("Missing required Svix headers")
            raise HTTPException(status_code=400, detail="Missing required headers")

        # Get body
        body = await request.body()

        logger.info(f"Received webhook: svix-id={svix_id}")

        # Verify webhook signature
        try:
            wh = Webhook(webhook_secret)
            payload = wh.verify(body, {
                "svix-id": svix_id,
                "svix-timestamp": svix_timestamp,
                "svix-signature": svix_signature,
            })
        except WebhookVerificationError as e:
            logger.error(f"Webhook verification failed: {e}")
            raise HTTPException(status_code=400, detail="Invalid signature")

        # Process the event
        event_type = payload.get("type")
        logger.info(f"Processing event type: {event_type}")

        if event_type == "user.created":
            # Handle user creation
            user_data = payload.get("data")
            logger.info(f"User created: {user_data.get('id')}")
            result = await handle_user_created(db, payload)
            return result

        elif event_type == "user.updated":
            # Handle user update
            user_data = payload.get("data")
            logger.info(f"User updated: {user_data.get('id')}")
            # Add your user update logic here

        elif event_type == "user.deleted":
            # Handle user deletion
            user_data = payload.get("data")
            logger.info(f"User deleted: {user_data.get('id')}")
            # Add your user deletion logic here
        else:
            logger.warning(f"Unhandled event type: {event_type}")

        return {"status": "success", "event_type": event_type}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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
        existing_user = db.query(Users).filter(Users.clerk_id == clerk_user_id).first()

        if existing_user:
            logger.info(f"User {clerk_user_id} already exists")
            return {"success": True, "message": "User already exists", "user_id": existing_user.id}

        # Create new user
        new_user = create_user(db=db, clerk_id=clerk_user_id, username=username, email=email)

        logger.info(f"Created user {clerk_user_id} successfully")
        return {"success": True, "message": "User created successfully", "user_id": new_user.id}

    except IntegrityError as e:
        db.rollback()
        logger.warning(f"User creation conflict for {clerk_user_id}: {e}")
        return {"success": True, "message": "User creation conflict, assuming already created"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user {clerk_user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
