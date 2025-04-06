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
    """Test creating a flow, starting a flow run, and then retrieving it."""
    async with prefect_client("create_flow") as (session, tools):
        # Create a unique flow name
        test_flow_name = f"test_flow_{uuid.uuid4().hex[:8]}"
        logger.info(f"Testing create_flow with name: {test_flow_name}...")
        
        async with asyncio.timeout(30):  # Increased timeout to allow for more operations
            # Create a test flow
            create_flow_result = await session.call_tool("create_flow", {
                "name": test_flow_name,
                "description": "Test flow created by MCP test",
                "flow_code": """
from prefect import flow

@flow
def test_flow():
    return "Hello, Prefect!"
"""
            })
            
            # Extract flow ID
            flow_id = None
            for content in create_flow_result.content:
                if content.type == "text":
                    try:
                        parsed = json.loads(content.text.replace("'", '"'))
                        if parsed.get("id"):
                            flow_id = parsed["id"]
                    except (json.JSONDecodeError, KeyError):
                        pass
                    
                    assert flow_id, "Flow ID not found in response"
            
            # Start a flow run
            logger.info(f"Testing create_flow_run for flow ID: {flow_id}...")
            create_flow_run_result = await session.call_tool("create_flow_run", {
                "flow_id": flow_id
            })
            
            # Extract flow run ID
            flow_run_id = None
            for content in create_flow_run_result.content:
                if content.type == "text":
                    try:
                        parsed = json.loads(content.text.replace("'", '"'))
                        if parsed.get("id"):
                            flow_run_id = parsed["id"]
                    except (json.JSONDecodeError, KeyError):
                        pass
                    
                    assert flow_run_id, "Flow run ID not found in response"
            
            # Wait and poll for the flow run to be retrievable
            logger.info(f"Polling for flow run with ID: {flow_run_id}...")
            retrieved_flow_run = await wait_for_flow_run(session, flow_run_id)
            
            # Verify the flow run was retrieved
            assert retrieved_flow_run is not None, "Could not retrieve flow run"
            
            # Additional verifications
            assert retrieved_flow_run.get('id') == flow_run_id, "Retrieved flow run ID does not match"
            assert 'name' in retrieved_flow_run, "Flow run details incomplete"

            async with asyncio.timeout(10):
                flow_runs_result = await session.call_tool("get_flow_runs", {"limit": 5})
            
            # Verify response contains text content
            assert flow_runs_result.content is not None
            for content in flow_runs_result.content:
                if content.type == "text":
                    logger.info(f"Flow runs result: {content.text[:200]}...")
                    assert "flow_runs" in content.text

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
