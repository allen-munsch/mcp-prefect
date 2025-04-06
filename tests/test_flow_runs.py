#!/usr/bin/env python3
import asyncio
import logging
import json
import pytest
from .conftest import prefect_client

pytestmark = pytest.mark.anyio
logger = logging.getLogger("prefect-mcp-test")

async def test_get_flow_runs():
    """Test getting a list of flow runs."""
    async with prefect_client("get_flow_runs") as (session, tools):
        logger.info("Testing get_flow_runs tool...")
        async with asyncio.timeout(10):
            flow_runs_result = await session.call_tool("get_flow_runs", {"limit": 5})
            
            # Verify response contains text content
            assert flow_runs_result.content is not None
            for content in flow_runs_result.content:
                if content.type == "text":
                    logger.info(f"Flow runs result: {content.text[:200]}...")
                    assert "flow_runs" in content.text

async def test_get_flow_runs_with_filter():
    """Test getting flow runs with filtering."""
    async with prefect_client("get_flow_runs") as (session, tools):
        logger.info("Testing get_flow_runs with filter...")
        async with asyncio.timeout(10):
            filtered_result = await session.call_tool(
                "get_flow_runs", 
                {"limit": 3, "flow_name": "test"}
            )
            
            # Verify response contains text content
            assert filtered_result.content is not None
            for content in filtered_result.content:
                if content.type == "text":
                    logger.info(f"Filtered flow runs result: {content.text[:200]}...")
                    assert "flow_runs" in content.text

async def test_get_flow_run_by_id():
    """Test getting a specific flow run by ID."""
    async with prefect_client("get_flow_runs") as (session, tools):
        logger.info("Testing get_flow_run tool...")
        async with asyncio.timeout(10):
            # Get a list of flow runs first to get a valid ID
            flow_runs_result = await session.call_tool("get_flow_runs", {"limit": 1})
            
            flow_run_id = None
            # Extract a flow run ID if possible
            for content in flow_runs_result.content:
                if content.type == "text":
                    try:
                        parsed = json.loads(content.text.replace("'", '"'))
                        if parsed.get("flow_runs") and len(parsed["flow_runs"]) > 0:
                            flow_run_id = parsed["flow_runs"][0].get("id")
                    except (json.JSONDecodeError, KeyError):
                        pass
            
            # Skip test if no flow run ID is found
            if not flow_run_id:
                pytest.skip("No flow runs available to test get_flow_run")
            
            logger.info(f"Testing get_flow_run with ID: {flow_run_id}...")
            flow_run_result = await session.call_tool("get_flow_run", {"flow_run_id": flow_run_id})
            
            # Verify response contains text content
            assert flow_run_result.content is not None
            for content in flow_run_result.content:
                if content.type == "text":
                    logger.info(f"Flow run details result: {content.text[:200]}...")
                    # Verify that the response contains the ID we requested
                    assert flow_run_id in content.text