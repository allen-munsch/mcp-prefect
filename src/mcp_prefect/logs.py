"""Logs module for MCP Prefect."""

from datetime import datetime
from typing import List, Optional, Union

import mcp.types as types
from prefect import get_client

from .server import mcp


@mcp.tool
async def get_logs(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    flow_run_id: Optional[str] = None,
    task_run_id: Optional[str] = None,
    level: Optional[int] = None,
    timestamp_after: Optional[str] = None,
    timestamp_before: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get logs with optional filtering.
    
    Args:
        limit: Maximum number of logs to return
        offset: Number of logs to skip
        flow_run_id: Filter by flow run ID
        task_run_id: Filter by task run ID
        level: Filter by log level (10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL)
        timestamp_after: ISO formatted datetime string for logs after this time
        timestamp_before: ISO formatted datetime string for logs before this time
        
    Returns:
        A list of logs with their details
    """
    try:
        async with get_client() as client:
            # Build filter parameters
            filter_dict = {}
            if flow_run_id:
                filter_dict["flow_run_id"] = {"any_": [flow_run_id]}
            if task_run_id:
                filter_dict["task_run_id"] = {"any_": [task_run_id]}
            if level is not None:
                filter_dict["level"] = {"ge_": level}
            if timestamp_after:
                filter_dict["timestamp"] = {"after_": timestamp_after}
            if timestamp_before:
                if "timestamp" in filter_dict:
                    filter_dict["timestamp"]["before_"] = timestamp_before
                else:
                    filter_dict["timestamp"] = {"before_": timestamp_before}
            
            response = await client._client.post(
                "/logs/filter",
                json={
                    "logs": filter_dict if filter_dict else None,
                    "limit": limit,
                    "offset": offset,
                    "sort": "TIMESTAMP_DESC"
                }
            )
            
            logs = response.json()
            
            return [types.TextContent(type="text", text=str({"logs": logs}))]
    except Exception as e:
        error_message = f"Error fetching logs: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def create_log(
    message: str,
    level: int = 20,
    flow_run_id: Optional[str] = None,
    task_run_id: Optional[str] = None,
    name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a log entry.
    
    Args:
        message: The log message
        level: Log level (10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL)
        flow_run_id: Associate with a flow run
        task_run_id: Associate with a task run
        name: Logger name
        
    Returns:
        Confirmation of log creation
    """
    try:
        async with get_client() as client:
            log_data = {
                "name": name or "prefect.mcp",
                "level": level,
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            if flow_run_id:
                log_data["flow_run_id"] = flow_run_id
            if task_run_id:
                log_data["task_run_id"] = task_run_id
            
            response = await client._client.post(
                "/logs/",
                json=[log_data]  # Logs API expects a list
            )
            
            return [types.TextContent(type="text", text="Log created successfully.")]
    except Exception as e:
        error_message = f"Error creating log: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def get_flow_run_logs(
    flow_run_id: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    level: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get logs for a specific flow run.
    
    Args:
        flow_run_id: The flow run UUID
        limit: Maximum number of logs to return
        offset: Number of logs to skip
        level: Minimum log level to return
        
    Returns:
        Logs for the flow run
    """
    try:
        async with get_client() as client:
            filter_dict = {"flow_run_id": {"any_": [flow_run_id]}}
            if level is not None:
                filter_dict["level"] = {"ge_": level}
            
            response = await client._client.post(
                "/logs/filter",
                json={
                    "logs": filter_dict,
                    "limit": limit,
                    "offset": offset,
                    "sort": "TIMESTAMP_ASC"
                }
            )
            
            logs = response.json()
            
            # Format logs for better readability
            formatted_logs = []
            for log in logs:
                formatted_logs.append({
                    "timestamp": log.get("timestamp"),
                    "level": log.get("level"),
                    "message": log.get("message"),
                    "name": log.get("name")
                })
            
            return [types.TextContent(type="text", text=str({"flow_run_logs": formatted_logs}))]
    except Exception as e:
        error_message = f"Error fetching flow run logs: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]


@mcp.tool
async def get_task_run_logs(
    task_run_id: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    level: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get logs for a specific task run.
    
    Args:
        task_run_id: The task run UUID
        limit: Maximum number of logs to return
        offset: Number of logs to skip
        level: Minimum log level to return
        
    Returns:
        Logs for the task run
    """
    try:
        async with get_client() as client:
            filter_dict = {"task_run_id": {"any_": [task_run_id]}}
            if level is not None:
                filter_dict["level"] = {"ge_": level}
            
            response = await client._client.post(
                "/logs/filter",
                json={
                    "logs": filter_dict,
                    "limit": limit,
                    "offset": offset,
                    "sort": "TIMESTAMP_ASC"
                }
            )
            
            logs = response.json()
            
            # Format logs for better readability
            formatted_logs = []
            for log in logs:
                formatted_logs.append({
                    "timestamp": log.get("timestamp"),
                    "level": log.get("level"),
                    "message": log.get("message"),
                    "name": log.get("name")
                })
            
            return [types.TextContent(type="text", text=str({"task_run_logs": formatted_logs}))]
    except Exception as e:
        error_message = f"Error fetching task run logs: {str(e)}"
        return [types.TextContent(type="text", text=error_message)]