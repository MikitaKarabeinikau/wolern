from fastapi import APIRouter, Depends, HTTPException, Request
import os
import json
from datetime import datetime
from svix.webhooks import Webhook
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.src.database.database import get_database
from backend.src.database.models import Users
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/clerk")
async def handle_user_created(request: Request, db: Session = Depends(get_database)):
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
    if not webhook_secret:
        logger.error("Webhook secret not configured")
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    body = await request.body()
    payload = body.decode('utf-8')
    headers = dict(request.headers)

    try:
        webhook = Webhook(webhook_secret)
        webhook.verify(payload, headers)

        data = json.loads(payload)
        if data.get("type") == "user.created":
            clerk_user_id = data["data"]["id"]
            email_addresses = data["data"].get("email_addresses", [])
            email = email_addresses[0].get("email_address") if email_addresses else None

            try:
                existing_user = db.query(Users).filter(Users.clerk_id == clerk_user_id).first()
                if existing_user:
                    logger.info(f"User with clerk_id '{clerk_user_id}' already exists")
                    return {"success": True, "message": "User already exists"}

                new_user = Users(
                    clerk_id=clerk_user_id,
                    username = None,
                    email=email,
                    created_at=datetime.utcnow()
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                logger.info(f"User with clerk_id '{clerk_user_id}' created successfully")
                return {"success": True, "message": "User created successfully"}
            except IntegrityError:
                logger.warning(f"User creation conflict for clerk_id '{clerk_user_id}', assuming already created")
                return {"success": True, "message": "User creation conflict, assuming already created"}
            except Exception as e:
                if db:
                    db.rollback()
                logger.error(f"Database error on user creation: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Database error on user creation: {e}")
        
        user_data = data.get("data", {})
        user_id = user_data.get("id")

    except Exception as e:
        logger.error(f"Error handling webhook: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"Event type {data.get('type')} handled")
    return {"success": True, "message": f"Event type {data.get('type')} handled"}