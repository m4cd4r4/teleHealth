from .auth_routes import router as auth_router
from .patient_routes import router as patient_router
from .appointment_routes import router as appointment_router
from .exercise_routes import router as exercise_router
from .progress_routes import router as progress_router
from .communication_routes import router as communication_router
from .file_routes import router as file_router

__all__ = [
    'auth_router',
    'patient_router',
    'appointment_router',
    'exercise_router',
    'progress_router',
    'communication_router',
    'file_router',
]
