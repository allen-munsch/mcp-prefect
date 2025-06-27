from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client

from .server import mcp


@mcp.tool
async def get_workspaces(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of accessible workspaces.
    
    Args:
        limit: Maximum number of workspaces to return
        offset: Number of workspaces to skip
        name: Filter workspaces by name (note: filtering may not be supported by all Prefect versions)
        
    Returns:
        A list of workspaces with their details
    """
    try:
        async with get_client() as client:
            workspaces = await client.read_workspaces(
                limit=limit,
                offset=offset,
            )
            
            workspaces_result = {
                "workspaces": [workspace.dict() for workspace in workspaces]
            }
            
            return [types.TextContent(type="text", text=str(workspaces_result))]
    except Exception as e:
        # For local Prefect instances, workspace APIs may not be available
        return [types.TextContent(
            type="text",
            text="Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance."
        )]


@mcp.tool
async def get_current_workspace() -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get the current workspace.
    
    Returns:
        Details of the current workspace
    """
    try:
        async with get_client() as client:
            workspace = await client.read_workspace()
            
            return [types.TextContent(type="text", text=str(workspace.dict()))]
    except Exception as e:
        # For local Prefect instances, workspace APIs may not be available
        return [types.TextContent(
            type="text",
            text="Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance."
        )]


@mcp.tool
async def get_workspace(
    workspace_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a workspace by ID.
    
    Args:
        workspace_id: The workspace UUID
        
    Returns:
        Workspace details
    """
    try:
        async with get_client() as client:
            workspace = await client.read_workspace_by_id(UUID(workspace_id))
            
            return [types.TextContent(type="text", text=str(workspace.dict()))]
    except Exception as e:
        # For local Prefect instances, workspace APIs may not be available
        return [types.TextContent(
            type="text",
            text="Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance."
        )]


@mcp.tool
async def get_workspace_by_handle(
    account_handle: str,
    workspace_handle: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a workspace by its handle.
    
    Args:
        account_handle: The account handle
        workspace_handle: The workspace handle
        
    Returns:
        Workspace details
    """
    try:
        async with get_client() as client:
            workspace = await client.read_workspace_by_handle(
                account_handle=account_handle,
                workspace_handle=workspace_handle
            )
            
            return [types.TextContent(type="text", text=str(workspace.dict()))]
    except Exception as e:
        # For local Prefect instances, workspace APIs may not be available
        return [types.TextContent(
            type="text",
            text="Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance."
        )]
