#!/usr/bin/env python3
import logging
import pytest

from .conftest import prefect_client

pytestmark = pytest.mark.anyio

logger = logging.getLogger("prefect-mcp-test")

async def test_get_block_types():
    """Test getting block types."""

    async with prefect_client("get_block_types") as (session, tools):
        logger.info("Testing get_block_types tool...")
        block_types_result = await session.call_tool("get_block_types", {"limit": 5})
        
        # Verify response contains text content
        assert block_types_result.content is not None
        
        for content in block_types_result.content:
            if content.type == "text":
                logger.info(f"Block types result: {content.text[:200]}...")
                assert "block_types" in content.text or "blocks" in content.text