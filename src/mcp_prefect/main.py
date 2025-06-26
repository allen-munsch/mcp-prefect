import click
import logging

from .enums import APIType
from .server import mcp

log = logging.getLogger(__name__)
info = log.info


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
    # Import modules to register their decorated tools
    if APIType.FLOW.value in apis:
        from . import flow
    if APIType.FLOW_RUN.value in apis:
        from . import flow_run
    if APIType.DEPLOYMENT.value in apis:
        from . import deployment
    if APIType.TASK_RUN.value in apis:
        from . import task_run
    if APIType.WORKSPACE.value in apis:
        from . import workspace
    if APIType.BLOCK.value in apis:
        from . import block
    if APIType.VARIABLE.value in apis:
        from . import variable
    if APIType.WORK_QUEUE.value in apis:
        from . import work_queue
    if APIType._MCP_INTERNAL.value in apis:
        from . import health_check

    # Configure transport and run
    info(f'Starting with transport: {transport}')
    if transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
