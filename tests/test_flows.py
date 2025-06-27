#!/usr/bin/env python3
import asyncio
import json
import logging
import uuid
import pytest
from .conftest import prefect_client

pytestmark = pytest.mark.anyio
logger = logging.getLogger("prefect-mcp-test")


async def wait_for_flow_run(session, flow_run_id, max_attempts=10, delay=1):
    """
    Poll for flow run details, waiting for it to be in a retrievable state.
    
    :param session: The MCP client session
    :param flow_run_id: ID of the flow run to retrieve
    :param max_attempts: Maximum number of polling attempts
    :param delay: Delay between attempts in seconds
    :return: Flow run details or None if not found
    """
    for attempt in range(max_attempts):
        try:
            flow_run_result = await session.call_tool("get_flow_run", {"flow_run_id": flow_run_id})
            
            # Check the response content
            for content in flow_run_result.content:
                if content.type == "text":
                    # Try to parse the response
                    try:
                        parsed = json.loads(content.text.replace("'", '"'))
                        # Add more sophisticated state checking if needed
                        if parsed and parsed.get('id') == flow_run_id:
                            return parsed
                    except (json.JSONDecodeError, KeyError):
                        pass
            
            # If we didn't return, wait and continue
            await asyncio.sleep(delay)
        
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)
    
    return None

async def test_get_flow_run_by_id():
    """Test getting flow runs from existing flows and deployments."""
    async with prefect_client(["get_flow_runs", "get_flow_run"]) as (session, tools):
        logger.info("Testing get_flow_runs and get_flow_run...")
        
        async with asyncio.timeout(30):
            # First, get existing flow runs
            flow_runs_result = await session.call_tool("get_flow_runs", {"limit": 5})
            
            # Verify response contains text content
            assert flow_runs_result.content is not None
            flow_run_id = None
            
            for content in flow_runs_result.content:
                if content.type == "text":
                    logger.info(f"Flow runs result: {content.text[:200]}...")
                    assert "flow_runs" in content.text
                    
                    # Try to extract a flow run ID from the response
                    from .utils import extract_id_from_response
                    flow_run_id = extract_id_from_response(content.text, "id")
                    if flow_run_id:
                        break
            
            if flow_run_id:
                # Test getting a specific flow run
                logger.info(f"Testing get_flow_run for ID: {flow_run_id}...")
                flow_run_result = await session.call_tool("get_flow_run", {"flow_run_id": flow_run_id})
                
                # Verify response contains text content
                assert flow_run_result.content is not None
                for content in flow_run_result.content:
                    if content.type == "text":
                        logger.info(f"Flow run result: {content.text[:200]}...")
                        assert flow_run_id in content.text
            else:
                logger.info("No flow runs available to test get_flow_run with")

            # Test filtered flow runs (without flow_name since it's not supported)
            async with asyncio.timeout(10):
                filtered_result = await session.call_tool(
                    "get_flow_runs", 
                    {"limit": 3}
                )
                
                # Verify response contains text content
                assert filtered_result.content is not None
                for content in filtered_result.content:
                    if content.type == "text":
                        logger.info(f"Filtered flow runs result: {content.text[:200]}...")
                        assert "flow_runs" in content.text
