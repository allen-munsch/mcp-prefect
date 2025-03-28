#!/usr/bin/env python3
import asyncio
import json
import logging
import os
import sys
from functools import partial
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

import anyio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream

# This matches the imports in your code snippets
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prefect-mcp-test")


async def message_handler(
    message: Any,
) -> None:
    """Handle incoming messages from the server."""
    if isinstance(message, Exception):
        logger.error(f"Error: {message}")
        return
    
    logger.info(f"Received message type: {type(message).__name__}")


async def test_prefect_mcp():
    """Test connecting to the Prefect MCP server and calling tools."""
    # Get the server URL from environment or use default
    server_url = os.environ.get("MCP_URL", "http://localhost:8000")
    
    # Ensure URL points to the SSE endpoint
    if not server_url.endswith("/sse"):
        server_url = server_url.rstrip("/") + "/sse"
    
    logger.info(f"Connecting to Prefect MCP server at {server_url}")
    
    try:
        # Connect to the server using sse_client from your code
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
                
                # Map tools by name for easy lookup
                tool_map = {tool.name: tool for tool in tools_result.tools}
                
                # Print available tools
                for tool in tools_result.tools:
                    logger.info(f"Tool: {tool.name} - {tool.description}")

                # Test categories for better organization
                await test_health(session, tool_map)
                await test_flows(session, tool_map)
                await test_deployments(session, tool_map)
                await test_flow_runs(session, tool_map)
                await test_task_runs(session, tool_map)
                await test_workspaces(session, tool_map)
                await test_blocks(session, tool_map)
                await test_variables(session, tool_map)
                await test_work_queues(session, tool_map)
                
                logger.info("All tests completed successfully")
                
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise


async def test_health(session: ClientSession, tool_map: Dict[str, Any]):
    """Test health check endpoint."""
    if "get_health" in tool_map:
        try:
            logger.info("Testing get_health tool...")
            health_result = await session.call_tool("get_health", {})
            for content in health_result.content:
                if content.type == "text":
                    logger.info(f"Health check result: {content.text}")
        except Exception as e:
            logger.error(f"Error calling get_health: {e}")


async def test_flows(session: ClientSession, tool_map: Dict[str, Any]):
    """Test flow-related endpoints."""
    if "get_flows" in tool_map:
        try:
            logger.info("Testing get_flows tool...")
            flows_result = await session.call_tool("get_flows", {"limit": 5})
            for content in flows_result.content:
                if content.type == "text":
                    logger.info(f"Flows result: {content.text[:200]}...")
            
            # Try with filter
            logger.info("Testing get_flows with filter...")
            filtered_flows = await session.call_tool("get_flows", {"limit": 3, "flow_name": "test"})
            for content in filtered_flows.content:
                if content.type == "text":
                    logger.info(f"Filtered flows result: {content.text[:200]}...")
        except Exception as e:
            logger.error(f"Error calling get_flows: {e}")

    # Test get_flow if available
    if "get_flow" in tool_map:
        try:
            # Get a list of flows first to get a valid ID
            flows_result = await session.call_tool("get_flows", {"limit": 1})
            flow_id = None
            
            # Extract a flow ID if possible
            for content in flows_result.content:
                if content.type == "text":
                    try:
                        flows_data = eval(content.text)
                        if flows_data["flows"]:
                            flow_id = flows_data["flows"][0]["id"]
                    except:
                        pass
            
            if flow_id:
                logger.info(f"Testing get_flow with ID: {flow_id}...")
                flow_result = await session.call_tool("get_flow", {"flow_id": flow_id})
                for content in flow_result.content:
                    if content.type == "text":
                        logger.info(f"Flow details result: {content.text[:200]}...")
            else:
                logger.info("Skipping get_flow test - no flows available")
        except Exception as e:
            logger.error(f"Error calling get_flow: {e}")


async def test_deployments(session: ClientSession, tool_map: Dict[str, Any]):
    """Test deployment-related endpoints."""
    if "get_deployments" in tool_map:
        try:
            logger.info("Testing get_deployments tool...")
            deployments_result = await session.call_tool("get_deployments", {"limit": 5})
            for content in deployments_result.content:
                if content.type == "text":
                    logger.info(f"Deployments result: {content.text[:200]}...")
            
            # Try with filter
            logger.info("Testing get_deployments with filter...")
            filtered_deployments = await session.call_tool("get_deployments", {"limit": 3, "flow_name": "test"})
            for content in filtered_deployments.content:
                if content.type == "text":
                    logger.info(f"Filtered deployments result: {content.text[:200]}...")
        except Exception as e:
            logger.error(f"Error calling get_deployments: {e}")

    # Test get_deployment if available
    if "get_deployment" in tool_map:
        try:
            # Get a list of deployments first to get a valid ID
            deployments_result = await session.call_tool("get_deployments", {"limit": 1})
            deployment_id = None
            
            # Extract a deployment ID if possible
            for content in deployments_result.content:
                if content.type == "text":
                    try:
                        deployments_data = eval(content.text)
                        if deployments_data["deployments"]:
                            deployment_id = deployments_data["deployments"][0]["id"]
                    except:
                        pass
            
            if deployment_id:
                logger.info(f"Testing get_deployment with ID: {deployment_id}...")
                deployment_result = await session.call_tool("get_deployment", {"deployment_id": deployment_id})
                for content in deployment_result.content:
                    if content.type == "text":
                        logger.info(f"Deployment details result: {content.text[:200]}...")
            else:
                logger.info("Skipping get_deployment test - no deployments available")
        except Exception as e:
            logger.error(f"Error calling get_deployment: {e}")


async def test_flow_runs(session: ClientSession, tool_map: Dict[str, Any]):
    """Test flow run-related endpoints."""
    if "get_flow_runs" in tool_map:
        try:
            logger.info("Testing get_flow_runs tool...")
            flow_runs_result = await session.call_tool("get_flow_runs", {"limit": 5})
            for content in flow_runs_result.content:
                if content.type == "text":
                    logger.info(f"Flow runs result: {content.text[:200]}...")
        except Exception as e:
            logger.error(f"Error calling get_flow_runs: {e}")

    # Test get_flow_run if available and we have flow runs
    if "get_flow_run" in tool_map:
        try:
            # Get a list of flow runs first to get a valid ID
            flow_runs_result = await session.call_tool("get_flow_runs", {"limit": 1})
            flow_run_id = None
            
            # Extract a flow run ID if possible
            for content in flow_runs_result.content:
                if content.type == "text":
                    try:
                        flow_runs_data = eval(content.text)
                        if flow_runs_data["flow_runs"]:
                            flow_run_id = flow_runs_data["flow_runs"][0]["id"]
                    except:
                        pass
            
            if flow_run_id:
                logger.info(f"Testing get_flow_run with ID: {flow_run_id}...")
                flow_run_result = await session.call_tool("get_flow_run", {"flow_run_id": flow_run_id})
                for content in flow_run_result.content:
                    if content.type == "text":
                        logger.info(f"Flow run details result: {content.text[:200]}...")
            else:
                logger.info("Skipping get_flow_run test - no flow runs available")
        except Exception as e:
            logger.error(f"Error calling get_flow_run: {e}")


async def test_task_runs(session: ClientSession, tool_map: Dict[str, Any]):
    """Test task run-related endpoints."""
    if "get_task_runs" in tool_map:
        try:
            logger.info("Testing get_task_runs tool...")
            task_runs_result = await session.call_tool("get_task_runs", {"limit": 5})
            for content in task_runs_result.content:
                if content.type == "text":
                    logger.info(f"Task runs result: {content.text[:200]}...")
        except Exception as e:
            logger.error(f"Error calling get_task_runs: {e}")


async def test_workspaces(session: ClientSession, tool_map: Dict[str, Any]):
    """Test workspace-related endpoints."""
    if "get_workspaces" in tool_map:
        try:
            logger.info("Testing get_workspaces tool (expect message about Cloud-only)...")
            workspaces_result = await session.call_tool("get_workspaces")
            for content in workspaces_result.content:
                if content.type == "text":
                    logger.info(f"Workspaces response: {content.text}")
        except Exception as e:
            logger.error(f"Error calling get_workspaces: {e}")


async def test_blocks(session: ClientSession, tool_map: Dict[str, Any]):
    """Test block-related endpoints."""
    if "get_block_types" in tool_map:
        try:
            logger.info("Testing get_block_types tool...")
            block_types_result = await session.call_tool("get_block_types", {"limit": 5})
            for content in block_types_result.content:
                if content.type == "text":
                    logger.info(f"Block types result: {content.text[:200]}...")
        except Exception as e:
            logger.error(f"Error calling get_block_types: {e}")


async def test_variables(session: ClientSession, tool_map: Dict[str, Any]):
    """Test variable-related endpoints."""
    if "get_variables" in tool_map:
        try:
            logger.info("Testing get_variables tool...")
            variables_result = await session.call_tool("get_variables", {"limit": 5})
            for content in variables_result.content:
                if content.type == "text":
                    logger.info(f"Variables result: {content.text[:200]}...")
        except Exception as e:
            logger.error(f"Error calling get_variables: {e}")
            
    # Test create_variable and delete_variable if available
    if "create_variable" in tool_map and "delete_variable" in tool_map:
        try:
            # Create a test variable with a unique name
            test_var_name = f"test_var_{uuid4().hex[:8]}"
            logger.info(f"Testing create_variable with name: {test_var_name}...")
            
            create_result = await session.call_tool("create_variable", {
                "name": test_var_name,
                "value": json.dumps({"test": True, "created_by": "mcp_test"}),
                "tags": ["test", "mcp_test"]
            })
            
            for content in create_result.content:
                if content.type == "text":
                    logger.info(f"Create variable result: {content.text[:200]}...")
            
            # Now try to delete it
            logger.info(f"Testing delete_variable for name: {test_var_name}...")
            delete_result = await session.call_tool("delete_variable", {"name": test_var_name})
            
            for content in delete_result.content:
                if content.type == "text":
                    logger.info(f"Delete variable result: {content.text}")
        except Exception as e:
            logger.error(f"Error testing variable creation/deletion: {e}")


async def test_work_queues(session: ClientSession, tool_map: Dict[str, Any]):
    """Test work queue-related endpoints."""
    if "get_work_queues" in tool_map:
        try:
            logger.info("Testing get_work_queues tool...")
            work_queues_result = await session.call_tool("get_work_queues", {"limit": 5})
            for content in work_queues_result.content:
                if content.type == "text":
                    logger.info(f"Work queues result: {content.text[:200]}...")
        except Exception as e:
            logger.error(f"Error calling get_work_queues: {e}")
            
    # Test create_work_queue and delete_work_queue if available
    if "create_work_queue" in tool_map and "delete_work_queue" in tool_map:
        try:
            # Create a test work queue with a unique name
            test_queue_name = f"test_queue_{uuid4().hex[:8]}"
            logger.info(f"Testing create_work_queue with name: {test_queue_name}...")
            
            create_result = await session.call_tool("create_work_queue", {
                "name": test_queue_name,
                "description": "Test work queue created by MCP test"
            })
            
            work_queue_id = None
            for content in create_result.content:
                if content.type == "text":
                    logger.info(f"Create work queue result: {content.text[:200]}...")
                    try:
                        queue_data = eval(content.text)
                        work_queue_id = queue_data["id"]
                    except:
                        pass
            
            if work_queue_id:
                # Now try to delete it
                logger.info(f"Testing delete_work_queue for ID: {work_queue_id}...")
                delete_result = await session.call_tool("delete_work_queue", {"work_queue_id": work_queue_id})
                
                for content in delete_result.content:
                    if content.type == "text":
                        logger.info(f"Delete work queue result: {content.text}")
            else:
                logger.info("Skipping delete_work_queue test - couldn't get work queue ID")
        except Exception as e:
            logger.error(f"Error testing work queue creation/deletion: {e}")


if __name__ == "__main__":
    # Run with asyncio backend
    anyio.run(test_prefect_mcp, backend="asyncio")