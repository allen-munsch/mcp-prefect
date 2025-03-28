# Prefect MCP Server

A Model Context Protocol (MCP) server implementation for [Prefect](https://www.prefect.io/), allowing AI assistants to interact with Prefect through natural language.

## Features

This MCP server provides access to the following Prefect APIs:

- **Flow Management**: List, get, and delete flows
- **Flow Run Management**: Create, monitor, and control flow runs
- **Deployment Management**: Manage deployments and their schedules
- **Task Run Management**: Monitor and control task runs
- **Work Queue Management**: Create and manage work queues
- **Block Management**: Access block types and documents
- **Variable Management**: Create and manage variables
- **Workspace Management**: Get information about workspaces


## Configuration

Set the following environment variables:

```bash
export PREFECT_API_URL="http://localhost:4200/api"  # URL of your Prefect API
export PREFECT_API_KEY="your_api_key"               # Your Prefect API key (if using Prefect Cloud)
```

## Usage

Run the MCP server, and prefect:

```
docker compose up
```

## Example Input

Once connected, an AI assistant can help users interact with Prefect using natural language. Examples:

- "Show me all my flows"
- "List all failed flow runs from yesterday"
- "Trigger the 'data-processing' deployment"
- "Pause the schedule for the 'daily-reporting' deployment"
- "What's the status of my last ETL flow run?"

## Development

Several of the endpoints have yet to be implemented

### Adding New Functions

To add a new function to an existing API:

1. Add the function to the appropriate module in `src/mcp_prefect`
2. Add the function to the `get_all_functions()` list in the module

To add a new API type:

1. Add the new type to `APIType` in `enums.py`
2. Create a new module in `src/prefect/`
3. Update `main.py` to include the new API type

