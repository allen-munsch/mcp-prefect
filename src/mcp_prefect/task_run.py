from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from datetime import datetime

import mcp.types as types
from prefect import get_client
from prefect.states import Cancelled, Completed, Failed, Pending, Running, Scheduled
from prefect.client.schemas.filters import (
    TaskRunFilter,
    TaskRunFilterName,
    TaskRunFilterState,
    TaskRunFilterStateType,
    TaskRunFilterStateName,
    TaskRunFilterTags,
    TaskRunFilterStartTime,
    FlowRunFilter,
    FlowRunFilterId,
)
from prefect.client.schemas.sorting import TaskRunSort

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
        # Build filter objects
        task_run_filter = None
        filter_components = []
        
        if task_name:
            filter_components.append(
                TaskRunFilterName(like_=f"%{task_name}%")
            )
        
        if state_type:
            filter_components.append(
                TaskRunFilterState(
                    type=TaskRunFilterStateType(any_=[state_type.upper()])
                )
            )
        
        if state_name:
            filter_components.append(
                TaskRunFilterState(
                    name=TaskRunFilterStateName(any_=[state_name])
                )
            )
        
        if tags:
            filter_components.append(
                TaskRunFilterTags(all_=tags)
            )
        
        if start_time_after or start_time_before:
            start_time_filter_args = {}
            if start_time_after:
                start_time_filter_args["after_"] = datetime.fromisoformat(start_time_after)
            if start_time_before:
                start_time_filter_args["before_"] = datetime.fromisoformat(start_time_before)
            filter_components.append(
                TaskRunFilterStartTime(**start_time_filter_args)
            )
        
        # Combine filters if any exist
        if filter_components:
            # Create TaskRunFilter with the components
            # Note: You may need to adjust this based on how TaskRunFilter combines filters
            task_run_filter = TaskRunFilter()
            for component in filter_components:
                if isinstance(component, TaskRunFilterName):
                    task_run_filter.name = component
                elif isinstance(component, TaskRunFilterState):
                    task_run_filter.state = component
                elif isinstance(component, TaskRunFilterTags):
                    task_run_filter.tags = component
                elif isinstance(component, TaskRunFilterStartTime):
                    task_run_filter.start_time = component
        
        task_runs = await client.read_task_runs(
            task_run_filter=task_run_filter,
            limit=limit,
            offset=offset or 0
        )
        
        # Add UI links to each task run
        task_runs_result = {
            "task_runs": [
                {
                    **task_run.model_dump(),
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
        task_run_dict = task_run.model_dump()
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
        # Build filter using new filter objects
        flow_run_filter = FlowRunFilter(
            id=FlowRunFilterId(any_=[UUID(flow_run_id)])
        )
        
        task_run_filter = None
        if state_type:
            task_run_filter = TaskRunFilter(
                state=TaskRunFilterState(
                    type=TaskRunFilterStateType(any_=[state_type.upper()])
                )
            )
        
        task_runs = await client.read_task_runs(
            flow_run_filter=flow_run_filter,
            task_run_filter=task_run_filter,
            limit=limit,
            offset=offset or 0
        )
        
        # Add UI links to each task run
        task_runs_result = {
            "task_runs": [
                {
                    **task_run.model_dump(),
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
    force: bool = False,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Set a task run's state.
    
    Args:
        task_run_id: The task run UUID
        state: The new state to set (e.g., "SCHEDULED", "RUNNING", "COMPLETED", "FAILED")
        message: An optional message explaining the state change
        force: If True, disregard orchestration logic when setting the state
        
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
            state=state_obj,
            force=force
        )
        
        return [types.TextContent(type="text", text=str(result.model_dump()))]