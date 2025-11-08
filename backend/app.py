from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.src.routes import exercise
from backend.src.routes.app_routes import router as clerk_webhook_router
from backend.src.routes.app_routes import router as api_router
from backend.src.routes import exercise

app = FastAPI()

app.include_router(api_router)

app.include_router(clerk_webhook_router , prefix="/webhooks")



origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5172",
    "http://localhost:8000",
    "http://localhost:*",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(exercise.router, prefix="/exercise", tags=["exercise"])

@app.get("/")
async def root():
    return {"message": "Wolern API is running"}