#!/usr/bin/env python3
import asyncio
import logging
import uuid
import json
import pytest
from .conftest import prefect_client

pytestmark = pytest.mark.anyio
logger = logging.getLogger("prefect-mcp-test")

async def test_get_work_queues():
    """Test getting work queues."""
    async with prefect_client("get_work_queues") as (session, tools):
        logger.info("Testing get_work_queues tool...")
        async with asyncio.timeout(10):
            work_queues_result = await session.call_tool("get_work_queues", {"limit": 5})
            
            # Verify response contains text content
            assert work_queues_result.content is not None
            for content in work_queues_result.content:
                if content.type == "text":
                    logger.info(f"Work queues result: {content.text[:200]}...")
                    assert "work_queues" in content.text

async def test_get_work_queues_with_filter():
    """Test getting work queues with filtering."""
    async with prefect_client("get_work_queues") as (session, tools):
        logger.info("Testing get_work_queues with filter...")
        async with asyncio.timeout(10):
            filtered_result = await session.call_tool(
                "get_work_queues", 
                {"limit": 3, "queue_name": "test"}
            )
            
            # Verify response contains text content
            assert filtered_result.content is not None
            for content in filtered_result.content:
                if content.type == "text":
                    logger.info(f"Filtered work queues result: {content.text[:200]}...")
                    assert "work_queues" in content.text

async def test_create_and_delete_work_queue():
    """Test creating and deleting a work queue."""
    async with prefect_client("create_work_queue") as (session, tools):
        # Create a test work queue with a unique name
        test_queue_name = f"test_queue_{uuid.uuid4().hex[:8]}"
        logger.info(f"Testing create_work_queue with name: {test_queue_name}...")
        
        async with asyncio.timeout(10):
            create_result = await session.call_tool("create_work_queue", {
                "name": test_queue_name,
                "description": "Test work queue created by MCP test"
            })
            
            # Verify response contains text content
            assert create_result.content is not None
            work_queue_id = None
            for content in create_result.content:
                if content.type == "text":
                    logger.info(f"Create work queue result: {content.text[:200]}...")
                    try:
                        parsed = json.loads(content.text.replace("'", '"'))
                        if parsed.get("id"):
                            work_queue_id = parsed["id"]
                    except (json.JSONDecodeError, KeyError):
                        pass
                    
                    assert work_queue_id, "Work queue ID not found in response"
            
            # Now try to delete it
            logger.info(f"Testing delete_work_queue for ID: {work_queue_id}...")
            delete_result = await session.call_tool("delete_work_queue", {"work_queue_id": work_queue_id})
            
            # Verify response contains text content
            assert delete_result.content is not None
            queue_deleted = False
            for content in delete_result.content:
                if content.type == "text":
                    logger.info(f"Delete work queue result: {content.text}")
                    queue_deleted = "deleted" in content.text.lower() or "success" in content.text.lower()
                    assert queue_deleted, "Work queue was not deleted successfully"