from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from ..config import settings

def create_token_with_expiry(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token with an expiry time.
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional expiry time delta
        
    Returns:
        The encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt

def create_access_token(data: dict) -> str:
    """
    Create an access token with the default expiry time.
    
    Args:
        data: The data to encode in the token
        
    Returns:
        The encoded access token
    """
    return create_token_with_expiry(
        data,
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )

def create_refresh_token(data: dict) -> str:
    """
    Create a refresh token with a longer expiry time.
    
    Args:
        data: The data to encode in the token
        
    Returns:
        The encoded refresh token
    """
    return create_token_with_expiry(
        data,
        expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    )

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
