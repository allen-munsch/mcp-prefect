from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_work_queues, "get_work_queues", "Get all work queues"),
        (get_work_queue, "get_work_queue", "Get a work queue by ID"),
        (get_work_queue_by_name, "get_work_queue_by_name", "Get a work queue by name"),
        (create_work_queue, "create_work_queue", "Create a work queue"),
        (update_work_queue, "update_work_queue", "Update a work queue"),
        (delete_work_queue, "delete_work_queue", "Delete a work queue"),
        (pause_work_queue, "pause_work_queue", "Pause a work queue"),
        (resume_work_queue, "resume_work_queue", "Resume a work queue"),
    ]


async def get_work_queues(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    name: Optional[str] = None,
    is_paused: Optional[bool] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of work queues with optional filtering.
    
    Args:
        limit: Maximum number of work queues to return
        offset: Number of work queues to skip
        name: Filter by name
        is_paused: Filter by paused status
        
    Returns:
        A list of work queues with their details
    """
    async with get_client() as client:
        # Build filter parameters
        filters = {}
        if name:
            filters["name"] = {"like_": f"%{name}%"}
        if is_paused is not None:
            filters["is_paused"] = {"eq_": is_paused}
        
        work_queues = await client.read_work_queues(
            limit=limit,
            offset=offset,
            **filters
        )
        
        work_queues_result = {
            "work_queues": [work_queue.dict() for work_queue in work_queues]
        }
        
        return [types.TextContent(type="text", text=str(work_queues_result))]


async def get_work_queue(
    work_queue_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get details of a specific work queue by ID.
    
    Args:
        work_queue_id: The work queue UUID
        
    Returns:
        Work queue details
    """
    async with get_client() as client:
        work_queue = await client.read_work_queue(UUID(work_queue_id))
        
        return [types.TextContent(type="text", text=str(work_queue.dict()))]


async def get_work_queue_by_name(
    name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a work queue by name.
    
    Args:
        name: The work queue name
        
    Returns:
        Work queue details
    """
    async with get_client() as client:
        work_queue = await client.read_work_queue_by_name(name)
        
        return [types.TextContent(type="text", text=str(work_queue.dict()))]


async def create_work_queue(
    name: str,
    description: Optional[str] = None,
    is_paused: Optional[bool] = None,
    concurrency_limit: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a work queue.
    
    Args:
        name: The name for the work queue
        description: Optional description
        is_paused: Whether the queue should be paused upon creation
        concurrency_limit: Optional concurrency limit
        
    Returns:
        Details of the created work queue
    """
    async with get_client() as client:
        work_queue = await client.create_work_queue(
            name=name,
            description=description,
            is_paused=is_paused,
            concurrency_limit=concurrency_limit,
        )
        
        return [types.TextContent(type="text", text=str(work_queue.dict()))]


async def update_work_queue(
    work_queue_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_paused: Optional[bool] = None,
    concurrency_limit: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a work queue.
    
    Args:
        work_queue_id: The work queue UUID
        name: New name
        description: New description
        is_paused: New paused status
        concurrency_limit: New concurrency limit
        
    Returns:
        Details of the updated work queue
    """
    async with get_client() as client:
        # Prepare update data
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if is_paused is not None:
            update_data["is_paused"] = is_paused
        if concurrency_limit is not None:
            update_data["concurrency_limit"] = concurrency_limit
        
        work_queue = await client.update_work_queue(
            id=UUID(work_queue_id),
            **update_data
        )
        
        return [types.TextContent(type="text", text=str(work_queue.dict()))]


async def delete_work_queue(
    work_queue_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a work queue by ID.
    
    Args:
        work_queue_id: The work queue UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.delete_work_queue(UUID(work_queue_id))
        
        return [types.TextContent(type="text", text=f"Work queue '{work_queue_id}' deleted successfully.")]


async def pause_work_queue(
    work_queue_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Pause a work queue.
    
    Args:
        work_queue_id: The work queue UUID
        
    Returns:
        Details of the updated work queue
    """
    async with get_client() as client:
        work_queue = await client.update_work_queue(
            id=UUID(work_queue_id),
            is_paused=True
        )
        
        return [types.TextContent(type="text", text=str(work_queue.dict()))]


async def resume_work_queue(
    work_queue_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Resume a work queue.
    
    Args:
        work_queue_id: The work queue UUID
        
    Returns:
        Details of the updated work queue
    """
    async with get_client() as client:
        work_queue = await client.update_work_queue(
            id=UUID(work_queue_id),
            is_paused=False
        )
        
        return [types.TextContent(type="text", text=str(work_queue.dict()))]