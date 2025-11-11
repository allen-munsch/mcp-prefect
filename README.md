[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/allen-munsch-mcp-prefect-badge.jpg)](https://mseep.ai/app/allen-munsch-mcp-prefect)

# Prefect MCP Server

A Model Context Protocol (MCP) server implementation for [Prefect](https://www.prefect.io/), enabling AI assistants to interact with Prefect through natural language.

> **Note**: The official Prefect MCP server is available [here](https://pypi.org/project/prefect-mcp/). This is a community implementation.

## 🚀 Quick Start

```bash
docker compose up
```

## 📦 Installation

### pip Installation
```bash
pip install mcp-prefect
```

### From Source
```bash
git clone https://github.com/allen-munsch/mcp-prefect
cd mcp-prefect
pip install -e .
```

### Manual Run
```bash
PREFECT_API_URL=http://localhost:4200/api \
PREFECT_API_KEY=your_api_key_here \
MCP_PORT=8000 \
python -m mcp_prefect.main --transport http
```

## 🛠️ Features

```

╭────────────────────────────────────────────────────────────────────────────╮
│                                                                            │
│        _ __ ___  _____           __  __  _____________    ____    ____     │
│       _ __ ___ .'____/___ ______/ /_/  |/  / ____/ __ \  |___ \  / __ \    │
│      _ __ ___ / /_  / __ `/ ___/ __/ /|_/ / /   / /_/ /  ___/ / / / / /    │
│     _ __ ___ / __/ / /_/ (__  ) /_/ /  / / /___/ ____/  /  __/_/ /_/ /     │
│    _ __ ___ /_/    \____/____/\__/_/  /_/\____/_/      /_____(*)____/      │
│                                                                            │
│                                                                            │
│                                FastMCP  2.0                                │
│                                                                            │
│                                                                            │
│                 🖥️  Server name:     MCP Prefect 3.6.1                      │
│                 📦 Transport:       STDIO                                  │
│                                                                            │
│                 🏎️  FastMCP version: 2.12.3                                 │
│                 🤝 MCP SDK version: 1.14.1                                 │
│                                                                            │
│                 📚 Docs:            https://gofastmcp.com                  │
│                 🚀 Deploy:          https://fastmcp.cloud                  │
│                                                                            │
╰────────────────────────────────────────────────────────────────────────────╯


[11/11/25 02:08:06] INFO     Starting MCP server 'MCP Prefect 3.6.1' with transport 'stdio'                                                                                     server.py:1495
✅ Initialized successfully
Server: MCP Prefect 3.6.1 1.14.1

🔄 Listing tools...

🎯 FOUND 64 TOOLS:
================================================================================

📂 ARTIFACT (6 tools)
  🔧 create_artifact
  🔧 delete_artifact
  🔧 get_artifact
  🔧 get_artifacts
  🔧 get_latest_artifacts
  🔧 update_artifact

📂 AUTOMATION (7 tools)
  🔧 create_automation
  🔧 delete_automation
  🔧 get_automation
  🔧 get_automations
  🔧 pause_automation
  🔧 resume_automation
  🔧 update_automation

📂 BLOCK (5 tools)
  🔧 delete_block_document
  🔧 get_block_document
  🔧 get_block_documents
  🔧 get_block_type
  🔧 get_block_types

📂 DEPLOYMENT (8 tools)
  🔧 delete_deployment
  🔧 get_deployment
  🔧 get_deployment_schedule
  🔧 get_deployments
  🔧 pause_deployment_schedule
  🔧 resume_deployment_schedule
  🔧 set_deployment_schedule
  🔧 update_deployment

📂 FLOW (13 tools)
  🔧 cancel_flow_run
  🔧 create_flow_run_from_deployment
  🔧 delete_flow
  🔧 delete_flow_run
  🔧 get_flow
  🔧 get_flow_run
  🔧 get_flow_run_logs
  🔧 get_flow_runs
  🔧 get_flow_runs_by_flow
  🔧 get_flows
  🔧 get_task_runs_by_flow_run
  🔧 restart_flow_run
  🔧 set_flow_run_state

📂 LOG (2 tools)
  🔧 create_log
  🔧 get_logs

📂 OTHER (1 tools)
  🔧 get_health

📂 TASK (4 tools)
  🔧 get_task_run
  🔧 get_task_run_logs
  🔧 get_task_runs
  🔧 set_task_run_state

📂 VARIABLE (5 tools)
  🔧 create_variable
  🔧 delete_variable
  🔧 get_variable
  🔧 get_variables
  🔧 update_variable

📂 WORK (13 tools)
  🔧 create_work_queue
  🔧 delete_work_queue
  🔧 get_current_workspace
  🔧 get_work_queue
  🔧 get_work_queue_by_name
  🔧 get_work_queue_runs
  🔧 get_work_queues
  🔧 get_workspace
  🔧 get_workspace_by_handle
  🔧 get_workspaces
  🔧 pause_work_queue
  🔧 resume_work_queue
  🔧 update_work_queue

📊 TOTAL: 64 tools across 10 categories
```

## 💬 Example Interactions

AI assistants can help you with:

**Flow Management**
- "Show me all my flows and their last run status"
- "Create a new flow run for the 'data-processing' deployment"
- "What's the current status of flow run 'abc-123'?"

**Deployment Control**
- "Pause the schedule for the 'daily-reporting' deployment"
- "Update the 'etl-pipeline' deployment with new parameters"

**Infrastructure Management**
- "List all work pools and their current status"
- "Create a new work queue for high-priority jobs"

**Variable & Configuration**
- "Create a variable called 'api_timeout' with value 300"
- "Show me all variables containing 'config' in their name"

**Monitoring & Debugging**
- "Get the logs for the last failed flow run"
- "Show me all running task runs right now"

## 🤖 Platform Integration

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "prefect": {
      "command": "mcp-prefect",
      "args": ["--transport", "stdio"]
    }
  }
}
```

### Cursor MCP
```json
{
  "mcpServers": {
    "prefect": {
      "command": "mcp-prefect",
      "args": ["--transport", "stdio"]
    }
  }
}
```

### Gemini CLI
```bash
gemini config set mcp-servers.prefect "mcp-prefect --transport stdio"
```

### Windsurf / Claude Code
```json
{
  "mcpServers": {
    "prefect": {
      "command": "mcp-prefect",
      "args": ["--transport", "stdio"],
      "env": {
        "PREFECT_API_URL": "http://localhost:4200/api",
        "PREFECT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Generic MCP Client
```json
{
  "mcpServers": {
    "prefect": {
      "command": "mcp-prefect",
      "args": ["--transport", "stdio"],
      "env": {
        "PREFECT_API_URL": "http://localhost:4200/api",
        "PREFECT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🧪 Development

### Running Tests
```bash
pytest tests/ -v
```

### Building from Source
```bash
git clone https://github.com/allen-munsch/mcp-prefect
cd mcp-prefect
pip install -e .
python -m mcp_prefect
```
