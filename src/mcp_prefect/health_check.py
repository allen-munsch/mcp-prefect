from typing import Callable, List, Union

import mcp.types as types
from prefect import get_client


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_health, "get_health", "Get health status"),
    ]


async def get_health() -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get health status of the Prefect server.
    
    Returns:
        Health status information
    """
    try:
        # Test connection to Prefect by calling the health endpoint
        async with get_client() as client:
            health_status = await client.hello()
            
        return [types.TextContent(type="text", text=str(health_status))]
    
    except Exception as e:
        error_status = {
            "status": "unhealthy",
            "message": f"Error connecting to Prefect server: {str(e)}"
        }
        
        return [types.TextContent(type="text", text=str(error_status))]