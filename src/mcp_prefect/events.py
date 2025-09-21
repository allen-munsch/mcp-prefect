
# ============================================================================
# events.py - Events Module
# ============================================================================

@mcp.tool
async def stream_events(
    filter: Optional[Dict[str, Any]] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Stream events from Prefect."""
    try:
        async with get_client() as client:
            response = await client._client.post(
                "/events",
                json={"filter": filter} if filter else {}
            )
            return [types.TextContent(type="text", text=str({"events": response.json()}))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@mcp.tool
async def filter_events(
    filter: Dict[str, Any],
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Filter events."""
    try:
        async with get_client() as client:
            response = await client._client.post(
                "/events/filter",
                json={"filter": filter, "limit": limit, "offset": offset}
            )
            return [types.TextContent(type="text", text=str({"events": response.json()}))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@mcp.tool
async def count_events(
    countable: str,
    filter: Dict[str, Any],
    time_unit: str = "day",
    time_interval: float = 1.0,
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Count events by a specific dimension."""
    try:
        async with get_client() as client:
            response = await client._client.post(
                f"/events/count-by/{countable}",
                json={
                    "filter": filter,
                    "time_unit": time_unit,
                    "time_interval": time_interval
                }
            )
            return [types.TextContent(type="text", text=str(response.json()))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

