# ============================================================================
# block_schemas.py - Block Schemas Module
# ============================================================================

@mcp.tool
async def get_block_schemas(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Get block schemas."""
    try:
        async with get_client() as client:
            response = await client._client.post(
                "/block_schemas/filter",
                json={"limit": limit, "offset": offset}
            )
            return [types.TextContent(type="text", text=str({"block_schemas": response.json()}))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@mcp.tool
async def get_block_schema(
    schema_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Get a block schema by ID."""
    try:
        async with get_client() as client:
            response = await client._client.get(f"/block_schemas/{schema_id}")
            return [types.TextContent(type="text", text=str(response.json()))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@mcp.tool
async def get_block_schema_by_checksum(
    checksum: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Get a block schema by checksum."""
    try:
        async with get_client() as client:
            response = await client._client.get(f"/block_schemas/checksum/{checksum}")
            return [types.TextContent(type="text", text=str(response.json()))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


# ============================================================================
# flow_run_states.py - Flow Run States Module
# ============================================================================

@mcp.tool
async def get_flow_run_state(
    state_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Get a flow run state by ID."""
    try:
        async with get_client() as client:
            response = await client._client.get(f"/flow_run_states/{state_id}")
            return [types.TextContent(type="text", text=str(response.json()))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@mcp.tool
async def get_flow_run_states(
    flow_run_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Get all states for a flow run."""
    try:
        async with get_client() as client:
            response = await client._client.get(f"/flow_run_states/?flow_run_id={flow_run_id}")
            return [types.TextContent(type="text", text=str({"states": response.json()}))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


