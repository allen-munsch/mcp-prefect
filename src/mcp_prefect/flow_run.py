from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client
from prefect.states import Cancelled, Completed, Failed, Pending, Running, Scheduled

from .envs import PREFECT_API_URL


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_flow_runs, "get_flow_runs", "Get all flow runs"),
        (get_flow_run, "get_flow_run", "Get a flow run by ID"),
        (get_flow_runs_by_flow, "get_flow_runs_by_flow", "Get flow runs for a specific flow"),
        (restart_flow_run, "restart_flow_run", "Restart a flow run"),
        (cancel_flow_run, "cancel_flow_run", "Cancel a flow run"),
        (delete_flow_run, "delete_flow_run", "Delete a flow run"),
        (set_flow_run_state, "set_flow_run_state", "Set a flow run's state"),
    ]


def get_flow_run_url(flow_run_id: str) -> str:
    base_url = PREFECT_API_URL.replace("/api", "")
    return f"{base_url}/flow-runs/{flow_run_id}"


async def get_flow_runs(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    flow_name: Optional[str] = None,
    state_type: Optional[str] = None,
    state_name: Optional[str] = None,
    deployment_id: Optional[str] = None,
    tags: Optional[List[str]] = None,
    start_time_before: Optional[str] = None,
    start_time_after: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of flow runs with optional filtering.
    
    Args:
        limit: Maximum number of flow runs to return
        offset: Number of flow runs to skip
        flow_name: Filter by flow name
        state_type: Filter by state type (e.g., "RUNNING", "COMPLETED", "FAILED")
        state_name: Filter by state name
        deployment_id: Filter by deployment ID
        tags: Filter by tags
        start_time_before: ISO formatted datetime string
        start_time_after: ISO formatted datetime string
        
    Returns:
        A list of flow runs with their details
    """
    async with get_client() as client:
        # Build filter parameters
        filters = {}
        if flow_name:
            filters["flow_name"] = {"like_": f"%{flow_name}%"}
        if state_type:
            filters["state"] = {"type": {"any_": [state_type.upper()]}}
        if state_name:
            filters["state"] = {"name": {"any_": [state_name]}}
        if deployment_id:
            filters["deployment_id"] = {"eq_": UUID(deployment_id)}
        if tags:
            filters["tags"] = {"all_": tags}
        if start_time_after:
            filters["start_time"] = {"ge_": start_time_after}
        if start_time_before:
            if "start_time" in filters:
                filters["start_time"]["le_"] = start_time_before
            else:
                filters["start_time"] = {"le_": start_time_before}
        
        flow_runs = await client.read_flow_runs(
            limit=limit,
            offset=offset,
            **filters
        )
        
        # Add UI links to each flow run
        flow_runs_result = {
            "flow_runs": [
                {
                    **flow_run.dict(),
                    "ui_url": get_flow_run_url(str(flow_run.id))
                }
                for flow_run in flow_runs
            ]
        }
        
        return [types.TextContent(type="text", text=str(flow_runs_result))]


async def get_flow_run(
    flow_run_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get details of a specific flow run by ID.
    
    Args:
        flow_run_id: The flow run UUID
        
    Returns:
        Flow run details
    """
    async with get_client() as client:
        flow_run = await client.read_flow_run(UUID(flow_run_id))
        
        # Add UI link
        flow_run_dict = flow_run.dict()
        flow_run_dict["ui_url"] = get_flow_run_url(flow_run_id)
        
        return [types.TextContent(type="text", text=str(flow_run_dict))]


async def get_flow_runs_by_flow(
    flow_id: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    state_type: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get flow runs for a specific flow.
    
    Args:
        flow_id: The flow UUID
        limit: Maximum number of flow runs to return
        offset: Number of flow runs to skip
        state_type: Filter by state type (e.g., "RUNNING", "COMPLETED", "FAILED")
        
    Returns:
        A list of flow runs for the specified flow
    """
    async with get_client() as client:
        # Build filter parameters
        filters = {"flow_id": {"eq_": UUID(flow_id)}}
        if state_type:
            filters["state"] = {"type": {"any_": [state_type.upper()]}}
        
        flow_runs = await client.read_flow_runs(
            limit=limit,
            offset=offset,
            **filters
        )
        
        # Add UI links to each flow run
        flow_runs_result = {
            "flow_runs": [
                {
                    **flow_run.dict(),
                    "ui_url": get_flow_run_url(str(flow_run.id))
                }
                for flow_run in flow_runs
            ]
        }
        
        return [types.TextContent(type="text", text=str(flow_runs_result))]


async def restart_flow_run(
    flow_run_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Restart a flow run.
    
    Args:
        flow_run_id: The flow run UUID
        
    Returns:
        Details of the new flow run
    """
    async with get_client() as client:
        flow_run_id_uuid = UUID(flow_run_id)
        new_flow_run = await client.create_flow_run_from_flow_run(flow_run_id_uuid)
        
        new_flow_run_dict = new_flow_run.dict()
        new_flow_run_dict["ui_url"] = get_flow_run_url(str(new_flow_run.id))
        
        return [types.TextContent(type="text", text=str(new_flow_run_dict))]


async def cancel_flow_run(
    flow_run_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Cancel a flow run.
    
    Args:
        flow_run_id: The flow run UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.set_flow_run_state(
            flow_run_id=UUID(flow_run_id),
            state=Cancelled(message="Cancelled via MCP")
        )
        
        return [types.TextContent(type="text", text=f"Flow run '{flow_run_id}' cancelled successfully.")]


async def delete_flow_run(
    flow_run_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a flow run.
    
    Args:
        flow_run_id: The flow run UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.delete_flow_run(UUID(flow_run_id))
        
        return [types.TextContent(type="text", text=f"Flow run '{flow_run_id}' deleted successfully.")]


async def set_flow_run_state(
    flow_run_id: str,
    state: str,
    message: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Set a flow run's state.
    
    Args:
        flow_run_id: The flow run UUID
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
        
        result = await client.set_flow_run_state(
            flow_run_id=UUID(flow_run_id),
            state=state_obj
        )
        
        return [types.TextContent(type="text", text=str(result.dict()))]