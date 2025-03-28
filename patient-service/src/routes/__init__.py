# Patient Service Routes Package

from .patient_routes import router as patient_router
from .medical_record_routes import router as medical_record_router

# Export all routers
__all__ = [
    "patient_router",
    "medical_record_router"
]
