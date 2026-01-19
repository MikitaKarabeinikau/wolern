from pathlib import Path
from backend.src.database.models import init_db  # FIX: Add full path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.src.api.webhooks import clerk
from backend.src.config import settings

# ============================================================================
# LOGGING SETUP - CONFIGURE ONCE
# ============================================================================
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Remove duplicate - configure logging ONCE
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "app.log"),
        logging.StreamHandler()
    ],
    force=True  # Override any previous configuration
)

logger = logging.getLogger(__name__)

# ============================================================================
# FASTAPI APP
# ============================================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# ============================================================================
# CORS MIDDLEWARE
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# ============================================================================
# ROUTERS
# ============================================================================
app.include_router(clerk.router, prefix="/webhooks", tags=["Webhooks"])

# ============================================================================
# ROOT ENDPOINTS
# ============================================================================
@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
    }

# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}", exc_info=True)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")