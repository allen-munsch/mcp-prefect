from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_work_pools, "get_work_pools", "Get all work pools"),
        (get_work_pool, "get_work_pool", "Get a work pool by name"),
        (create_work_pool, "create_work_pool", "Create a work pool"),
        (update_work_pool, "update_work_pool", "Update a work pool"),
        (delete_work_pool, "delete_work_pool", "Delete a work pool"),
        (get_scheduled_flow_runs, "get_scheduled_flow_runs", "Get scheduled flow runs for a work pool"),
        (get_work_pool_queues, "get_work_pool_queues", "Get work queues for a work pool"),
        (get_work_pool_queue, "get_work_pool_queue", "Get a specific work queue in a work pool"),
        (create_work_pool_queue, "create_work_pool_queue", "Create a work queue in a work pool"),
        (update_work_pool_queue, "update_work_pool_queue", "Update a work queue in a work pool"),
        (delete_work_pool_queue, "delete_work_pool_queue", "Delete a work queue from a work pool"),
    ]


async def get_work_pools(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get all work pools with optional pagination.
    
    Args:
        limit: Maximum number of work pools to return
        offset: Number of work pools to skip
        
    Returns:
        A list of work pools
    """
    async with get_client() as client:
        try:
            # The method name might be different based on Prefect's API
            work_pools = await client.read_work_pools(
                limit=limit,
                offset=offset
            )
            
            work_pools_result = {
                "work_pools": [work_pool.dict() for work_pool in work_pools]
            }
            
            return [types.TextContent(type="text", text=str(work_pools_result))]
        except Exception as e:
            error_message = f"Error fetching work pools: {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def get_work_pool(
    name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a work pool by name.
    
    Args:
        name: The work pool name
        
    Returns:
        Work pool details
    """
    async with get_client() as client:
        try:
            work_pool = await client.read_work_pool(name)
            
            return [types.TextContent(type="text", text=str(work_pool.dict()))]
        except Exception as e:
            error_message = f"Error fetching work pool '{name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def create_work_pool(
    name: str,
    type: str,
    description: Optional[str] = None,
    base_job_template: Optional[Dict] = None,
    is_paused: Optional[bool] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a work pool.
    
    Args:
        name: The name for the work pool
        type: The type of work pool (e.g., 'kubernetes', 'process', etc.)
        description: Optional description
        base_job_template: Optional base job template as JSON
        is_paused: Whether the work pool should be paused
        
    Returns:
        Details of the created work pool
    """
    async with get_client() as client:
        try:
            work_pool = await client.create_work_pool(
                name=name,
                work_pool_type=type,
                description=description,
                base_job_template=base_job_template or {},
                is_paused=is_paused
            )
            
            return [types.TextContent(type="text", text=str(work_pool.dict()))]
        except Exception as e:
            error_message = f"Error creating work pool: {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def update_work_pool(
    name: str,
    description: Optional[str] = None,
    base_job_template: Optional[Dict] = None,
    is_paused: Optional[bool] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a work pool.
    
    Args:
        name: The work pool name
        description: New description
        base_job_template: New base job template as JSON
        is_paused: New paused status
        
    Returns:
        Details of the updated work pool
    """
    async with get_client() as client:
        try:
            # Prepare update data
            update_data = {}
            if description is not None:
                update_data["description"] = description
            if base_job_template is not None:
                update_data["base_job_template"] = base_job_template
            if is_paused is not None:
                update_data["is_paused"] = is_paused
            
            work_pool = await client.update_work_pool(
                name=name,
                **update_data
            )
            
            return [types.TextContent(type="text", text=str(work_pool.dict()))]
        except Exception as e:
            error_message = f"Error updating work pool '{name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def delete_work_pool(
    name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a work pool by name.
    
    Args:
        name: The work pool name
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        try:
            await client.delete_work_pool(name)
            
            return [types.TextContent(type="text", text=f"Work pool '{name}' deleted successfully.")]
        except Exception as e:
            error_message = f"Error deleting work pool '{name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def get_scheduled_flow_runs(
    work_pool_name: str,
    limit: Optional[int] = None,
    scheduled_before: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get scheduled flow runs for a work pool.
    
    Args:
        work_pool_name: The work pool name
        limit: Maximum number of flow runs to return
        scheduled_before: ISO formatted timestamp
        
    Returns:
        A list of scheduled flow runs
    """
    async with get_client() as client:
        try:
            flow_runs = await client.get_scheduled_flow_runs(
                work_pool_name=work_pool_name,
                limit=limit,
                scheduled_before=scheduled_before
            )
            
            flow_runs_result = {
                "scheduled_flow_runs": [flow_run.dict() for flow_run in flow_runs]
            }
            
            return [types.TextContent(type="text", text=str(flow_runs_result))]
        except Exception as e:
            error_message = f"Error fetching scheduled flow runs for work pool '{work_pool_name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def get_work_pool_queues(
    work_pool_name: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get work queues for a work pool.
    
    Args:
        work_pool_name: The work pool name
        limit: Maximum number of queues to return
        offset: Number of queues to skip
        
    Returns:
        A list of work queues in the work pool
    """
    async with get_client() as client:
        try:
            queues = await client.read_work_pool_queues(
                work_pool_name=work_pool_name,
                limit=limit,
                offset=offset
            )
            
            queues_result = {
                "work_pool_queues": [queue.dict() for queue in queues]
            }
            
            return [types.TextContent(type="text", text=str(queues_result))]
        except Exception as e:
            error_message = f"Error fetching work queues for work pool '{work_pool_name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def get_work_pool_queue(
    work_pool_name: str,
    queue_name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a specific work queue in a work pool.
    
    Args:
        work_pool_name: The work pool name
        queue_name: The work queue name
        
    Returns:
        Work queue details
    """
    async with get_client() as client:
        try:
            queue = await client.read_work_pool_queue(
                work_pool_name=work_pool_name,
                queue_name=queue_name
            )
            
            return [types.TextContent(type="text", text=str(queue.dict()))]
        except Exception as e:
            error_message = f"Error fetching work queue '{queue_name}' in work pool '{work_pool_name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def create_work_pool_queue(
    work_pool_name: str,
    name: str,
    description: Optional[str] = None,
    is_paused: Optional[bool] = None,
    concurrency_limit: Optional[int] = None,
    priority: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a work queue in a work pool.
    
    Args:
        work_pool_name: The work pool name
        name: The name for the work queue
        description: Optional description
        is_paused: Whether the queue is paused
        concurrency_limit: Optional concurrency limit
        priority: Optional priority
        
    Returns:
        Details of the created work queue
    """
    async with get_client() as client:
        try:
            queue = await client.create_work_pool_queue(
                work_pool_name=work_pool_name,
                name=name,
                description=description,
                is_paused=is_paused,
                concurrency_limit=concurrency_limit,
                priority=priority
            )
            
            return [types.TextContent(type="text", text=str(queue.dict()))]
        except Exception as e:
            error_message = f"Error creating work queue in work pool '{work_pool_name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def update_work_pool_queue(
    work_pool_name: str,
    queue_name: str,
    description: Optional[str] = None,
    is_paused: Optional[bool] = None,
    concurrency_limit: Optional[int] = None,
    priority: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a work queue in a work pool.
    
    Args:
        work_pool_name: The work pool name
        queue_name: The work queue name
        description: New description
        is_paused: New paused status
        concurrency_limit: New concurrency limit
        priority: New priority
        
    Returns:
        Details of the updated work queue
    """
    async with get_client() as client:
        try:
            # Prepare update data
            update_data = {}
            if description is not None:
                update_data["description"] = description
            if is_paused is not None:
                update_data["is_paused"] = is_paused
            if concurrency_limit is not None:
                update_data["concurrency_limit"] = concurrency_limit
            if priority is not None:
                update_data["priority"] = priority
            
            queue = await client.update_work_pool_queue(
                work_pool_name=work_pool_name,
                queue_name=queue_name,
                **update_data
            )
            
            return [types.TextContent(type="text", text=str(queue.dict()))]
        except Exception as e:
            error_message = f"Error updating work queue '{queue_name}' in work pool '{work_pool_name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]


async def delete_work_pool_queue(
    work_pool_name: str,
    queue_name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a work queue from a work pool.
    
    Args:
        work_pool_name: The work pool name
        queue_name: The work queue name
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        try:
            await client.delete_work_pool_queue(
                work_pool_name=work_pool_name,
                queue_name=queue_name
            )
            
            return [types.TextContent(type="text", text=f"Work queue '{queue_name}' deleted from work pool '{work_pool_name}' successfully.")]
        except Exception as e:
            error_message = f"Error deleting work queue '{queue_name}' from work pool '{work_pool_name}': {str(e)}"
            return [types.TextContent(type="text", text=error_message)]