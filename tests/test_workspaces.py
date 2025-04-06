#!/usr/bin/env python3
import asyncio
import logging
import pytest
from .conftest import prefect_client

pytestmark = pytest.mark.anyio
logger = logging.getLogger("prefect-mcp-test")

async def test_get_workspaces():
    """Test getting workspaces (Cloud-only feature)."""
    async with prefect_client("get_workspaces") as (session, tools):
        logger.info("Testing get_workspaces tool (expect message about Cloud-only)...")
        async with asyncio.timeout(10):
            workspaces_result = await session.call_tool("get_workspaces")
            
            # Verify response contains text content
            assert workspaces_result.content is not None
            for content in workspaces_result.content:
                if content.type == "text":
                    logger.info(f"Workspaces response: {content.text}")
                    # Cloud-only feature - response might indicate it's not available
                    assert content.text

async def test_get_workspaces_with_filter():
    """Test getting workspaces with filtering (Cloud-only feature)."""
    async with prefect_client("get_workspaces") as (session, tools):
        logger.info("Testing get_workspaces with filter (expect message about Cloud-only)...")
        async with asyncio.timeout(10):
            filtered_result = await session.call_tool(
                "get_workspaces", 
                {"name": "test"}
            )
            
            # Verify response contains text content
            assert filtered_result.content is not None
            for content in filtered_result.content:
                if content.type == "text":
                    logger.info(f"Filtered workspaces response: {content.text}")
                    # Cloud-only feature - response might indicate it's not available
                    assert content.text