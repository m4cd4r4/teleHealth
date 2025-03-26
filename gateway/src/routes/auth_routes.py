from fastapi import APIRouter, Request, HTTPException, status
import httpx
from ..services import ServiceType, service_registry
from ..utils import proxy_response

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    """
    Forward registration request to auth service.
    """
    auth_service_url = service_registry.get_service_url(ServiceType.AUTH)
    
    if not service_registry.is_service_healthy(ServiceType.AUTH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is currently unavailable"
        )
    
    # Get request body
    body = await request.json()
    
    # Forward the request to the auth service
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{auth_service_url}/api/v1/auth/register",
            json=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"}
        )
        
        return await proxy_response(response)

@router.post("/login")
async def login(request: Request):
    """
    Forward login request to auth service.
    """
    auth_service_url = service_registry.get_service_url(ServiceType.AUTH)
    
    if not service_registry.is_service_healthy(ServiceType.AUTH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is currently unavailable"
        )
    
    # Get request body
    body = await request.body()
    
    # Forward the request to the auth service
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{auth_service_url}/api/v1/auth/login",
            content=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"}
        )
        
        return await proxy_response(response)

@router.post("/refresh-token")
async def refresh_token(request: Request):
    """
    Forward token refresh request to auth service.
    """
    auth_service_url = service_registry.get_service_url(ServiceType.AUTH)
    
    if not service_registry.is_service_healthy(ServiceType.AUTH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is currently unavailable"
        )
    
    # Get request body
    body = await request.json()
    
    # Forward the request to the auth service
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{auth_service_url}/api/v1/auth/refresh-token",
            json=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"}
        )
        
        return await proxy_response(response)

@router.post("/verify-email/{token}")
async def verify_email(token: str, request: Request):
    """
    Forward email verification request to auth service.
    """
    auth_service_url = service_registry.get_service_url(ServiceType.AUTH)
    
    if not service_registry.is_service_healthy(ServiceType.AUTH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is currently unavailable"
        )
    
    # Forward the request to the auth service
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{auth_service_url}/api/v1/auth/verify-email/{token}",
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"}
        )
        
        return await proxy_response(response)

@router.post("/forgot-password")
async def forgot_password(request: Request):
    """
    Forward password reset request to auth service.
    """
    auth_service_url = service_registry.get_service_url(ServiceType.AUTH)
    
    if not service_registry.is_service_healthy(ServiceType.AUTH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is currently unavailable"
        )
    
    # Get request body
    body = await request.json()
    
    # Forward the request to the auth service
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{auth_service_url}/api/v1/auth/forgot-password",
            json=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"}
        )
        
        return await proxy_response(response)

@router.post("/reset-password/{token}")
async def reset_password(token: str, request: Request):
    """
    Forward password reset confirmation to auth service.
    """
    auth_service_url = service_registry.get_service_url(ServiceType.AUTH)
    
    if not service_registry.is_service_healthy(ServiceType.AUTH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is currently unavailable"
        )
    
    # Get request body
    body = await request.json()
    
    # Forward the request to the auth service
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{auth_service_url}/api/v1/auth/reset-password/{token}",
            json=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"}
        )
        
        return await proxy_response(response)
