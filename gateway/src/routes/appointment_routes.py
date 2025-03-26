from fastapi import APIRouter
from ..services import ServiceType
from .route_utils import create_service_router

# Create a router for the appointment service
# Patients can access their own appointments, practitioners can access their appointments, admins can access all
router = create_service_router(
    service_type=ServiceType.APPOINTMENT,
    base_path="/appointments",
    require_auth=True,
    allowed_roles=["patient", "practitioner", "admin"]
)
