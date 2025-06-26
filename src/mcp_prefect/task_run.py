from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client
from prefect.states import Cancelled, Completed, Failed, Pending, Running, Scheduled

from .envs import PREFECT_API_URL
from .server import mcp


def get_task_run_url(task_run_id: str) -> str:
    base_url = PREFECT_API_URL.replace("/api", "")
    return f"{base_url}/task-runs/{task_run_id}"


@mcp.tool
async def get_task_runs(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    task_name: Optional[str] = None,
    state_type: Optional[str] = None,
    state_name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    start_time_before: Optional[str] = None,
    start_time_after: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of task runs with optional filtering.
    
    Args:
        limit: Maximum number of task runs to return
        offset: Number of task runs to skip
        task_name: Filter by task name
        state_type: Filter by state type (e.g., "RUNNING", "COMPLETED", "FAILED")
        state_name: Filter by state name
        tags: Filter by tags
        start_time_before: ISO formatted datetime string
        start_time_after: ISO formatted datetime string
        
    Returns:
        A list of task runs with their details
    """
    async with get_client() as client:
        # Build filter parameters
        filters = {}
        if task_name:
            filters["task_name"] = {"like_": f"%{task_name}%"}
        if state_type:
            filters["state"] = {"type": {"any_": [state_type.upper()]}}
        if state_name:
            filters["state"] = {"name": {"any_": [state_name]}}
        if tags:
            filters["tags"] = {"all_": tags}
        if start_time_after:
            filters["start_time"] = {"ge_": start_time_after}
        if start_time_before:
            if "start_time" in filters:
                filters["start_time"]["le_"] = start_time_before
            else:
                filters["start_time"] = {"le_": start_time_before}
        
        task_runs = await client.read_task_runs(
            limit=limit,
            offset=offset,
            **filters
        )
        
        # Add UI links to each task run
        task_runs_result = {
            "task_runs": [
                {
                    **task_run.dict(),
                    "ui_url": get_task_run_url(str(task_run.id))
                }
                for task_run in task_runs
            ]
        }
        
        return [types.TextContent(type="text", text=str(task_runs_result))]


@mcp.tool
async def get_task_run(
    task_run_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get details of a specific task run by ID.
    
    Args:
        task_run_id: The task run UUID
        
    Returns:
        Task run details
    """
    async with get_client() as client:
        task_run = await client.read_task_run(UUID(task_run_id))
        
        # Add UI link
        task_run_dict = task_run.dict()
        task_run_dict["ui_url"] = get_task_run_url(task_run_id)
        
        return [types.TextContent(type="text", text=str(task_run_dict))]


@mcp.tool
async def get_task_runs_by_flow_run(
    flow_run_id: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    state_type: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get task runs for a specific flow run.
    
    Args:
        flow_run_id: The flow run UUID
        limit: Maximum number of task runs to return
        offset: Number of task runs to skip
        state_type: Filter by state type (e.g., "RUNNING", "COMPLETED", "FAILED")
        
    Returns:
        A list of task runs for the specified flow run
    """
    async with get_client() as client:
        # Build filter parameters
        filters = {"flow_run_id": {"eq_": UUID(flow_run_id)}}
        if state_type:
            filters["state"] = {"type": {"any_": [state_type.upper()]}}
        
        task_runs = await client.read_task_runs(
            limit=limit,
            offset=offset,
            **filters
        )
        
        # Add UI links to each task run
        task_runs_result = {
            "task_runs": [
                {
                    **task_run.dict(),
                    "ui_url": get_task_run_url(str(task_run.id))
                }
                for task_run in task_runs
            ]
        }
        
        return [types.TextContent(type="text", text=str(task_runs_result))]


@mcp.tool
async def set_task_run_state(
    task_run_id: str,
    state: str,
    message: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Set a task run's state.
    
    Args:
        task_run_id: The task run UUID
        state: The new state to set (e.g., "SCHEDULED", "RUNNING", "COMPLETED", "FAILED")
        message: An optional message explaining the state change
        
    Returns:
        Result of the state change operation
    """
    async with get_client() as client:
        state_obj = None
        if state.upper() == "SCHEDULED":
            state_obj = Scheduled(message=message)
        elif state.upper() == "RUNNING":
            state_obj = Running(message=message)
        elif state.upper() == "COMPLETED":
            state_obj = Completed(message=message)
        elif state.upper() == "FAILED":
            state_obj = Failed(message=message)
        elif state.upper() == "PENDING":
            state_obj = Pending(message=message)
        elif state.upper() == "CANCELLED":
            state_obj = Cancelled(message=message)
        else:
            return [types.TextContent(
                type="text", 
                text=f"Invalid state '{state}'. Must be one of: SCHEDULED, RUNNING, COMPLETED, FAILED, PENDING, CANCELLED"
            )]
        
        result = await client.set_task_run_state(
            task_run_id=UUID(task_run_id),
            state=state_obj
        )
        
        return [types.TextContent(type="text", text=str(result.dict()))]
