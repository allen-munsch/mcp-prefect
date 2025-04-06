#!/usr/bin/env python3
import json
import logging
import re
from typing import Any, Dict, Optional

import pytest

logger = logging.getLogger("prefect-mcp-test")


def extract_id_from_response(response_text: str, key: str = "id"):
    """
    Extract an ID from a response text using regex pattern.
    
    Args:
        response_text: The text containing the ID
        key: The key associated with the ID (default: "id")
        
    Returns:
        The extracted ID or None if not found
    """
    try:
        # Extract the UUID using regex pattern
        uuid_match = re.search(rf"'{key}': UUID\('([0-9a-f-]+)'\)", response_text)
        if uuid_match:
            return uuid_match.group(1)
        
        # Try another pattern (regular string ID)
        id_match = re.search(rf"'{key}': '([^']+)'", response_text)
        if id_match:
            return id_match.group(1)
            
        return None
    except Exception as e:
        logger.error(f"Error extracting ID: {e}")
        return None
