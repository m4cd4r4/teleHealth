from fastapi import APIRouter
from ..controllers.auth_controller import router as auth_controller_router

# Create router
router = APIRouter()

# Include controller routes
router.include_router(auth_controller_router, prefix="")
