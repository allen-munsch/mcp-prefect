from enum import Enum


class APIType(str, Enum):
    FLOW = "flow"
    FLOW_RUN = "flow_run"
    DEPLOYMENT = "deployment"
    TASK_RUN = "task_run"
    WORKSPACE = "workspace"
    BLOCK = "block"
    VARIABLE = "variable"
    WORK_QUEUE = "work_queue"

    _MCP_INTERNAL = "_mcp_internal"