from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import mcp.types as types
from prefect import get_client

from .server import mcp


@mcp.tool
async def get_block_types(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    slug: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a list of block types with optional filtering.
    
    Args:
        limit: Maximum number of block types to return
        offset: Number of block types to skip
        slug: Filter by slug pattern
        
    Returns:
        A list of block types with their details
    """
    async with get_client() as client:
        # Build filter parameters
        filters = {}
        if slug:
            filters["slug"] = {"like_": f"%{slug}%"}
        
        block_types = await client.read_block_types(
            # 
            # limit=limit,
            # offset=offset,
            # **filters
        )
        
        block_types_result = {
            "block_types": [block_type.model_dump() for block_type in block_types]
        }
        
        return [types.TextContent(type="text", text=str(block_types_result))]


@mcp.tool
async def get_block_type(
    slug: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a block type by slug.
    
    Args:
        slug: The block type slug
        
    Returns:
        Block type details
    """
    async with get_client() as client:
        block_type = await client.read_block_type_by_slug(slug)
        
        return [types.TextContent(type="text", text=str(block_type.model_dump()))]


@mcp.tool
async def get_block_documents(
    block_type_slug: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    name: Optional[str] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get block documents by block type.
    
    Args:
        block_type_slug: The block type slug
        limit: Maximum number of block documents to return
        offset: Number of block documents to skip
        name: Filter by name pattern
        
    Returns:
        A list of block documents with their details
    """
    async with get_client() as client:
        # Build filter parameters
        filters = {}
        if block_type_slug:
            filters["block_type_slug"] = {"eq_": block_type_slug}
        if name:
            filters["name"] = {"like_": f"%{name}%"}
        
        block_documents = await client.read_block_documents(
            limit=limit,
            offset=offset,
            **filters
        )
        
        block_documents_result = {
            "block_documents": [block_doc.model_dump() for block_doc in block_documents]
        }
        
        return [types.TextContent(type="text", text=str(block_documents_result))]


@mcp.tool
async def get_block_document(
    block_document_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Get a block document by ID.
    
    Args:
        block_document_id: The block document UUID
        
    Returns:
        Block document details
    """
    async with get_client() as client:
        block_document = await client.read_block_document(UUID(block_document_id))
        
        return [types.TextContent(type="text", text=str(block_document.model_dump()))]


@mcp.tool
async def delete_block_document(
    block_document_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """
    Delete a block document by ID.
    
    Args:
        block_document_id: The block document UUID
        
    Returns:
        Confirmation message
    """
    async with get_client() as client:
        await client.delete_block_document(UUID(block_document_id))
        
        return [types.TextContent(type="text", text=f"Block document '{block_document_id}' deleted successfully.")]
