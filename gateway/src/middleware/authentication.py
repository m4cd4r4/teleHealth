from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from ..utils.jwt_handler import decode_jwt

security = HTTPBearer()

async def verify_jwt(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token and attach user information to request state.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials"
        )
    
    token = credentials.credentials
    payload = decode_jwt(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token or expired token"
        )
    
    request.state.user = payload
    return payload

def require_role(roles: List[str]):
    """
    Middleware factory to check if user has required role.
    """
    async def role_checker(request: Request):
        user = getattr(request.state, "user", None)
        if not user or "role" not in user or user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource"
            )
        return True
    return role_checker

def get_current_user(request: Request) -> Optional[dict]:
    """
    Get current user from request state.
    Returns None if no user is authenticated.
    """
    return getattr(request.state, "user", None)
