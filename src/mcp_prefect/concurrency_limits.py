from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_concurrency_limits, "get_concurrency_limits", "Get all concurrency limits"),
        (get_concurrency_limit, "get_concurrency_limit", "Get a concurrency limit by ID"),
        (get_concurrency_limit_by_tag, "get_concurrency_limit_by_tag", "Get a concurrency limit by tag"),
        (create_concurrency_limit, "create_concurrency_limit", "Create a concurrency limit"),
        (update_concurrency_limit, "update_concurrency_limit", "Update a concurrency limit"),
        (delete_concurrency_limit, "delete_concurrency_limit", "Delete a concurrency limit"),
        (increment_concurrency_limit, "increment_concurrency_limit", "Increment a concurrency limit"),
        (decrement_concurrency_limit, "decrement_concurrency_limit", "Decrement a concurrency limit"),
        (reset_concurrency_limit, "reset_concurrency_limit", "Reset a concurrency limit by tag"),
    ]


async def get_concurrency_limits() -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get all concurrency limits.
    
    Returns:
        A list of concurrency limits
    """
    async with get_client() as client:
        try:
            # Prefect API doesn't support limit/offset on concurrency limits endpoint directly
            # Use the filter endpoint instead
            concurrency_limits = await client.read_concurrency_limits_filter()
            
            limits_result = {
                "concurrency_limits": [limit.dict() for limit in concurrency_limits]
            }
            
            return [types.TextContent(type="text", text=str(limits_result))]
        except Exception as e:
            error_message = f"Error fetching concurrency limits: {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def get_concurrency_limit(
    limit_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a concurrency limit by ID.
    
    Args:
        limit_id: The concurrency limit UUID
        
    Returns:
        Concurrency limit details
    """
    async with get_client() as client:
        try:
            concurrency_limit = await client.read_concurrency_limit(UUID(limit_id))
            
            return [types.TextContent(type="text", text=str(concurrency_limit.dict()))]
        except Exception as e:
            error_message = f"Error fetching concurrency limit {limit_id}: {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def get_concurrency_limit_by_tag(
    tag: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a concurrency limit by tag.
    
    Args:
        tag: The concurrency limit tag
        
    Returns:
        Concurrency limit details
    """
    async with get_client() as client:
        try:
            concurrency_limit = await client.read_concurrency_limit_by_tag(tag)
            
            return [types.TextContent(type="text", text=str(concurrency_limit.dict()))]
        except Exception as e:
            error_message = f"Error fetching concurrency limit for tag '{tag}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def create_concurrency_limit(
    tag: str,
    concurrency_limit: int,
    active: Optional[bool] = True,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a concurrency limit.
    
    Args:
        tag: The tag to limit
        concurrency_limit: The maximum allowed concurrency
        active: Whether the limit is active
        
    Returns:
        Details of the created concurrency limit
    """
    async with get_client() as client:
        try:
            limit = await client.create_concurrency_limit(
                tag=tag,
                concurrency_limit=concurrency_limit,
                active=active
            )
            
            return [types.TextContent(type="text", text=str(limit.dict()))]
        except Exception as e:
            error_message = f"Error creating concurrency limit: {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def update_concurrency_limit(
    limit_id: str,
    concurrency_limit: Optional[int] = None,
    active: Optional[bool] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a concurrency limit.
    
    Args:
        limit_id: The concurrency limit UUID
        concurrency_limit: The new maximum allowed concurrency
        active: Whether the limit is active
        
    Returns:
        Details of the updated concurrency limit
    """
    async with get_client() as client:
        try:
            # Prepare update data
            update_data = {}
            if concurrency_limit is not None:
                update_data["concurrency_limit"] = concurrency_limit
            if active is not None:
                update_data["active"] = active
            
            updated_limit = await client.update_concurrency_limit(
                id=UUID(limit_id),
                **update_data
            )
            
            return [types.TextContent(type="text", text=str(updated_limit.dict()))]
        except Exception as e:
            error_message = f"Error updating concurrency limit {limit_id}: {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def delete_concurrency_limit(
    limit_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a concurrency limit by ID.
    
    Args:
        limit_id: The concurrency limit UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        try:
            await client.delete_concurrency_limit(UUID(limit_id))
            
            return [types.TextContent(type="text", text=f"Concurrency limit '{limit_id}' deleted successfully.")]
        except Exception as e:
            error_message = f"Error deleting concurrency limit {limit_id}: {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def increment_concurrency_limit(
    tag: str,
    delta: int = 1,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Increment a concurrency limit by tag.
    
    Args:
        tag: The concurrency limit tag
        delta: Amount to increment by (default 1)
        
    Returns:
        Updated concurrency limit details
    """
    async with get_client() as client:
        try:
            updated_limit = await client.increment_concurrency_limit(
                tag=tag,
                delta=delta
            )
            
            return [types.TextContent(type="text", text=str(updated_limit.dict()))]
        except Exception as e:
            error_message = f"Error incrementing concurrency limit for tag '{tag}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def decrement_concurrency_limit(
    tag: str,
    delta: int = 1,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Decrement a concurrency limit by tag.
    
    Args:
        tag: The concurrency limit tag
        delta: Amount to decrement by (default 1)
        
    Returns:
        Updated concurrency limit details
    """
    async with get_client() as client:
        try:
            updated_limit = await client.decrement_concurrency_limit(
                tag=tag,
                delta=delta
            )
            
            return [types.TextContent(type="text", text=str(updated_limit.dict()))]
        except Exception as e:
            error_message = f"Error decrementing concurrency limit for tag '{tag}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def reset_concurrency_limit(
    tag: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Reset a concurrency limit by tag, setting its current count to 0.
    
    Args:
        tag: The concurrency limit tag
        
    Returns:
        Updated concurrency limit details
    """
    async with get_client() as client:
        try:
            updated_limit = await client.reset_concurrency_limit(tag=tag)
            
            return [types.TextContent(type="text", text=str(updated_limit.dict()))]
        except Exception as e:
            error_message = f"Error resetting concurrency limit for tag '{tag}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]