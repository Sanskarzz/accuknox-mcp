#!/usr/bin/env python3
"""
MCP Server with Streamable HTTP Transport and Echo Tool

This server implements the Model Context Protocol using the FastMCP framework
which provides native HTTP support. It includes an echo tool for demonstration.
"""

import logging
from fastmcp import FastMCP, Context
import httpx
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("echo-mcp-server")

@mcp.tool()
def echo(ctx: Context, message: str, repeat: int = 1) -> dict:
    """
    Echo back the input text with authorization token info. Useful for testing and debugging.
    
    Args:
        message: The message to echo back
        repeat: Number of times to repeat the message (1-10, default: 1)
    
    Returns:
        The echoed message, repeated the specified number of times, plus auth info
    """
    # Validate inputs
    if not message:
        raise ValueError("Message cannot be empty")
    
    if not isinstance(repeat, int) or repeat < 1 or repeat > 10:
        raise ValueError("Repeat must be an integer between 1 and 10")
    
    # Create the echo response
    echo_response = "\n".join([message] * repeat)
    
    # Extract Authorization header from context
    auth_header = None
    bearer_token = None
    debug_info = {}
    
    # Access request headers through FastMCP Context properly
    try:
        # Get the actual request object from context
        request = ctx.request_context.request
        debug_info["request_available"] = request is not None
        
        if request and hasattr(request, 'headers'):
            debug_info["headers_available"] = True
            # Access headers (case-insensitive lookup)
            auth_header = request.headers.get('authorization') or request.headers.get('Authorization')
            
            if not auth_header:
                auth_header = "No Authorization header found"
                debug_info["all_headers"] = dict(request.headers)
            else:
                debug_info["found_auth_header"] = True
                
        else:
            auth_header = "Request object has no headers attribute"
            debug_info["request_type"] = str(type(request)) if request else "None"
            
        # Extract Bearer token if present
        if auth_header and isinstance(auth_header, str) and auth_header.startswith('Bearer '):
            bearer_token = auth_header[7:]  # Remove "Bearer " prefix
            debug_info["token_extracted"] = True
        elif auth_header and auth_header not in ['No Authorization header found', 'Request object has no headers attribute']:
            bearer_token = "Non-Bearer token format"
            debug_info["non_bearer_format"] = True
            
    except Exception as e:
        auth_header = f"Error accessing headers: {str(e)}"
        bearer_token = None
        debug_info["error"] = str(e)
    
    return {
        "echo_message": f"Echo ({repeat}x): {echo_response}",
        "authorization_info": {
            "full_header": auth_header,
            "bearer_token": bearer_token,
            "token_length": len(bearer_token) if bearer_token and bearer_token != "Non-Bearer token format" else 0
        },
        "debug_info": debug_info,
        "request_info": {
            "repeat_count": repeat,
            "original_message": message
        }
    }

@mcp.tool()
async def get_counts(
    ctx: Context,
    type: Optional[str] = "Kubearmor",
    view: Optional[str] = "List", 
    cluster_id: Optional[List[str]] = None,
    workspace_id: Optional[int] = 11,
    namespace: Optional[List[str]] = None,
    filters: Optional[List[str]] = None,
    from_time: Optional[int] = 1730399520,
    to_time: Optional[int] = 1751518034,
    log_type: Optional[str] = "active",
    search: Optional[str] = "",
    workload_type: Optional[List[str]] = None,
    workload_name: Optional[List[str]] = None
) -> dict:
    """
    Get alerts counts for different types from AccuKnox API.
    
    Args:
        type: Alert type (default: "Kubearmor")
        view: View type (default: "List")
        cluster_id: List of cluster IDs (default: empty list)
        workspace_id: Workspace ID (default: 11)
        namespace: List of namespaces (default: empty list)
        filters: List of filters (default: empty list)
        from_time: Start time timestamp (default: 1730399520)
        to_time: End time timestamp (default: 1751518034)
        log_type: Log type (default: "active")
        search: Search query (default: empty string)
        workload_type: List of workload types (default: empty list)
        workload_name: List of workload names (default: empty list)
    
    Returns:
        API response with alerts count data
    """
    # Extract Bearer token from request headers
    bearer_token = None
    try:
        request = ctx.request_context.request
        if request and hasattr(request, 'headers'):
            auth_header = request.headers.get('authorization') or request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                bearer_token = auth_header[7:]  # Remove "Bearer " prefix
    except Exception as e:
        return {"error": f"Failed to extract bearer token: {str(e)}"}
    
    if not bearer_token:
        return {"error": "No Bearer token found in request headers"}
    
    # Prepare the API request payload
    payload = {
        "Type": type,
        "View": view,
        "ClusterID": cluster_id or [],
        "WorkspaceID": workspace_id,
        "Namespace": namespace or [],
        "Filters": filters or [],
        "FromTime": from_time,
        "ToTime": to_time,
        "LogType": log_type,
        "Search": search,
        "WorkloadType": workload_type or [],
        "WorkloadName": workload_name or []
    }
    
    # Prepare headers
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://app.dev.accuknox.com/",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}",
        "X-Tenant-Id": "11",
        "Origin": "https://app.dev.accuknox.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4",
        "TE": "trailers"
    }
    
    # Make the API request
    api_url = "https://cwpp.dev.accuknox.com/monitors/v1/alerts/events/count"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            # Return the response
            return {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "data": response.json() if response.status_code == 200 else None,
                "error": response.text if response.status_code != 200 else None,
                "request_payload": payload,
                "token_used": f"Bearer {bearer_token[:8]}..." if bearer_token else None
            }
            
    except httpx.TimeoutException:
        return {"error": "Request timeout - API took too long to respond"}
    except httpx.RequestError as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# The FastMCP framework automatically creates the FastAPI app and handles
# all the MCP protocol details, including streamable HTTP transport

if __name__ == "__main__":
    # Run the server with streamable HTTP transport
    mcp.run(
        transport="http",  # Use streamable HTTP transport
        host="127.0.0.1",  # Bind only to localhost for security
        port=8000,
        log_level="info"
    ) 