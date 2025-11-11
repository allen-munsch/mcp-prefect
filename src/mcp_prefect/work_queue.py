from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client
from prefect.client.schemas.filters import (
    WorkQueueFilter,
    WorkQueueFilterName,
)

from .server import mcp


@mcp.tool
async def get_work_queues(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    name: Optional[str] = None,
    is_paused: Optional[bool] = None,
    work_pool_name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of work queues with optional filtering.
    
    Args:
        limit: Maximum number of work queues to return
        offset: Number of work queues to skip
        name: Filter by name
        is_paused: Filter by paused status
        work_pool_name: Filter by work pool name
        
    Returns:
        A list of work queues with their details
    """
    async with get_client() as client:
        # Build filter object
        work_queue_filter = None
        
        if name or is_paused is not None:
            work_queue_filter = WorkQueueFilter()
            if name:
                work_queue_filter.name = WorkQueueFilterName(like_=f"%{name}%")
            # Note: is_paused filter is not directly available in WorkQueueFilter
            # We'll handle it by filtering the results after the API call
        
        work_queues = await client.read_work_queues(
            work_queue_filter=work_queue_filter,
            work_pool_name=work_pool_name,
            limit=limit,
            offset=offset or 0
        )
        
        # Apply is_paused filter manually if needed
        if is_paused is not None:
            work_queues = [wq for wq in work_queues if wq.is_paused == is_paused]
        
        work_queues_result = {
            "work_queues": [work_queue.model_dump() for work_queue in work_queues]
        }
        
        return [types.TextContent(type="text", text=str(work_queues_result))]


@mcp.tool
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
        
        return [types.TextContent(type="text", text=str(work_queue.model_dump()))]


@mcp.tool
async def get_work_queue_by_name(
    name: str,
    work_pool_name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a work queue by name.
    
    Args:
        name: The work queue name
        work_pool_name: Optional work pool name to scope the search
        
    Returns:
        Work queue details
    """
    async with get_client() as client:
        work_queue = await client.read_work_queue_by_name(
            name=name,
            work_pool_name=work_pool_name
        )
        
        return [types.TextContent(type="text", text=str(work_queue.model_dump()))]


@mcp.tool
async def create_work_queue(
    name: str,
    description: Optional[str] = None,
    is_paused: Optional[bool] = None,
    concurrency_limit: Optional[int] = None,
    work_pool_name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a work queue.
    
    Args:
        name: The name for the work queue
        description: Optional description
        is_paused: Whether the queue should be paused upon creation
        concurrency_limit: Optional concurrency limit
        work_pool_name: Optional work pool name to create the queue in
        
    Returns:
        Details of the created work queue
    """
    async with get_client() as client:
        work_queue = await client.create_work_queue(
            name=name,
            description=description,
            is_paused=is_paused,
            concurrency_limit=concurrency_limit,
            work_pool_name=work_pool_name,
        )
        
        return [types.TextContent(type="text", text=str(work_queue.model_dump()))]


@mcp.tool
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
        
        await client.update_work_queue(
            id=UUID(work_queue_id),
            **update_data
        )
        
        # Read the updated work queue to return its details
        updated_work_queue = await client.read_work_queue(UUID(work_queue_id))
        return [types.TextContent(type="text", text=str(updated_work_queue.model_dump()))]


@mcp.tool
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
        # Correct method name is delete_work_queue_by_id
        await client.delete_work_queue_by_id(UUID(work_queue_id))
        
        return [types.TextContent(type="text", text=f"Work queue '{work_queue_id}' deleted successfully.")]


@mcp.tool
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
        await client.update_work_queue(
            id=UUID(work_queue_id),
            is_paused=True
        )
        
        # Read the updated work queue to return its details
        updated_work_queue = await client.read_work_queue(UUID(work_queue_id))
        return [types.TextContent(type="text", text=str(updated_work_queue.model_dump()))]


@mcp.tool
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
        await client.update_work_queue(
            id=UUID(work_queue_id),
            is_paused=False
        )
        
        # Read the updated work queue to return its details
        updated_work_queue = await client.read_work_queue(UUID(work_queue_id))
        return [types.TextContent(type="text", text=str(updated_work_queue.model_dump()))]


@mcp.tool
async def get_work_queue_runs(
    work_queue_id: str,
    limit: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get flow runs for a specific work queue.
    
    Args:
        work_queue_id: The work queue UUID
        limit: Maximum number of flow runs to return
        
    Returns:
        A list of flow runs in the work queue
    """
    async with get_client() as client:
        flow_runs = await client.get_runs_in_work_queue(
            id=UUID(work_queue_id),
            limit=limit or 10
        )
        
        flow_runs_result = {
            "flow_runs": [flow_run.model_dump() for flow_run in flow_runs]
        }
        
        return [types.TextContent(type="text", text=str(flow_runs_result))]