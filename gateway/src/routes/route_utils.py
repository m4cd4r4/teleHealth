from fastapi import APIRouter, Request, Depends, HTTPException, status
import httpx
from typing import List, Optional
from ..services import ServiceType, service_registry
from ..utils import proxy_response
from ..middleware import verify_jwt, require_role

def create_service_router(service_type: ServiceType, base_path: str, require_auth: bool = True, allowed_roles: Optional[List[str]] = None):
    """
    Create a router for a specific service.
    This handles forwarding requests to the appropriate microservice.
    
    Args:
        service_type: The type of service to route to
        base_path: The base path for the service (e.g., "/patients")
        require_auth: Whether authentication is required
        allowed_roles: List of roles allowed to access this service
    
    Returns:
        A FastAPI router configured to forward requests
    """
    router = APIRouter()
    
    # Define dependencies based on auth requirements
    dependencies = []
    if require_auth:
        dependencies.append(Depends(verify_jwt))
        if allowed_roles:
            dependencies.append(Depends(require_role(allowed_roles)))
    
    async def forward_request(request: Request, path: str = ""):
        """
        Forward a request to the appropriate microservice.
        """
        service_url = service_registry.get_service_url(service_type)
        
        if not service_registry.is_service_healthy(service_type):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{service_type.value} service is currently unavailable"
            )
        
        # Construct the target URL
        target_url = f"{service_url}/api/v1{base_path}/{path}"
        if path:
            # Remove trailing slash if path is provided
            target_url = target_url.rstrip("/")
        
        # Get request details
        method = request.method
        headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
        
        # Forward the request
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(
                    target_url,
                    headers=headers,
                    params=request.query_params
                )
            elif method == "POST":
                body = await request.body()
                response = await client.post(
                    target_url,
                    content=body,
                    headers=headers
                )
            elif method == "PUT":
                body = await request.body()
                response = await client.put(
                    target_url,
                    content=body,
                    headers=headers
                )
            elif method == "DELETE":
                response = await client.delete(
                    target_url,
                    headers=headers
                )
            elif method == "PATCH":
                body = await request.body()
                response = await client.patch(
                    target_url,
                    content=body,
                    headers=headers
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method {method} not allowed"
                )
            
            return await proxy_response(response)
    
    # Add routes for all common HTTP methods
    router.add_api_route("/{path:path}", forward_request, methods=["GET"], dependencies=dependencies)
    router.add_api_route("/{path:path}", forward_request, methods=["POST"], dependencies=dependencies)
    router.add_api_route("/{path:path}", forward_request, methods=["PUT"], dependencies=dependencies)
    router.add_api_route("/{path:path}", forward_request, methods=["DELETE"], dependencies=dependencies)
    router.add_api_route("/{path:path}", forward_request, methods=["PATCH"], dependencies=dependencies)
    
    # Add a route for the base path
    router.add_api_route("", forward_request, methods=["GET"], dependencies=dependencies)
    router.add_api_route("", forward_request, methods=["POST"], dependencies=dependencies)
    
    return router
