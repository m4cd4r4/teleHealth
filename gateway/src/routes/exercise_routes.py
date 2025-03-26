from fastapi import APIRouter
from ..services import ServiceType
from .route_utils import create_service_router

# Create a router for the exercise service
# Patients can access their own exercises, practitioners can create and manage exercises, admins can access all
router = create_service_router(
    service_type=ServiceType.EXERCISE,
    base_path="/exercises",
    require_auth=True,
    allowed_roles=["patient", "practitioner", "admin"]
)
