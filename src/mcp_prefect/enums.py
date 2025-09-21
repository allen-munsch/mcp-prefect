from enum import Enum


class APIType(str, Enum):
    """Enumeration of available API types in the MCP Prefect server."""
    
    # Core workflow components
    FLOW = "flow"
    FLOW_RUN = "flow_run"
    DEPLOYMENT = "deployment"
    TASK_RUN = "task_run"
    
    # Infrastructure and execution
    WORKSPACE = "workspace"
    WORK_POOL = "work_pool"
    WORK_QUEUE = "work_queue"
    
    # Configuration and storage
    BLOCK = "block"
    VARIABLE = "variable"
    
    # Observability and control
    ARTIFACT = "artifact"
    LOG = "log"
    AUTOMATION = "automation"
    CONCURRENCY_LIMIT = "concurrency_limit"
    
    # Internal
    _MCP_INTERNAL = "_mcp_internal"
