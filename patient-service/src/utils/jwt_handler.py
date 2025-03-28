from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional, List
from ..config import settings

# Security scheme for JWT bearer token
security = HTTPBearer()

def decode_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token.
    
    Args:
        token: The token to decode
        
    Returns:
        The decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Get the current user from the JWT token.
    
    Args:
        credentials: The HTTP authorization credentials
        
    Returns:
        The user data from the token
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    token = credentials.credentials
    payload = decode_jwt(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload

async def get_current_user_with_roles(required_roles: List[str] = None):
    """
    Dependency to get the current user and verify they have the required roles.
    
    Args:
        required_roles: List of roles that are allowed to access the endpoint
        
    Returns:
        A dependency function that checks the user's roles
    """
    async def _get_user_with_roles(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if required_roles is None:
            return user
            
        user_role = user.get("role")
        if user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return user
    
    return _get_user_with_roles
