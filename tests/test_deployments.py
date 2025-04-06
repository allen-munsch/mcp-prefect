# test_deployments.py
import asyncio
import logging
import pytest

from .conftest import prefect_client

pytestmark = pytest.mark.anyio

logger = logging.getLogger("prefect-mcp-test")


async def test_get_deployments():
    """Test getting a list of deployments."""
    async with prefect_client("get_deployments") as (session, tools):
        logger.info("Testing get_deployments tool...")
        async with asyncio.timeout(10):
            deployments_result = await session.call_tool("get_deployments", {"limit": 5})
        
        # Verify response contains text content
        assert deployments_result.content is not None
        
        for content in deployments_result.content:
            if content.type == "text":
                logger.info(f"Deployments result: {content.text[:200]}...")
                assert "deployments" in content.text

async def test_get_deployments_with_filter():
    """Test getting deployments with filtering."""
    async with prefect_client("get_deployments") as (session, tools):
        logger.info("Testing get_deployments with filter...")
        async with asyncio.timeout(10):
            filtered_result = await session.call_tool(
                "get_deployments", 
                {"limit": 3, "flow_name": "test"}
            )
        
        # Verify response contains text content
        assert filtered_result.content is not None
        
        for content in filtered_result.content:
            if content.type == "text":
                logger.info(f"Filtered deployments result: {content.text[:200]}...")
                assert "deployments" in content.text