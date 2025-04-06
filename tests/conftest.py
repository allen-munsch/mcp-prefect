#!/usr/bin/env python3
from contextlib import asynccontextmanager
from datetime import datetime
import logging
import os
import time
from typing import Any, List
import uuid
import pytest

# Prefect imports
from prefect import flow, task
from prefect.client.orchestration import PrefectClient, get_client
from prefect.server.schemas.core import Flow
from prefect.server.schemas.actions import DeploymentCreate
from prefect.flows import FlowRun

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prefect-mcp-test")

# Apply anyio marker to all test modules
pytest.anyio_backend = "asyncio"

def get_server_url():
    """Get the server URL from environment or use default."""
    url = os.environ.get("MCP_URL", "http://localhost:8000")
    if not url.endswith("/sse"):
        url = url.rstrip("/") + "/sse"
    return url

async def message_handler(
    message: Any,
) -> None:
    """Handle incoming messages from the server."""
    if isinstance(message, Exception):
        logger.error(f"Error: {message}")
        return
    logger.info(f"\nReceived message type: {type(message).__name__}\n")

async def create_and_run_flow(
    client: PrefectClient,
    flow: Flow,
    flow_name: str = None,
    flow_tags: List[str] = None,
    parameters: dict = None,
    max_wait_seconds: int = 60,
    poll_interval: float = 1.0
) -> FlowRun:
    """
    Create and run a Prefect flow using the Prefect client, with polling for completion.
    
    Args:
        client (PrefectClient): Prefect client instance
        flow_name (str, optional): Name of the flow.
        flow_tags (List[str], optional): Tags to associate with the flow
        parameters (dict, optional): Parameters to pass to the flow
        max_wait_seconds (int, optional): Maximum time to wait for flow run completion
        poll_interval (float, optional): Time between polling attempts
    
    Returns:
        FlowRun: The completed flow run
    """
    from prefect.client.schemas.actions import FlowCreate
    from prefect.client.schemas.objects import Flow as FlowModel
    from prefect.client.schemas.filters import FlowRunFilter
    from prefect.client.schemas.sorting import FlowRunSort
    import time
    import asyncio
    
    # Create flow via client
    flow_create_result = await client.create_flow(flow=flow)
    
    # Create a Flow object with a version
    # flow = FlowModel(
    #     id=flow_create_result, 
    #     name=flow_create.name, 
    #     version='0.1.0',
    #     tags=flow_tags or []
    # )
    
    # Create deployment
    deployment_create_result = await client.create_deployment(
        name=f"{flow.name}-deployment",
        flow_id=flow_create_result,
        infrastructure_document_id=None,
        tags=flow_tags or [],
        work_queue_name="default"
    )

    # Create a flow run
    flow_run = await client.create_flow_run(
        flow=flow,
        parameters=parameters or {},
        tags=flow_tags or []
    )
    
    # Poll for flow run completion
    start_time = time.time()
    while time.time() - start_time < max_wait_seconds:
        # Fetch the latest flow run state
        flow_run_filter = FlowRunFilter(id={'eq': flow_run.id})
        flow_runs = await client.read_flow_runs(
            flow_run_filter=flow_run_filter,
            sort=FlowRunSort.START_TIME_DESC,
            limit=1
        )
        
        if not flow_runs:
            raise ValueError(f"Flow run {flow_run.id} not found")
        
        current_flow_run = flow_runs[0]
        
        # Check if the flow run is in a terminal state
        if current_flow_run.state.is_final():
            return current_flow_run
        
        # Wait before next poll
        await asyncio.sleep(poll_interval)
    
    # Timeout occurred
    raise TimeoutError(f"Flow run {flow_run.id} did not complete within {max_wait_seconds} seconds")


# @pytest.fixture(scope="session", autouse=True)
# async def seed_test_data():
#     """
#     Seed test data once per test session.
#     This fixture runs automatically before any tests.
#     """
#     logger.info("Seeding test data...")
    
#     async with get_client() as client:
#         # Define test flows for seeding
#         @flow
#         def simple_test_flow(x: int = 1) -> int:
#             """A simple test flow for demonstration."""
#             return x * 2
        
#         @flow
#         def another_test_flow(message: str = "Hello") -> str:
#             """Another test flow for demonstration."""
#             return message.upper()
        
#         # Create and run test flows
#         try:
#             await create_and_run_flow(
#                 client,
#                 simple_test_flow, 
#                 flow_name="test-multiplication-flow", 
#                 flow_tags=["test", "example"],
#                 parameters={"x": 5}
#             )
            
#             await create_and_run_flow(
#                 client, 
#                 another_test_flow, 
#                 flow_name="test-message-flow", 
#                 flow_tags=["test", "example"],
#                 parameters={"message": "test message"}
#             )
            
#             logger.info("Test data seeding completed successfully")
#         except Exception as e:
#             logger.error(f"Error seeding test data: {e}")
#             raise

@asynccontextmanager
async def prefect_client(required_tools: List[str] | str):
    """Create a Prefect client session for testing."""
    from mcp.client.session import ClientSession
    from mcp.client.sse import sse_client
    
    server_url = get_server_url()
    if isinstance(required_tools, str):
        required_tools = [required_tools]
    
    async with sse_client(server_url) as (read_stream, write_stream):
        # Create a ClientSession with your message handler
        async with ClientSession(
            read_stream,
            write_stream,
            message_handler=message_handler
        ) as session:
            # Initialize the connection
            logger.info("Initializing MCP session...")
            init_result = await session.initialize()
            server_info = init_result.serverInfo
            logger.info(f"Connected to {server_info.name} v{server_info.version}")
            logger.info(f"Protocol version: {init_result.protocolVersion}")
            logger.info(f"Server capabilities: {init_result.capabilities}")
            
            # List available tools
            logger.info("Listing available tools...")
            tools_result = await session.list_tools()
            tools = [tool.name for tool in tools_result.tools]
            
            if not all(tool_name in tools for tool_name in required_tools):
                pytest.skip(f"One of the Tools: '{required_tools}' not available in {tools}")
            
            yield session, tools