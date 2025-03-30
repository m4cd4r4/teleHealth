from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, Dict, Any
import httpx
import json
import logging
from jose import jwt, JWTError

from ..config import settings

# Configure logging
logger = logging.getLogger("appointment_service.utils.auth")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.AUTH_SERVICE_URL}/auth/login",
    auto_error=False
)

async def get_current_user(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Depends(oauth2_scheme)
) -> Dict[str, Any]:
    """
    Get the current user from the token in the Authorization header.
    
    This function validates the JWT token by calling the auth service.
    
    Parameters:
    - authorization: The Authorization header value
    - token: The token from the OAuth2 scheme
    
    Returns:
    - Dict containing the user information
    
    Raises:
    - HTTPException: If the token is invalid or the user is not authenticated
    """
    # Extract token from Authorization header if provided
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    
    if not token:
        logger.warning("No authentication token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Verify token with auth service
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.AUTH_SERVICE_URL}/auth/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                logger.warning(f"Token verification failed with status code {response.status_code}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_data = response.json()
            logger.debug(f"User authenticated: {user_data.get('username', 'unknown')}")
            return user_data
            
    except httpx.RequestError as e:
        logger.error(f"Error communicating with auth service: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get the current active user.
    
    This function checks if the authenticated user is active.
    
    Parameters:
    - current_user: The authenticated user
    
    Returns:
    - Dict containing the user information
    
    Raises:
    - HTTPException: If the user is inactive
    """
    if not current_user.get("is_active", False):
        logger.warning(f"Inactive user attempted access: {current_user.get('username', 'unknown')}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def check_admin_permission(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Check if the current user has admin permission.
    
    Parameters:
    - current_user: The authenticated user
    
    Returns:
    - Dict containing the user information
    
    Raises:
    - HTTPException: If the user does not have admin permission
    """
    if not current_user.get("is_admin", False):
        logger.warning(f"User without admin permission attempted admin action: {current_user.get('username', 'unknown')}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )
    return current_user


async def check_practitioner_permission(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Check if the current user has practitioner permission.
    
    Parameters:
    - current_user: The authenticated user
    
    Returns:
    - Dict containing the user information
    
    Raises:
    - HTTPException: If the user does not have practitioner permission
    """
    user_type = current_user.get("user_type", "").lower()
    if user_type != "practitioner" and not current_user.get("is_admin", False):
        logger.warning(f"User without practitioner permission attempted practitioner action: {current_user.get('username', 'unknown')}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Practitioner permission required"
        )
    return current_user
