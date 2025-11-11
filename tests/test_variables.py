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
                    # Parse JSON response to verify structure
                    response_data = json.loads(content.text)
                    assert "variables" in response_data
                    assert isinstance(response_data["variables"], list)

async def test_get_variables_with_name_filter():
    """Test getting variables with name filtering."""
    async with prefect_client("get_variables") as (session, tools):
        logger.info("Testing get_variables with name filter...")
        async with asyncio.timeout(10):
            filtered_result = await session.call_tool(
                "get_variables", 
                {"limit": 3, "name": "test"}
            )
            
            # Verify response contains text content
            assert filtered_result.content is not None
            for content in filtered_result.content:
                if content.type == "text":
                    logger.info(f"Filtered variables result: {content.text[:200]}...")
                    response_data = json.loads(content.text)
                    assert "variables" in response_data
                    assert isinstance(response_data["variables"], list)

async def test_get_variables_with_offset():
    """Test getting variables with offset."""
    async with prefect_client("get_variables") as (session, tools):
        logger.info("Testing get_variables with offset...")
        async with asyncio.timeout(10):
            offset_result = await session.call_tool(
                "get_variables", 
                {"limit": 5, "offset": 2}
            )
            
            # Verify response contains text content
            assert offset_result.content is not None
            for content in offset_result.content:
                if content.type == "text":
                    logger.info(f"Offset variables result: {content.text[:200]}...")
                    response_data = json.loads(content.text)
                    assert "variables" in response_data
                    assert isinstance(response_data["variables"], list)

async def test_get_variable():
    """Test getting a specific variable."""
    async with prefect_client("get_variable") as (session, tools):
        # First create a test variable to read
        test_var_name = f"test_get_{uuid.uuid4().hex[:8]}"
        
        # Create the variable first
        await session.call_tool("create_variable", {
            "name": test_var_name,
            "value": {"test": "get_variable_test"},
            "tags": ["test"]
        })
        
        logger.info(f"Testing get_variable with name: {test_var_name}...")
        async with asyncio.timeout(10):
            get_result = await session.call_tool("get_variable", {"name": test_var_name})
            
            # Verify response contains text content
            assert get_result.content is not None
            for content in get_result.content:
                if content.type == "text":
                    logger.info(f"Get variable result: {content.text[:200]}...")
                    response_data = json.loads(content.text)
                    assert "name" in response_data
                    assert response_data["name"] == test_var_name
            
            # Clean up
            await session.call_tool("delete_variable", {"name": test_var_name})

async def test_get_nonexistent_variable():
    """Test getting a variable that doesn't exist."""
    async with prefect_client("get_variable") as (session, tools):
        nonexistent_name = f"nonexistent_{uuid.uuid4().hex[:8]}"
        logger.info(f"Testing get_variable with nonexistent name: {nonexistent_name}...")
        async with asyncio.timeout(10):
            get_result = await session.call_tool("get_variable", {"name": nonexistent_name})
            
            # Verify response contains error message
            assert get_result.content is not None
            for content in get_result.content:
                if content.type == "text":
                    logger.info(f"Get nonexistent variable result: {content.text}")
                    response_data = json.loads(content.text)
                    assert "error" in response_data
                    assert "not found" in response_data["error"].lower()

async def test_create_and_delete_variable():
    """Test creating and deleting a variable."""
    async with prefect_client("create_variable") as (session, tools):
        # Create a test variable with a unique name
        test_var_name = f"test_var_{uuid.uuid4().hex[:8]}"
        logger.info(f"Testing create_variable with name: {test_var_name}...")
        
        async with asyncio.timeout(10):
            create_result = await session.call_tool("create_variable", {
                "name": test_var_name,
                "value": {"test": True, "created_by": "mcp_test"},  # Direct dict, no JSON string
                "tags": ["test", "mcp_test"]
            })
            
            # Verify response contains text content
            assert create_result.content is not None
            variable_created = False
            for content in create_result.content:
                if content.type == "text":
                    logger.info(f"Create variable result: {content.text[:200]}...")
                    response_data = json.loads(content.text)
                    assert "variable" in response_data
                    assert response_data["variable"]["name"] == test_var_name
                    variable_created = True
            
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
                    response_data = json.loads(content.text)
                    assert "message" in response_data
                    assert "deleted" in response_data["message"].lower() or "success" in response_data["message"].lower()
                    variable_deleted = True
            
            assert variable_deleted, "Variable was not deleted successfully"

async def test_create_variable_with_different_value_types():
    """Test creating variables with different value types."""
    async with prefect_client("create_variable") as (session, tools):
        test_cases = [
            {"type": "string", "value": "simple string value"},
            {"type": "number", "value": 42},
            {"type": "float", "value": 3.14159},
            {"type": "boolean", "value": True},
            {"type": "list", "value": [1, 2, 3, "test"]},
            {"type": "dict", "value": {"nested": {"key": "value"}, "array": [1, 2, 3]}},
            {"type": "null", "value": None},
        ]
        
        for test_case in test_cases:
            test_var_name = f"test_{test_case['type']}_{uuid.uuid4().hex[:8]}"
            logger.info(f"Testing {test_case['type']} value with variable: {test_var_name}")
            
            async with asyncio.timeout(10):
                create_result = await session.call_tool("create_variable", {
                    "name": test_var_name,
                    "value": test_case["value"],
                    "tags": ["value_type_test", test_case["type"]]
                })
                
                # Verify creation was successful
                assert create_result.content is not None
                for content in create_result.content:
                    if content.type == "text":
                        response_data = json.loads(content.text)
                        assert "variable" in response_data
                        assert response_data["variable"]["name"] == test_var_name
                
                # Clean up
                await session.call_tool("delete_variable", {"name": test_var_name})

async def test_update_variable():
    """Test updating a variable."""
    async with prefect_client("update_variable") as (session, tools):
        test_var_name = f"test_update_{uuid.uuid4().hex[:8]}"
        
        # First create a variable to update
        await session.call_tool("create_variable", {
            "name": test_var_name,
            "value": {"original": "value"},
            "tags": ["original_tag"]
        })
        
        logger.info(f"Testing update_variable with name: {test_var_name}...")
        async with asyncio.timeout(10):
            update_result = await session.call_tool("update_variable", {
                "name": test_var_name,
                "value": {"updated": "value", "new_field": "test"},
                "tags": ["updated_tag", "test"]
            })
            
            # Verify response contains success message
            assert update_result.content is not None
            for content in update_result.content:
                if content.type == "text":
                    logger.info(f"Update variable result: {content.text[:200]}...")
                    response_data = json.loads(content.text)
                    assert "message" in response_data
                    assert "updated" in response_data["message"].lower()
                    assert "variable" in response_data
                    assert response_data["variable"]["name"] == test_var_name
            
            # Clean up
            await session.call_tool("delete_variable", {"name": test_var_name})

async def test_update_nonexistent_variable():
    """Test updating a variable that doesn't exist."""
    async with prefect_client("update_variable") as (session, tools):
        nonexistent_name = f"nonexistent_update_{uuid.uuid4().hex[:8]}"
        logger.info(f"Testing update_variable with nonexistent name: {nonexistent_name}...")
        async with asyncio.timeout(10):
            update_result = await session.call_tool("update_variable", {
                "name": nonexistent_name,
                "value": "new_value"
            })
            
            # Verify response contains error message
            assert update_result.content is not None
            for content in update_result.content:
                if content.type == "text":
                    logger.info(f"Update nonexistent variable result: {content.text}")
                    response_data = json.loads(content.text)
                    assert "error" in response_data
                    assert "not found" in response_data["error"].lower()

async def test_delete_nonexistent_variable():
    """Test deleting a variable that doesn't exist."""
    async with prefect_client("delete_variable") as (session, tools):
        nonexistent_name = f"nonexistent_delete_{uuid.uuid4().hex[:8]}"
        logger.info(f"Testing delete_variable with nonexistent name: {nonexistent_name}...")
        async with asyncio.timeout(10):
            delete_result = await session.call_tool("delete_variable", {"name": nonexistent_name})
            
            # Verify response contains error message
            assert delete_result.content is not None
            for content in delete_result.content:
                if content.type == "text":
                    logger.info(f"Delete nonexistent variable result: {content.text}")
                    response_data = json.loads(content.text)
                    assert "error" in response_data
                    assert "not found" in response_data["error"].lower()