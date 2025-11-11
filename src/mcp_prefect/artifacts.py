"""Artifacts module for MCP Prefect."""

from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client

from .server import mcp


@mcp.tool
async def get_artifacts(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    flow_run_id: Optional[str] = None,
    task_run_id: Optional[str] = None,
    artifact_type: Optional[str] = None,
    key: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of artifacts with optional filtering.
    
    Args:
        limit: Maximum number of artifacts to return
        offset: Number of artifacts to skip
        flow_run_id: Filter by flow run ID
        task_run_id: Filter by task run ID
        artifact_type: Filter by artifact type
        key: Filter by artifact key
        
    Returns:
        A list of artifacts with their details
    """
    try:
        async with get_client() as client:
            # Build filter parameters
            filter_dict = {}
            if flow_run_id:
                filter_dict["flow_run_id"] = {"any_": [UUID(flow_run_id)]}
            if task_run_id:
                filter_dict["task_run_id"] = {"any_": [UUID(task_run_id)]}
            if artifact_type:
                filter_dict["type"] = {"any_": [artifact_type]}
            if key:
                filter_dict["key"] = {"like_": f"%{key}%"}
            
            response = await client._client.post(
                "/artifacts/filter",
                json={
                    "artifacts": filter_dict if filter_dict else None,
                    "limit": limit,
                    "offset": offset,
                    "sort": "CREATED_DESC"
                }
            )
            
            artifacts = response.json()
            
            return [types.TextContent(type="text", text=str({"artifacts": artifacts}))]
    except Exception as e:
        error_message = f"Error fetching artifacts: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def get_artifact(
    artifact_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get details of a specific artifact by ID.
    
    Args:
        artifact_id: The artifact UUID
        
    Returns:
        Artifact details
    """
    try:
        async with get_client() as client:
            response = await client._client.get(
                f"/artifacts/{artifact_id}"
            )
            
            artifact = response.json()
            
            return [types.TextContent(type="text", text=str(artifact))]
    except Exception as e:
        error_message = f"Error fetching artifact: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def create_artifact(
    key: str,
    data: Any,
    artifact_type: Optional[str] = "result",
    description: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    flow_run_id: Optional[str] = None,
    task_run_id: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create an artifact.
    
    Args:
        key: A unique reference key for this artifact
        data: The data to store in the artifact
        artifact_type: The type of artifact (e.g., 'result', 'table', 'markdown')
        description: A markdown-enabled description
        metadata: Key-value pairs of metadata (strings only)
        flow_run_id: Associate with a flow run
        task_run_id: Associate with a task run
        
    Returns:
        Details of the created artifact
    """
    try:
        async with get_client() as client:
            artifact_data = {
                "key": key,
                "type": artifact_type,
                "data": data,
            }
            
            if description:
                artifact_data["description"] = description
            if metadata:
                artifact_data["metadata_"] = metadata
            if flow_run_id:
                artifact_data["flow_run_id"] = UUID(flow_run_id)
            if task_run_id:
                artifact_data["task_run_id"] = UUID(task_run_id)
            
            response = await client._client.post(
                "/artifacts/",
                json=artifact_data
            )
            
            created_artifact = response.json()
            
            return [types.TextContent(type="text", text=str(created_artifact))]
    except Exception as e:
        error_message = f"Error creating artifact: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def update_artifact(
    artifact_id: str,
    data: Optional[Any] = None,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update an artifact.
    
    Args:
        artifact_id: The artifact UUID
        data: New data for the artifact
        description: New description
        metadata: New metadata
        
    Returns:
        Details of the updated artifact
    """
    try:
        async with get_client() as client:
            update_data = {}
            if data is not None:
                update_data["data"] = data
            if description is not None:
                update_data["description"] = description
            if metadata is not None:
                update_data["metadata_"] = metadata
            
            response = await client._client.patch(
                f"/artifacts/{artifact_id}",
                json=update_data
            )
            
            updated_artifact = response.json()
            
            return [types.TextContent(type="text", text=str(updated_artifact))]
    except Exception as e:
        error_message = f"Error updating artifact: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def delete_artifact(
    artifact_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete an artifact by ID.
    
    Args:
        artifact_id: The artifact UUID
        
    Returns:
        Confirmation message
    """
    try:
        async with get_client() as client:
            await client._client.delete(
                f"/artifacts/{artifact_id}"
            )
            
            return [types.TextContent(type="text", text=f"Artifact '{artifact_id}' deleted successfully.")]
    except Exception as e:
        error_message = f"Error deleting artifact: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def get_latest_artifacts(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    flow_run_id: Optional[str] = None,
    task_run_id: Optional[str] = None,
    artifact_type: Optional[str] = None,
    key: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get the latest artifacts by key.
    
    Args:
        limit: Maximum number of artifacts to return
        offset: Number of artifacts to skip
        flow_run_id: Filter by flow run ID
        task_run_id: Filter by task run ID
        artifact_type: Filter by artifact type
        key: Filter by artifact key
        
    Returns:
        A list of the latest artifacts
    """
    try:
        async with get_client() as client:
            # Build filter parameters
            filter_dict = {}
            if flow_run_id:
                filter_dict["flow_run_id"] = {"any_": [UUID(flow_run_id)]}
            if task_run_id:
                filter_dict["task_run_id"] = {"any_": [UUID(task_run_id)]}
            if artifact_type:
                filter_dict["type"] = {"any_": [artifact_type]}
            if key:
                filter_dict["key"] = {"like_": f"%{key}%"}
            
            response = await client._client.post(
                "/artifacts/latest/filter",
                json={
                    "artifacts": filter_dict if filter_dict else None,
                    "limit": limit,
                    "offset": offset,
                    "sort": "UPDATED_DESC"
                }
            )
            
            artifacts = response.json()
            
            return [types.TextContent(type="text", text=str({"latest_artifacts": artifacts}))]
    except Exception as e:
        error_message = f"Error fetching latest artifacts: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]