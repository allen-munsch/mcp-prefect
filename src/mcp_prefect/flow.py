from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client

from .envs import PREFECT_API_URL


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_flows, "get_flows", "Get all flows"),
        (get_flow, "get_flow", "Get a flow by ID"),
        (delete_flow, "delete_flow", "Delete a flow by ID"),
    ]


def get_flow_url(flow_id: str) -> str:
    """Generate a UI URL for a flow."""
    base_url = PREFECT_API_URL.replace("/api", "")
    return f"{base_url}/flows/{flow_id}"


async def get_flows(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    flow_name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of flows with optional filtering.
    
    Args:
        limit: Maximum number of flows to return
        offset: Number of flows to skip
        flow_name: Filter flows by name
        tags: Filter flows by tags
        created_after: ISO formatted datetime string for filtering flows created after this time
        created_before: ISO formatted datetime string for filtering flows created before this time
        
    Returns:
        A list of flows with their details
    """
    try:
        async with get_client() as client:
            # Build filter parameters
            filters = {}
            if flow_name:
                filters["name"] = {"like_": f"%{flow_name}%"}
            if tags:
                filters["tags"] = {"all_": tags}
            if created_after:
                filters["created"] = {"ge_": created_after}
            if created_before:
                if "created" in filters:
                    filters["created"]["le_"] = created_before
                else:
                    filters["created"] = {"le_": created_before}
                    
            flows = await client.read_flows(
                limit=limit,
                offset=offset,
                **filters
            )
            
            # Handle empty results
            if not flows:
                return [types.TextContent(type="text", text=str({"flows": []}))]
            
            # Add UI links to each flow
            flows_with_links = []
            for flow in flows:
                flow_dict = flow.dict()
                flow_dict["ui_url"] = get_flow_url(str(flow.id))
                flows_with_links.append(flow_dict)
                
            flows_result = {"flows": flows_with_links}
            
            return [types.TextContent(type="text", text=str(flows_result))]
        
    except Exception as e:
        error_message = f"Error fetching flows: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


async def get_flow(
    flow_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get details of a specific flow by ID.
    
    Args:
        flow_id: The flow UUID
        
    Returns:
        Flow details
    """
    try:
        async with get_client() as client:
            # Validate flow_id
            try:
                flow_uuid = UUID(flow_id)
            except ValueError:
                return [types.TextContent(
                    type="text", 
                    text=f"Invalid flow ID format: {flow_id}. Must be a valid UUID."
                )]
            
            flow = await client.read_flow(flow_uuid)
            
            # Add UI link
            flow_dict = flow.dict()
            flow_dict["ui_url"] = get_flow_url(flow_id)
            
            return [types.TextContent(type="text", text=str(flow_dict))]
    
    except Exception as e:
        error_message = f"Error fetching flow {flow_id}: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


async def delete_flow(
    flow_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a flow by ID.
    
    Args:
        flow_id: The flow UUID
        
    Returns:
        Confirmation message
    """
    try:
        async with get_client() as client:
            # Validate flow_id
            try:
                flow_uuid = UUID(flow_id)
            except ValueError:
                return [types.TextContent(
                    type="text", 
                    text=f"Invalid flow ID format: {flow_id}. Must be a valid UUID."
                )]
            
            await client.delete_flow(flow_uuid)
            
            return [types.TextContent(type="text", text=f"Flow '{flow_id}' deleted successfully.")]
    
    except Exception as e:
        error_message = f"Error deleting flow {flow_id}: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]