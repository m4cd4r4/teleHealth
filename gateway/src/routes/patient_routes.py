from fastapi import APIRouter
from ..services import ServiceType
from .route_utils import create_service_router

# Create a router for the patient service
# Patients can access their own data, practitioners can access their patients' data, admins can access all
router = create_service_router(
    service_type=ServiceType.PATIENT,
    base_path="/patients",
    require_auth=True,
    allowed_roles=["patient", "practitioner", "admin"]
)
