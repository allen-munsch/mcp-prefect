from typing import Any, List, Optional, Union
import json

import mcp.types as types
from prefect import get_client
from prefect.exceptions import ObjectNotFound

from .server import mcp


@mcp.tool
async def get_variables(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of variables with optional filtering.
    
    Args:
        limit: Maximum number of variables to return
        offset: Number of variables to skip (not supported in current Prefect version)
        name: Filter by name pattern (client-side filtering since API doesn't support it)
        
    Returns:
        A list of variables with their details
    """
    try:
        async with get_client() as client:
            # Get all variables and filter client-side since the API doesn't support filtering
            variables = await client.read_variables(limit=limit)
            
            # Apply client-side filtering for name
            if name:
                variables = [var for var in variables if name.lower() in var.name.lower()]
            
            # Apply offset client-side
            if offset:
                variables = variables[offset:]
            
            variables_result = {
                "variables": [variable.model_dump() for variable in variables]
            }
            
            return [types.TextContent(type="text", text=json.dumps(variables_result, indent=2, default=str))]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


@mcp.tool
async def get_variable(
    name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a variable by name.
    
    Args:
        name: The variable name
        
    Returns:
        Variable details or error message if not found
    """
    try:
        async with get_client() as client:
            variable = await client.read_variable_by_name(name)
            
            if variable is None:
                return [types.TextContent(type="text", text=json.dumps({"error": f"Variable '{name}' not found"}, indent=2))]
            
            return [types.TextContent(type="text", text=json.dumps(variable.model_dump(), indent=2, default=str))]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


@mcp.tool
async def create_variable(
    name: str,
    value: Any,
    tags: Optional[List[str]] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a variable.
    
    Args:
        name: The variable name
        value: The variable value (can be string, dict, list, etc.)
        tags: Optional tags
        
    Returns:
        Details of the created variable or error message
    """
    try:
        async with get_client() as client:
            from prefect.client.schemas.actions import VariableCreate
            
            # Create the proper variable object
            variable_create = VariableCreate(
                name=name,
                value=value,
                tags=tags or []
            )
            
            variable = await client.create_variable(variable=variable_create)
            
            variable_result = {"variable": variable.model_dump()}
            return [types.TextContent(type="text", text=json.dumps(variable_result, indent=2, default=str))]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


@mcp.tool
async def update_variable(
    name: str,
    value: Optional[Any] = None,
    tags: Optional[List[str]] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a variable.
    
    Args:
        name: The variable name
        value: New value (can be any JSON-serializable type)
        tags: New tags
        
    Returns:
        Confirmation message or error
    """
    try:
        async with get_client() as client:
            from prefect.client.schemas.actions import VariableUpdate
            
            # Check if variable exists first
            existing_variable = await client.read_variable_by_name(name)
            if existing_variable is None:
                return [types.TextContent(type="text", text=json.dumps({"error": f"Variable '{name}' not found"}, indent=2))]
            
            # Prepare update data
            update_data = {}
            if value is not None:
                update_data["value"] = value
            if tags is not None:
                update_data["tags"] = tags
            
            # Create update object
            variable_update = VariableUpdate(name=name, **update_data)
            
            await client.update_variable(variable=variable_update)
            
            # Read the updated variable to return its details
            updated_variable = await client.read_variable_by_name(name)
            
            return [types.TextContent(type="text", text=json.dumps({
                "message": f"Variable '{name}' updated successfully",
                "variable": updated_variable.model_dump()
            }, indent=2, default=str))]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


@mcp.tool
async def delete_variable(
    name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a variable by name.
    
    Args:
        name: The variable name
        
    Returns:
        Confirmation message or error
    """
    try:
        async with get_client() as client:
            # Check if variable exists first
            existing_variable = await client.read_variable_by_name(name)
            if existing_variable is None:
                return [types.TextContent(type="text", text=json.dumps({"error": f"Variable '{name}' not found"}, indent=2))]
            
            await client.delete_variable_by_name(name)
            
            return [types.TextContent(type="text", text=json.dumps({
                "message": f"Variable '{name}' deleted successfully"
            }, indent=2))]
    except ObjectNotFound:
        return [types.TextContent(type="text", text=json.dumps({
            "error": f"Variable '{name}' not found"
        }, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]