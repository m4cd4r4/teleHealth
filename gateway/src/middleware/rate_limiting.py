import time
from fastapi import Request, HTTPException, status
import redis
from ..config import settings

# Initialize Redis client
# Note: In a real implementation, you would handle connection errors
try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        socket_connect_timeout=1,
        socket_timeout=1
    )
except Exception as e:
    print(f"Warning: Redis connection failed: {e}")
    # Fallback to a dummy implementation for development
    class DummyRedis:
        def get(self, key):
            return None
        def incr(self, key):
            return 1
        def expire(self, key, time):
            pass
        def pipeline(self):
            return self
        def execute(self):
            return [1, True]
    redis_client = DummyRedis()

async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware to implement rate limiting based on client IP.
    """
    # Get client IP
    client_ip = request.client.host
    
    # Create a key for this IP
    key = f"rate_limit:{client_ip}"
    
    # Check if this IP has exceeded rate limits
    current = redis_client.get(key)
    
    if current and int(current) > settings.RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    
    # Increment the counter
    pipe = redis_client.pipeline()
    pipe.incr(key)
    # Set expiry if it doesn't exist
    pipe.expire(key, settings.RATE_LIMIT_WINDOW_SECONDS)
    pipe.execute()
    
    # Process the request
    response = await call_next(request)
    
    # Add rate limit headers
    remaining = settings.RATE_LIMIT_MAX_REQUESTS - int(redis_client.get(key) or 0)
    response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_MAX_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
    response.headers["X-RateLimit-Reset"] = str(settings.RATE_LIMIT_WINDOW_SECONDS)
    
    return response
