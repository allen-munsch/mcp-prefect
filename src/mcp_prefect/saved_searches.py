"""Additional modules for complete MCP Prefect implementation."""

# ============================================================================
# saved_searches.py - Saved Searches Module
# ============================================================================

from typing import Any, Dict, List, Optional, Union
from uuid import UUID
import mcp.types as types
from prefect import get_client
from .server import mcp


@mcp.tool
async def get_saved_searches(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Get a list of saved searches."""
    try:
        async with get_client() as client:
            response = await client._client.post(
                "/saved_searches/filter",
                json={"limit": limit, "offset": offset}
            )
            return [types.TextContent(type="text", text=str({"saved_searches": response.json()}))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@mcp.tool
async def create_saved_search(
    name: str,
    filters: Dict[str, Any],
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Create a saved search."""
    try:
        async with get_client() as client:
            response = await client._client.post(
                "/saved_searches/",
                json={"name": name, "filters": filters}
            )
            return [types.TextContent(type="text", text=str(response.json()))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

