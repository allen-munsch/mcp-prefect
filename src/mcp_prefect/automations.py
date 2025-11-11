"""Automations module for MCP Prefect."""

from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client

from .server import mcp


@mcp.tool
async def get_automations(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    name: Optional[str] = None,
    enabled: Optional[bool] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of automations with optional filtering.
    
    Args:
        limit: Maximum number of automations to return
        offset: Number of automations to skip
        name: Filter by automation name
        enabled: Filter by enabled status
        
    Returns:
        A list of automations with their details
    """
    try:
        async with get_client() as client:
            # Build filter parameters
            filter_dict = {}
            if name:
                filter_dict["name"] = {"like_": f"%{name}%"}
            if enabled is not None:
                filter_dict["enabled"] = {"eq_": enabled}
            
            response = await client._client.post(
                "/automations/filter",
                json={
                    "automations": filter_dict if filter_dict else None,
                    "limit": limit,
                    "offset": offset,
                    "sort": "NAME_ASC"
                }
            )
            
            automations = response.json()
            
            return [types.TextContent(type="text", text=str({"automations": automations}))]
    except Exception as e:
        # Automations may only be available in Prefect Cloud
        if "404" in str(e) or "Not Found" in str(e):
            return [types.TextContent(
                type="text",
                text="Automations are only available in Prefect Cloud. This appears to be a local Prefect instance."
            )]
        error_message = f"Error fetching automations: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def get_automation(
    automation_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get details of a specific automation by ID.
    
    Args:
        automation_id: The automation UUID
        
    Returns:
        Automation details
    """
    try:
        async with get_client() as client:
            response = await client._client.get(
                f"/automations/{automation_id}"
            )
            
            automation = response.json()
            
            return [types.TextContent(type="text", text=str(automation))]
    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            return [types.TextContent(
                type="text",
                text="Automations are only available in Prefect Cloud."
            )]
        error_message = f"Error fetching automation: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def create_automation(
    name: str,
    enabled: bool,
    trigger: Dict[str, Any],
    actions: List[Dict[str, Any]],
    description: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create an automation.
    
    Args:
        name: The name for the automation
        enabled: Whether the automation is enabled
        trigger: The trigger configuration (e.g., flow run state change, work queue events)
        actions: List of actions to take when triggered
        description: Optional description
        
    Returns:
        Details of the created automation
    """
    try:
        async with get_client() as client:
            automation_data = {
                "name": name,
                "enabled": enabled,
                "trigger": trigger,
                "actions": actions,
            }
            
            if description:
                automation_data["description"] = description
            
            response = await client._client.post(
                "/automations/",
                json=automation_data
            )
            
            created_automation = response.json()
            
            return [types.TextContent(type="text", text=str(created_automation))]
    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            return [types.TextContent(
                type="text",
                text="Automations are only available in Prefect Cloud."
            )]
        error_message = f"Error creating automation: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def update_automation(
    automation_id: str,
    name: Optional[str] = None,
    enabled: Optional[bool] = None,
    trigger: Optional[Dict[str, Any]] = None,
    actions: Optional[List[Dict[str, Any]]] = None,
    description: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update an automation.
    
    Args:
        automation_id: The automation UUID
        name: New name
        enabled: New enabled status
        trigger: New trigger configuration
        actions: New actions
        description: New description
        
    Returns:
        Details of the updated automation
    """
    try:
        async with get_client() as client:
            # Build update data
            update_data = {}
            if name is not None:
                update_data["name"] = name
            if enabled is not None:
                update_data["enabled"] = enabled
            if trigger is not None:
                update_data["trigger"] = trigger
            if actions is not None:
                update_data["actions"] = actions
            if description is not None:
                update_data["description"] = description
            
            response = await client._client.patch(
                f"/automations/{automation_id}",
                json=update_data
            )
            
            updated_automation = response.json()
            
            return [types.TextContent(type="text", text=str(updated_automation))]
    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            return [types.TextContent(
                type="text",
                text="Automations are only available in Prefect Cloud."
            )]
        error_message = f"Error updating automation: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def delete_automation(
    automation_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete an automation by ID.
    
    Args:
        automation_id: The automation UUID
        
    Returns:
        Confirmation message
    """
    try:
        async with get_client() as client:
            await client._client.delete(
                f"/automations/{automation_id}"
            )
            
            return [types.TextContent(type="text", text=f"Automation '{automation_id}' deleted successfully.")]
    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            return [types.TextContent(
                type="text",
                text="Automations are only available in Prefect Cloud."
            )]
        error_message = f"Error deleting automation: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def pause_automation(
    automation_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Pause an automation.
    
    Args:
        automation_id: The automation UUID
        
    Returns:
        Confirmation message
    """
    try:
        async with get_client() as client:
            response = await client._client.patch(
                f"/automations/{automation_id}",
                json={"enabled": False}
            )
            
            return [types.TextContent(type="text", text=f"Automation '{automation_id}' paused successfully.")]
    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            return [types.TextContent(
                type="text",
                text="Automations are only available in Prefect Cloud."
            )]
        error_message = f"Error pausing automation: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def resume_automation(
    automation_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Resume (enable) an automation.
    
    Args:
        automation_id: The automation UUID
        
    Returns:
        Confirmation message
    """
    try:
        async with get_client() as client:
            response = await client._client.patch(
                f"/automations/{automation_id}",
                json={"enabled": True}
            )
            
            return [types.TextContent(type="text", text=f"Automation '{automation_id}' resumed successfully.")]
    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            return [types.TextContent(
                type="text",
                text="Automations are only available in Prefect Cloud."
            )]
        error_message = f"Error resuming automation: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]