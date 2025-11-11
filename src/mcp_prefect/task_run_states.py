# ============================================================================
# task_run_states.py - Task Run States Module
# ============================================================================

@mcp.tool
async def get_task_run_state(
    state_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Get a task run state by ID."""
    try:
        async with get_client() as client:
            response = await client._client.get(f"/task_run_states/{state_id}")
            return [types.TextContent(type="text", text=str(response.json()))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@mcp.tool
async def get_task_run_states(
    task_run_id: str,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Get all states for a task run."""
    try:
        async with get_client() as client:
            response = await client._client.get(f"/task_run_states/?task_run_id={task_run_id}")
            return [types.TextContent(type="text", text=str({"states": response.json()}))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]