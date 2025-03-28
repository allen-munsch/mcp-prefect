from fastmcp import FastMCP

from mcp_prefect.enums import APIType
from mcp_prefect.block import get_all_functions as get_block_functions
from mcp_prefect.deployment import get_all_functions as get_deployment_functions
from mcp_prefect.flow import get_all_functions as get_flow_functions
from mcp_prefect.flow_run import get_all_functions as get_flow_run_functions
from mcp_prefect.task_run import get_all_functions as get_task_run_functions
from mcp_prefect.variable import get_all_functions as get_variable_functions
from mcp_prefect.work_queue import get_all_functions as get_work_queue_functions
from mcp_prefect.workspace import get_all_functions as get_workspace_functions

# Create the FastMCP server
mcp = FastMCP("Prefect MCP", 
              dependencies=[
                  "prefect>=3.2.15",
                  "uvicorn>=0.34.0"
              ])

# Register all tools
def register_tools():
    api_types = {
        APIType.FLOW: get_flow_functions,
        APIType.FLOW_RUN: get_flow_run_functions,
        APIType.DEPLOYMENT: get_deployment_functions,
        APIType.TASK_RUN: get_task_run_functions,
        APIType.WORKSPACE: get_workspace_functions,
        APIType.BLOCK: get_block_functions,
        APIType.VARIABLE: get_variable_functions,
        APIType.WORK_QUEUE: get_work_queue_functions,
    }
    
    for api_type, get_function in api_types.items():
        print(f"api_type: {api_type} get_function: {get_function}")
        try:
            functions = get_function()
        except NotImplementedError:
            continue

        for fn, name, description in functions:
            mcp.add_tool(fn, name=name, description=description)

# Run the server when executed directly
if __name__ == "__main__":
    from .main import main
    main()