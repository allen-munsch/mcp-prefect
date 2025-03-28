from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_workspaces, "get_workspaces", "Get all workspaces"),
        (get_current_workspace, "get_current_workspace", "Get current workspace"),
        (get_workspace, "get_workspace", "Get a workspace by ID"),
        (get_workspace_by_handle, "get_workspace_by_handle", "Get a workspace by handle"),
    ]


async def get_workspaces(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of accessible workspaces.
    
    Args:
        limit: Maximum number of workspaces to return
        offset: Number of workspaces to skip
        
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