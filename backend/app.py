from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import os 
import psycopg2
from dotenv import load_dotenv
from backend.src.routes.app_routes import router as clerk_webhook_router

app = FastAPI()

app.include_router(clerk_webhook_router , prefix="/webhooks")


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

