#!/usr/bin/env python3
import asyncio
import json
import logging
import uuid
import pytest
from .conftest import prefect_client

pytestmark = pytest.mark.anyio
logger = logging.getLogger("prefect-mcp-test")

async def test_get_variables():
    """Test getting variables."""
    async with prefect_client("get_variables") as (session, tools):
        logger.info("Testing get_variables tool...")
        async with asyncio.timeout(10):
            variables_result = await session.call_tool("get_variables", {"limit": 5})
            
            # Verify response contains text content
            assert variables_result.content is not None
            for content in variables_result.content:
                if content.type == "text":
                    logger.info(f"Variables result: {content.text[:200]}...")
                    assert "variables" in content.text

async def test_get_variables_with_filter():
    """Test getting variables with filtering."""
    async with prefect_client("get_variables") as (session, tools):
        logger.info("Testing get_variables with filter...")
        async with asyncio.timeout(10):
            filtered_result = await session.call_tool(
                "get_variables", 
                {"limit": 3, "tag": "test"}
            )
            
            # Verify response contains text content
            assert filtered_result.content is not None
            for content in filtered_result.content:
                if content.type == "text":
                    logger.info(f"Filtered variables result: {content.text[:200]}...")
                    assert "variables" in content.text

async def test_create_and_delete_variable():
    """Test creating and deleting a variable."""
    async with prefect_client("create_variable") as (session, tools):
        # Create a test variable with a unique name
        test_var_name = f"test_var_{uuid.uuid4().hex[:8]}"
        logger.info(f"Testing create_variable with name: {test_var_name}...")
        
        async with asyncio.timeout(10):
            create_result = await session.call_tool("create_variable", {
                "name": test_var_name,
                "value": json.dumps({"test": True, "created_by": "mcp_test"}),
                "tags": ["test", "mcp_test"]
            })
            
            # Verify response contains text content
            assert create_result.content is not None
            variable_created = False
            for content in create_result.content:
                if content.type == "text":
                    logger.info(f"Create variable result: {content.text[:200]}...")
                    variable_created = test_var_name in content.text
                    assert variable_created, "Variable was not created successfully"
            
            # Now try to delete it
            logger.info(f"Testing delete_variable for name: {test_var_name}...")
            delete_result = await session.call_tool("delete_variable", {"name": test_var_name})
            
            # Verify response contains text content
            assert delete_result.content is not None
            variable_deleted = False
            for content in delete_result.content:
                if content.type == "text":
                    logger.info(f"Delete variable result: {content.text}")
                    variable_deleted = "deleted" in content.text.lower() or "success" in content.text.lower()
                    assert variable_deleted, "Variable was not deleted successfully"