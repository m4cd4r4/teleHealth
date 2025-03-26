from fastapi import APIRouter
from ..services import ServiceType
from .route_utils import create_service_router

# Create a router for the file service
# All authenticated users can access files, but the file service will handle permissions
router = create_service_router(
    service_type=ServiceType.FILE,
    base_path="/files",
    require_auth=True,
    allowed_roles=["patient", "practitioner", "admin"]
)
