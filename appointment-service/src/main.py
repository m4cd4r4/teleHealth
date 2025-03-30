from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio

from .config import settings, API_PREFIX
from .database import init_db
from .routes import appointment_routes, schedule_routes, notification_routes, calendar_routes

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("appointment_service")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Appointment Service for TeleHealth Platform",
    version="0.1.0",
    docs_url=f"{API_PREFIX}/docs",
    redoc_url=f"{API_PREFIX}/redoc",
    openapi_url=f"{API_PREFIX}/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(appointment_routes.router, prefix=API_PREFIX)
app.include_router(schedule_routes.router, prefix=API_PREFIX)
app.include_router(notification_routes.router, prefix=API_PREFIX)
app.include_router(calendar_routes.router, prefix=API_PREFIX)

@app.on_event("startup")
async def startup_event():
    """Initialize database and other resources on startup"""
    logger.info("Initializing appointment service...")
    await init_db()
    logger.info("Appointment service initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down appointment service...")
    # Add cleanup code here if needed
    logger.info("Appointment service shut down")


@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "Appointment Service is running"}


@app.get(f"{API_PREFIX}/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "0.1.0"
    }
