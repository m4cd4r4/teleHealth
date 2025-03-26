from fastapi import APIRouter
from ..services import ServiceType
from .route_utils import create_service_router

# Create a router for the progress service
# Patients can access their own progress, practitioners can access their patients' progress, admins can access all
router = create_service_router(
    service_type=ServiceType.PROGRESS,
    base_path="/progress",
    require_auth=True,
    allowed_roles=["patient", "practitioner", "admin"]
)
