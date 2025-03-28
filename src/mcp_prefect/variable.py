from typing import Any, Callable, Dict, List, Optional, Union
import json

import mcp.types as types
from prefect import get_client


def get_all_functions() -> list[tuple[Callable, str, str]]:
    return [
        (get_variables, "get_variables", "Get all variables"),
        (get_variable, "get_variable", "Get a variable by name"),
        (create_variable, "create_variable", "Create a variable"),
        (update_variable, "update_variable", "Update a variable"),
        (delete_variable, "delete_variable", "Delete a variable"),
    ]


async def get_variables(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of variables with optional filtering.
    
    Args:
        limit: Maximum number of variables to return
        offset: Number of variables to skip
        name: Filter by name pattern
        
    Returns:
        A list of variables with their details
    """
    async with get_client() as client:
        # Build filter parameters
        filters = {}
        if name:
            filters["name"] = {"like_": f"%{name}%"}
        
        variables = await client.read_variables(
            limit=limit,
            offset=offset,
            **filters
        )
        
        variables_result = {
            "variables": [variable.dict() for variable in variables]
        }
        
        return [types.TextContent(type="text", text=str(variables_result))]


async def get_variable(
    name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a variable by name.
    
    Args:
        name: The variable name
        
    Returns:
        Variable details
    """
    async with get_client() as client:
        variable = await client.read_variable(name)
        
        return [types.TextContent(type="text", text=str(variable.dict()))]


async def create_variable(
    name: str,
    value: str,
    tags: Optional[List[str]] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Create a variable.
    
    Args:
        name: The variable name
        value: The variable value
        tags: Optional tags
        
    Returns:
        Details of the created variable
    """
    async with get_client() as client:
        # Parse value if it's a valid JSON
        try:
            parsed_value = json.loads(value)
        except json.JSONDecodeError:
            # If it's not valid JSON, use the string as-is
            parsed_value = value
        
        variable = await client.create_variable(
            name=name,
            value=parsed_value,
            tags=tags or [],
        )
        
        return [types.TextContent(type="text", text=str(variable.dict()))]


async def update_variable(
    name: str,
    value: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Update a variable.
    
    Args:
        name: The variable name
        value: New value
        tags: New tags
        
    Returns:
        Details of the updated variable
    """
    async with get_client() as client:
        # Prepare update data
        update_data = {}
        if value is not None:
            # Parse value if it's a valid JSON
            try:
                parsed_value = json.loads(value)
            except json.JSONDecodeError:
                # If it's not valid JSON, use the string as-is
                parsed_value = value
                
            update_data["value"] = parsed_value
        if tags is not None:
            update_data["tags"] = tags
        
        updated_variable = await client.update_variable(
            name=name,
            **update_data
        )
        
        return [types.TextContent(type="text", text=str(updated_variable.dict()))]


async def delete_variable(
    name: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a variable by name.
    
    Args:
        name: The variable name
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.delete_variable(name)
        
        return [types.TextContent(type="text", text=f"Variable '{name}' deleted successfully.")]