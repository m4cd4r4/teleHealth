from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .middleware import logging_middleware, rate_limit_middleware
from .routes import (
    auth_router,
    patient_router,
    appointment_router,
    exercise_router,
    progress_router,
    communication_router,
    file_router
)
from .config import settings

app = FastAPI(
    title="TeleHealth API Gateway",
    description="API Gateway for the TeleHealth Physiotherapy Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.middleware("http")(logging_middleware)
app.middleware("http")(rate_limit_middleware)

# Include all route modules
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(patient_router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(appointment_router, prefix="/api/v1/appointments", tags=["Appointments"])
app.include_router(exercise_router, prefix="/api/v1/exercises", tags=["Exercises"])
app.include_router(progress_router, prefix="/api/v1/progress", tags=["Progress"])
app.include_router(communication_router, prefix="/api/v1/communications", tags=["Communications"])
app.include_router(file_router, prefix="/api/v1/files", tags=["Files"])

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for the API Gateway.
    """
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with basic information about the API.
    """
    return {
        "message": "TeleHealth API Gateway",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_GATEWAY_HOST,
        port=settings.API_GATEWAY_PORT,
        reload=True
    )
