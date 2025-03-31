from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import settings, API_PREFIX
from .database import init_db
# Import routers
from .routes import exercise_routes, program_routes 

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("exercise_service")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Exercise Service for TeleHealth Platform",
    version="0.1.0",
    docs_url=f"{API_PREFIX}/docs",
    redoc_url=f"{API_PREFIX}/redoc",
    openapi_url=f"{API_PREFIX}/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(exercise_routes.router, prefix=API_PREFIX)
app.include_router(program_routes.router, prefix=API_PREFIX)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Initializing exercise service...")
    await init_db()
    logger.info("Exercise service initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down exercise service...")
    # Add cleanup code here if needed
    logger.info("Exercise service shut down")

@app.get("/")
async def root():
    """Root endpoint for basic check"""
    return {"message": "Exercise Service is running"}

@app.get(f"{API_PREFIX}/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "0.1.0"
    }
