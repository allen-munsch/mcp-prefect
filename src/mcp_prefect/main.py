"""Main entry point for MCP Prefect server."""

import click
import logging

from .enums import APIType
from .server import mcp
from . import __version__

log = logging.getLogger(__name__)
info = log.info



@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http"]),
    default="stdio",
    help="Transport type for MCP communication",
)
@click.option(
    "--apis",
    type=click.Choice([api.value for api in APIType]),
    default=[api.value for api in APIType],
    multiple=True,
    help="APIs to enable (default is all)",
)
def main(transport: str, apis: list[str]) -> None:
    """
    Start the MCP Prefect server with selected APIs.
    
    Args:
        transport: Communication transport type (stdio or sse)
        apis: List of API modules to enable
    """
    # Import modules to register their decorated tools
    if APIType.FLOW.value in apis:
        info("Loading Flow API...")
        from . import flow
    
    if APIType.FLOW_RUN.value in apis:
        info("Loading Flow Run API...")
        from . import flow_run
    
    if APIType.DEPLOYMENT.value in apis:
        info("Loading Deployment API...")
        from . import deployment
    
    if APIType.TASK_RUN.value in apis:
        info("Loading Task Run API...")
        from . import task_run
    
    if APIType.WORKSPACE.value in apis:
        info("Loading Workspace API...")
        from . import workspace
    
    if APIType.WORK_POOL.value in apis:
        info("Loading Work Pool API...")
        from . import work_pools
    
    if APIType.WORK_QUEUE.value in apis:
        info("Loading Work Queue API...")
        from . import work_queue
    
    if APIType.BLOCK.value in apis:
        info("Loading Block API...")
        from . import block
    
    if APIType.VARIABLE.value in apis:
        info("Loading Variable API...")
        from . import variable
    
    if APIType.ARTIFACT.value in apis:
        info("Loading Artifact API...")
        from . import artifacts
    
    if APIType.LOG.value in apis:
        info("Loading Log API...")
        from . import logs
    
    if APIType.AUTOMATION.value in apis:
        info("Loading Automation API...")
        from . import automations
    
    if APIType.CONCURRENCY_LIMIT.value in apis:
        info("Loading Concurrency Limit API...")
        from . import concurrency_limits
    
    if APIType._MCP_INTERNAL.value in apis:
        info("Loading MCP Internal API...")
        from . import health_check

    # Configure transport and run
    info(f'Starting MCP Prefect {__version__} server with transport: {transport}')
    info(f'Enabled APIs: {", ".join(apis)}')

    host='0.0.0.0'
    if transport == "sse":
        mcp.run(transport="http", host=host)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()