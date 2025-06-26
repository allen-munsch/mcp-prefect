from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client

from .envs import PREFECT_API_URL
from .server import mcp


def get_deployment_url(deployment_id: str) -> str:
    base_url = PREFECT_API_URL.replace("/api", "")
    return f"{base_url}/deployments/{deployment_id}"


@mcp.tool
async def get_deployments(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    flow_name: Optional[str] = None,
    name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    is_schedule_active: Optional[bool] = None,
    work_queue_name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of deployments with optional filtering.
    
    Args:
        limit: Maximum number of deployments to return
        offset: Number of deployments to skip
        flow_name: Filter by flow name
        name: Filter by deployment name
        tags: Filter by tags
        is_schedule_active: Filter by schedule active status
        work_queue_name: Filter by work queue name
        
    Returns:
        A list of deployments with their details
    """
    try:
        async with get_client() as client:
            # Build deployment filter
            deployment_filter = None
            if any([name, tags, is_schedule_active, work_queue_name]):
                from prefect.client.schemas.filters import DeploymentFilter
                
                filter_dict = {}
                if name:
                    filter_dict["name"] = {"like_": f"%{name}%"}
                if tags:
                    filter_dict["tags"] = {"all_": tags}
                if is_schedule_active is not None:
                    filter_dict["is_schedule_active"] = {"eq_": is_schedule_active}
                if work_queue_name:
                    filter_dict["work_queue_name"] = {"eq_": work_queue_name}
                
                deployment_filter = DeploymentFilter(**filter_dict)
            
            # Build flow filter if flow_name is specified
            flow_filter = None
            if flow_name:
                from prefect.client.schemas.filters import FlowFilter
                
                flow_filter = FlowFilter(name={"like_": f"%{flow_name}%"})
            
            # Query using proper filter objects
            deployments = await client.read_deployments(
                deployment_filter=deployment_filter,
                flow_filter=flow_filter,
                limit=limit,
                offset=offset,
            )
            
            # Add UI links to each deployment
            deployments_result = {
                "deployments": [
                    {
                        **deployment.model_dump(),
                        "ui_url": get_deployment_url(str(deployment.id))
                    }
                    for deployment in deployments
                ]
            }
            
            return [types.TextContent(type="text", text=str(deployments_result))]
    except Exception as e:
        # Add proper error handling
        return [types.TextContent(type="text", text=str({"error": str(e)}))]


@mcp.tool
async def get_deployment(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get details of a specific deployment by ID.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Deployment details
    """
    async with get_client() as client:
        deployment = await client.read_deployment(UUID(deployment_id))
        
        # Add UI link
        deployment_dict = deployment.model_dump()
        deployment_dict["ui_url"] = get_deployment_url(deployment_id)
        
        return [types.TextContent(type="text", text=str(deployment_dict))]


@mcp.tool
async def create_flow_run_from_deployment(
    deployment_id: str,
    parameters: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    idempotency_key: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a flow run from a deployment.
    
    Args:
        deployment_id: The deployment UUID
        parameters: Optional parameters to pass to the flow run
        name: Optional name for the flow run
        tags: Optional tags for the flow run
        idempotency_key: Optional idempotency key
        
    Returns:
        Details of the created flow run
    """
    async with get_client() as client:
        parameters = parameters or {}
        
        flow_run = await client.create_flow_run_from_deployment(
            deployment_id=UUID(deployment_id),
            parameters=parameters,
            name=name,
            tags=tags,
            idempotency_key=idempotency_key,
        )
        
        # Add URL
        flow_run_dict = flow_run.model_dump()
        flow_run_dict["ui_url"] = PREFECT_API_URL.replace("/api", "") + f"/flow-runs/{flow_run.id}"
        
        return [types.TextContent(type="text", text=str(flow_run_dict))]


@mcp.tool
async def delete_deployment(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a deployment by ID.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.delete_deployment(UUID(deployment_id))
        
        return [types.TextContent(type="text", text=f"Deployment '{deployment_id}' deleted successfully.")]


@mcp.tool
async def update_deployment(
    deployment_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
    parameters: Optional[Dict[str, Any]] = None,
    work_queue_name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a deployment.
    
    Args:
        deployment_id: The deployment UUID
        name: New name for the deployment
        description: New description
        version: New version
        tags: New tags
        parameters: New parameters
        work_queue_name: New work queue name
        
    Returns:
        Details of the updated deployment
    """
    async with get_client() as client:
        # Get current deployment
        deployment = await client.read_deployment(UUID(deployment_id))
        
        # Prepare update data
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if version is not None:
            update_data["version"] = version
        if tags is not None:
            update_data["tags"] = tags
        if parameters is not None:
            update_data["parameters"] = parameters
        if work_queue_name is not None:
            update_data["work_queue_name"] = work_queue_name
        
        # Update deployment
        updated_deployment = await client.update_deployment(
            deployment_id=UUID(deployment_id),
            **update_data
        )
        
        # Add UI link
        updated_deployment_dict = updated_deployment.model_dump()
        updated_deployment_dict["ui_url"] = get_deployment_url(deployment_id)
        
        return [types.TextContent(type="text", text=str(updated_deployment_dict))]


@mcp.tool
async def get_deployment_schedule(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a deployment's schedule.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Schedule details
    """
    async with get_client() as client:
        schedule = await client.read_deployment_schedule(UUID(deployment_id))
        
        return [types.TextContent(type="text", text=str(schedule.model_dump()))]


@mcp.tool
async def set_deployment_schedule(
    deployment_id: str,
    cron: Optional[str] = None,
    interval_seconds: Optional[int] = None,
    anchor_date: Optional[str] = None,
    timezone: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Set a deployment's schedule.
    
    Args:
        deployment_id: The deployment UUID
        cron: Cron expression for the schedule
        interval_seconds: Alternative to cron - interval in seconds
        anchor_date: Required for interval schedules - the anchor date
        timezone: Timezone for the schedule
        
    Returns:
        Updated schedule details
    """
    async with get_client() as client:
        # Check schedule type
        if cron is not None and interval_seconds is not None:
            return [types.TextContent(
                type="text",
                text="Cannot specify both cron and interval_seconds. Choose one schedule type."
            )]
        
        if cron is not None:
            # Set cron schedule
            schedule = await client.set_deployment_schedule(
                deployment_id=UUID(deployment_id),
                schedule={"cron": cron, "timezone": timezone}
            )
        elif interval_seconds is not None:
            # Set interval schedule
            if not anchor_date:
                return [types.TextContent(
                    type="text",
                    text="anchor_date is required for interval schedules"
                )]
            
            schedule = await client.set_deployment_schedule(
                deployment_id=UUID(deployment_id),
                schedule={
                    "interval": interval_seconds,
                    "anchor_date": anchor_date,
                    "timezone": timezone
                }
            )
        else:
            return [types.TextContent(
                type="text",
                text="Must specify either cron or interval_seconds to set a schedule"
            )]
        
        return [types.TextContent(type="text", text=str(schedule.model_dump()))]


@mcp.tool
async def pause_deployment_schedule(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Pause a deployment's schedule.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.pause_deployment_schedule(UUID(deployment_id))
        
        return [types.TextContent(type="text", text=f"Schedule for deployment '{deployment_id}' paused successfully.")]


@mcp.tool
async def resume_deployment_schedule(
    deployment_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Resume a deployment's schedule.
    
    Args:
        deployment_id: The deployment UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.resume_deployment_schedule(UUID(deployment_id))
        
        return [types.TextContent(type="text", text=f"Schedule for deployment '{deployment_id}' resumed successfully.")]
