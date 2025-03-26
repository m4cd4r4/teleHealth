from fastapi import APIRouter
from ..services import ServiceType
from .route_utils import create_service_router

# Create a router for the communication service
# Patients and practitioners can access their own communications, admins can access all
router = create_service_router(
    service_type=ServiceType.COMMUNICATION,
    base_path="/communications",
    require_auth=True,
    allowed_roles=["patient", "practitioner", "admin"]
)
