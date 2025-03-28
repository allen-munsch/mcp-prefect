import click
import logging

from .block import get_all_functions as get_block_functions
from .deployment import get_all_functions as get_deployment_functions
from .flow import get_all_functions as get_flow_functions
from .flow_run import get_all_functions as get_flow_run_functions
from .task_run import get_all_functions as get_task_run_functions
from .variable import get_all_functions as get_variable_functions
from .work_queue import get_all_functions as get_work_queue_functions
from .workspace import get_all_functions as get_workspace_functions
from .health_check import get_all_functions as get_healthcheck_functions
from .enums import APIType
from .server import mcp

log = logging.getLogger(__name__)
info = log.info

APITYPE_TO_FUNCTIONS = {
    APIType.FLOW: get_flow_functions,
    APIType.FLOW_RUN: get_flow_run_functions,
    APIType.DEPLOYMENT: get_deployment_functions,
    APIType.TASK_RUN: get_task_run_functions,
    APIType.WORKSPACE: get_workspace_functions,
    APIType.BLOCK: get_block_functions,
    APIType.VARIABLE: get_variable_functions,
    APIType.WORK_QUEUE: get_work_queue_functions,

    APIType._MCP_INTERNAL: get_healthcheck_functions,
}


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
@click.option(
    "--apis",
    type=click.Choice([api.value for api in APIType]),
    default=[api.value for api in APIType],
    multiple=True,
    help="APIs to run, default is all",
)
def main(transport: str, apis: list[str]) -> None:
    # Register tools based on selected APIs
    for api in apis:
        get_function = APITYPE_TO_FUNCTIONS[APIType(api)]
        try:
            functions = get_function()
        except NotImplementedError:
            continue

        for fn, name, description in functions:
            print(f"api_type: {api} get_function: {get_function} fn: {fn} name: {name} description: {description}")
            mcp.add_tool(fn, name=name, description=description)

    # Configure transport and run
    info(f'Starting with transport: {transport}')
    if transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()