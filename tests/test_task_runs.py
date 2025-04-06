#!/usr/bin/env python3
import asyncio
import logging
import pytest
from .conftest import prefect_client

pytestmark = pytest.mark.anyio
logger = logging.getLogger("prefect-mcp-test")

async def test_get_task_runs():
    """Test getting a list of task runs."""
    async with prefect_client("get_task_runs") as (session, tools):
        logger.info("Testing get_task_runs tool...")
        async with asyncio.timeout(10):
            task_runs_result = await session.call_tool("get_task_runs", {"limit": 5})
            
            # Verify response contains text content
            assert task_runs_result.content is not None
            for content in task_runs_result.content:
                if content.type == "text":
                    logger.info(f"Task runs result: {content.text[:200]}...")
                    assert "task_runs" in content.text

async def test_get_task_runs_with_filter():
    """Test getting task runs with filtering."""
    async with prefect_client("get_task_runs") as (session, tools):
        logger.info("Testing get_task_runs with filter...")
        async with asyncio.timeout(10):
            filtered_result = await session.call_tool(
                "get_task_runs", 
                {"limit": 3, "task_name": "test"}
            )
            
            # Verify response contains text content
            assert filtered_result.content is not None
            for content in filtered_result.content:
                if content.type == "text":
                    logger.info(f"Filtered task runs result: {content.text[:200]}...")
                    assert "task_runs" in content.text