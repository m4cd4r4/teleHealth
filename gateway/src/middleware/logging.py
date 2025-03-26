import time
import uuid
import logging
from fastapi import Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("api_gateway")

async def logging_middleware(request: Request, call_next):
    """
    Middleware to log request and response details.
    Also adds a unique request ID to each request.
    """
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Log request details
    start_time = time.time()
    
    # Extract user ID if authenticated
    user_id = "anonymous"
    if hasattr(request.state, "user") and request.state.user:
        user_id = request.state.user.get("sub", "anonymous")
    
    # Log the incoming request
    logger.info(f"Request started | {request_id} | {request.method} {request.url.path} | User: {user_id}")
    
    # Process the request
    try:
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log the response
        logger.info(
            f"Request completed | {request_id} | {request.method} {request.url.path} | "
            f"Status: {response.status_code} | Time: {process_time:.4f}s | User: {user_id}"
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
    except Exception as e:
        # Log exceptions
        process_time = time.time() - start_time
        logger.error(
            f"Request failed | {request_id} | {request.method} {request.url.path} | "
            f"Error: {str(e)} | Time: {process_time:.4f}s | User: {user_id}"
        )
        raise
