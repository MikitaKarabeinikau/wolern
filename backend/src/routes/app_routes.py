from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.src.database import models
from ..database.database import (
    get_user_by_clerk_id,
    create_user, get_user_by_username,
    get_user_by_id,get_user_vocabulary,SessionLocal
)

from backend.utils import authenticate_and_get_user_details
import json
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
import os 
from svix.webhooks import Webhook
from backend.src.database.database import get_database


router = APIRouter()

class WebhookPayload(BaseModel):
    data: dict
    object: str
    type: str



@router.post("/clerk")
async def handle_user_created(request: Request, db: Session = Depends(get_database)):
    # Get raw body for signature verification
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
    if not webhook_secret:
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
                existing_usuer = db.query(models.Users).filter(models.Users.clerk_id == clerk_user_id).first()
                if existing_usuer:
                    return {"success": True, "message": "User already exists"}

                new_user = models.Users(
                    clerk_id=clerk_user_id,
                    username = None,
                    email=email,
                    created_at=datetime.utcnow()
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return {"success": True, "message": "User created successfully"}
            except IntegrityError:
                # This handles the unlikely case where the user.created event is sent twice
                # and another check might be needed, but the first check should prevent it.
                return {"success": True, "message": "User creation conflict, assuming already created"}
            except Exception as e:
                if db:
                    db.rollback()
            # Log the error for debugging purposes
                raise HTTPException(status_code=500, detail=f"Database error on user creation: {e}")
        
        user_data = data.get("data", {})
        user_id = user_data.get("id")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

        
    return {"success": True, "message": f"Event type {payload['type']} handled"}
        
            

@router.get("/users/")
async def get_users(db: Session = Depends(get_database)):
    users = db.query(models.Users).all()
    return {"users": users}


@router.get("/my-vocabulary")
async def my_vocabulary(request: Request, db: Session = Depends(get_database)):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details["user_id"]

    my_vocabulary = get_user_vocabulary(db, user_id=user_id)
    return {"vocabulary": my_vocabulary}


class UserCreateRequest(BaseModel):
    clerk_user_id: str
    username: str = None
    email: str