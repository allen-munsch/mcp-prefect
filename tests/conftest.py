#!/usr/bin/env python3
import os
import logging
from contextlib import asynccontextmanager
from typing import List
import pytest
from fastmcp import Client
from prefect import flow
from prefect.client.orchestration import get_client, PrefectClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prefect-mcp-test")

# Apply anyio marker to all test modules
pytest.anyio_backend = "asyncio"


def get_server_url() -> str:
    """Get the MCP server URL from environment or default to localhost."""
    return os.environ.get("MCP_URL", "http://localhost:8000/mcp").rstrip("/")


async def message_handler(message):
    """Optional: handle messages from the server (not needed for fastmcp.Client)."""
    logger.info(f"Received: {message}")


@asynccontextmanager
async def prefect_client(required_tools: List[str] | str):
    """
    Async context manager that connects to the FastMCP server and ensures required tools exist.
    """
    if isinstance(required_tools, str):
        required_tools = [required_tools]

    server_url = get_server_url()
    client = Client(server_url)

    async with client:
        logger.info(f"Connected to MCP server at {server_url}")

        # Fetch available tools from the MCP server
        tools = await client.list_tools()
        available_tool_names = [tool.name for tool in tools]

        logger.debug(f"Available MCP tools: {available_tool_names}")

        # Skip if any required tools are missing
        if not all(tool in available_tool_names for tool in required_tools):
            pytest.skip(f"Required tools {required_tools} not available")

        # Yield both for tests to use
        yield client, available_tool_names
