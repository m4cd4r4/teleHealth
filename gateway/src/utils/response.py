from fastapi.responses import JSONResponse
from typing import Any, Dict, List, Optional, Union
import httpx

async def proxy_response(response: httpx.Response) -> Any:
    """
    Proxy a response from a microservice to the client.
    This preserves the status code, headers, and body.
    """
    content = response.json() if response.headers.get("content-type") == "application/json" else response.text
    
    return JSONResponse(
        content=content,
        status_code=response.status_code,
        headers={k: v for k, v in response.headers.items() if k.lower() not in ["transfer-encoding", "content-encoding", "content-length"]}
    )

def error_response(status_code: int, message: str) -> JSONResponse:
    """
    Create a standardized error response.
    """
    return JSONResponse(
        status_code=status_code,
        content={"error": message}
    )

def success_response(data: Any = None, message: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a standardized success response.
    """
    response = {"success": True}
    
    if data is not None:
        response["data"] = data
    
    if message:
        response["message"] = message
    
    return response
