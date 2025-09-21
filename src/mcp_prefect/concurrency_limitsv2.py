"""Concurrency Limits module for MCP Prefect."""

from typing import List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client

from .server import mcp


@mcp.tool
async def get_concurrency_limits_v2(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    active: Optional[bool] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of global concurrency limits (v2).
    
    Args:
        limit: Maximum number of concurrency limits to return
        offset: Number of concurrency limits to skip
        active: Filter by active status
        
    Returns:
        A list of concurrency limits with their details
    """
    try:
        async with get_client() as client:
            # Use the v2 API for concurrency limits
            response = await client._client.post(
                "/v2/concurrency_limits/filter",
                json={
                    "limit": limit,
                    "offset": offset,
                }
            )
            
            limits = response.json()
            
            return [types.TextContent(type="text", text=str({"concurrency_limits": limits}))]
    except Exception as e:
        error_message = f"Error fetching concurrency limits: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def get_concurrency_limit_v2(
    id_or_name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a global concurrency limit by ID or name (v2).
    
    Args:
        id_or_name: The concurrency limit UUID or name
        
    Returns:
        Concurrency limit details
    """
    try:
        async with get_client() as client:
            response = await client._client.get(
                f"/v2/concurrency_limits/{id_or_name}"
            )
            
            limit = response.json()
            
            return [types.TextContent(type="text", text=str(limit))]
    except Exception as e:
        error_message = f"Error fetching concurrency limit: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def create_concurrency_limit_v2(
    name: str,
    limit: int,
    active: Optional[bool] = True,
    denied_slots: Optional[int] = 0,
    slot_decay_per_second: Optional[float] = 0.0,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a global concurrency limit (v2).
    
    Args:
        name: The name for the concurrency limit
        limit: The maximum number of concurrent slots
        active: Whether the limit is active
        denied_slots: Number of denied slots
        slot_decay_per_second: Rate at which slots decay
        
    Returns:
        Details of the created concurrency limit
    """
    try:
        async with get_client() as client:
            response = await client._client.post(
                "/v2/concurrency_limits/",
                json={
                    "name": name,
                    "limit": limit,
                    "active": active,
                    "denied_slots": denied_slots,
                    "slot_decay_per_second": slot_decay_per_second,
                }
            )
            
            created_limit = response.json()
            
            return [types.TextContent(type="text", text=str(created_limit))]
    except Exception as e:
        error_message = f"Error creating concurrency limit: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def update_concurrency_limit_v2(
    id_or_name: str,
    name: Optional[str] = None,
    limit: Optional[int] = None,
    active: Optional[bool] = None,
    denied_slots: Optional[int] = None,
    slot_decay_per_second: Optional[float] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a global concurrency limit (v2).
    
    Args:
        id_or_name: The concurrency limit UUID or name
        name: New name
        limit: New limit
        active: New active status
        denied_slots: New denied slots
        slot_decay_per_second: New slot decay rate
        
    Returns:
        Details of the updated concurrency limit
    """
    try:
        async with get_client() as client:
            # Build update payload
            update_data = {}
            if name is not None:
                update_data["name"] = name
            if limit is not None:
                update_data["limit"] = limit
            if active is not None:
                update_data["active"] = active
            if denied_slots is not None:
                update_data["denied_slots"] = denied_slots
            if slot_decay_per_second is not None:
                update_data["slot_decay_per_second"] = slot_decay_per_second
            
            response = await client._client.patch(
                f"/v2/concurrency_limits/{id_or_name}",
                json=update_data
            )
            
            updated_limit = response.json()
            
            return [types.TextContent(type="text", text=str(updated_limit))]
    except Exception as e:
        error_message = f"Error updating concurrency limit: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def delete_concurrency_limit_v2(
    id_or_name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a global concurrency limit (v2).
    
    Args:
        id_or_name: The concurrency limit UUID or name
        
    Returns:
        Confirmation message
    """
    try:
        async with get_client() as client:
            await client._client.delete(
                f"/v2/concurrency_limits/{id_or_name}"
            )
            
            return [types.TextContent(type="text", text=f"Concurrency limit '{id_or_name}' deleted successfully.")]
    except Exception as e:
        error_message = f"Error deleting concurrency limit: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


# Legacy v1 concurrency limit functions for task runs
@mcp.tool
async def get_concurrency_limits(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get task run concurrency limits (legacy v1).
    
    Args:
        limit: Maximum number of concurrency limits to return
        offset: Number of concurrency limits to skip
        
    Returns:
        A list of task run concurrency limits
    """
    try:
        async with get_client() as client:
            response = await client._client.post(
                "/concurrency_limits/filter",
                json={
                    "limit": limit,
                    "offset": offset,
                }
            )
            
            limits = response.json()
            
            return [types.TextContent(type="text", text=str({"concurrency_limits": limits}))]
    except Exception as e:
        error_message = f"Error fetching concurrency limits: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def get_concurrency_limit_by_tag(
    tag: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a task run concurrency limit by tag (legacy v1).
    
    Args:
        tag: The concurrency limit tag
        
    Returns:
        Concurrency limit details
    """
    try:
        async with get_client() as client:
            response = await client._client.get(
                f"/concurrency_limits/tag/{tag}"
            )
            
            limit = response.json()
            
            return [types.TextContent(type="text", text=str(limit))]
    except Exception as e:
        error_message = f"Error fetching concurrency limit: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def create_concurrency_limit(
    tag: str,
    concurrency_limit: int,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a task run concurrency limit (legacy v1).
    
    Args:
        tag: The tag for the concurrency limit
        concurrency_limit: The maximum number of concurrent task runs
        
    Returns:
        Details of the created concurrency limit
    """
    try:
        async with get_client() as client:
            response = await client._client.post(
                "/concurrency_limits/",
                json={
                    "tag": tag,
                    "concurrency_limit": concurrency_limit,
                }
            )
            
            created_limit = response.json()
            
            return [types.TextContent(type="text", text=str(created_limit))]
    except Exception as e:
        error_message = f"Error creating concurrency limit: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def delete_concurrency_limit_by_tag(
    tag: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a task run concurrency limit by tag (legacy v1).
    
    Args:
        tag: The concurrency limit tag
        
    Returns:
        Confirmation message
    """
    try:
        async with get_client() as client:
            await client._client.delete(
                f"/concurrency_limits/tag/{tag}"
            )
            
            return [types.TextContent(type="text", text=f"Concurrency limit with tag '{tag}' deleted successfully.")]
    except Exception as e:
        error_message = f"Error deleting concurrency limit: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]