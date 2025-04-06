```
git clone git@github.com:allen-munsch/mcp-prefect.git
cd mcp-prefect
pyenv install 3.12.9
pip install -e .
docker compose up -d
python ./test_scripts/test_prefect.py 
```

```
INFO:prefect-mcp-test:Connecting to Prefect MCP server at http://localhost:8000/sse
INFO:mcp.client.sse:Connecting to SSE endpoint: http://localhost:8000/sse
INFO:httpx:HTTP Request: GET http://localhost:8000/sse "HTTP/1.1 200 OK"
INFO:mcp.client.sse:Received endpoint URL: http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710
INFO:mcp.client.sse:Starting post writer with endpoint URL: http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710
INFO:prefect-mcp-test:Initializing MCP session...
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
INFO:prefect-mcp-test:Connected to Prefect MCP v1.6.0
INFO:prefect-mcp-test:Protocol version: 2024-11-05
INFO:prefect-mcp-test:Server capabilities: experimental={} logging=None prompts=PromptsCapability(listChanged=False) resources=ResourcesCapability(subscribe=False, listChanged=False) tools=ToolsCapability(listChanged=False)
INFO:prefect-mcp-test:Listing available tools...
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
INFO:prefect-mcp-test:Tool: get_flows - Get all flows
INFO:prefect-mcp-test:Tool: get_flow - Get a flow by ID
INFO:prefect-mcp-test:Tool: delete_flow - Delete a flow by ID
INFO:prefect-mcp-test:Tool: get_flow_runs - Get all flow runs
INFO:prefect-mcp-test:Tool: get_flow_run - Get a flow run by ID
INFO:prefect-mcp-test:Tool: get_flow_runs_by_flow - Get flow runs for a specific flow
INFO:prefect-mcp-test:Tool: restart_flow_run - Restart a flow run
INFO:prefect-mcp-test:Tool: cancel_flow_run - Cancel a flow run
INFO:prefect-mcp-test:Tool: delete_flow_run - Delete a flow run
INFO:prefect-mcp-test:Tool: set_flow_run_state - Set a flow run's state
INFO:prefect-mcp-test:Tool: get_deployments - Get all deployments
INFO:prefect-mcp-test:Tool: get_deployment - Get a deployment by ID
INFO:prefect-mcp-test:Tool: create_flow_run_from_deployment - Create a flow run from a deployment
INFO:prefect-mcp-test:Tool: delete_deployment - Delete a deployment
INFO:prefect-mcp-test:Tool: update_deployment - Update a deployment
INFO:prefect-mcp-test:Tool: get_deployment_schedule - Get a deployment's schedule
INFO:prefect-mcp-test:Tool: set_deployment_schedule - Set a deployment's schedule
INFO:prefect-mcp-test:Tool: pause_deployment_schedule - Pause a deployment's schedule
INFO:prefect-mcp-test:Tool: resume_deployment_schedule - Resume a deployment's schedule
INFO:prefect-mcp-test:Tool: get_task_runs - Get all task runs
INFO:prefect-mcp-test:Tool: get_task_run - Get a task run by ID
INFO:prefect-mcp-test:Tool: get_task_runs_by_flow_run - Get task runs for a specific flow run
INFO:prefect-mcp-test:Tool: set_task_run_state - Set a task run's state
INFO:prefect-mcp-test:Tool: get_workspaces - Get all workspaces
INFO:prefect-mcp-test:Tool: get_current_workspace - Get current workspace
INFO:prefect-mcp-test:Tool: get_workspace - Get a workspace by ID
INFO:prefect-mcp-test:Tool: get_workspace_by_handle - Get a workspace by handle
INFO:prefect-mcp-test:Tool: get_block_types - Get all block types
INFO:prefect-mcp-test:Tool: get_block_type - Get a block type by slug
INFO:prefect-mcp-test:Tool: get_block_documents - Get block documents by block type
INFO:prefect-mcp-test:Tool: get_block_document - Get a block document by ID
INFO:prefect-mcp-test:Tool: delete_block_document - Delete a block document
INFO:prefect-mcp-test:Tool: get_variables - Get all variables
INFO:prefect-mcp-test:Tool: get_variable - Get a variable by name
INFO:prefect-mcp-test:Tool: create_variable - Create a variable
INFO:prefect-mcp-test:Tool: update_variable - Update a variable
INFO:prefect-mcp-test:Tool: delete_variable - Delete a variable
INFO:prefect-mcp-test:Tool: get_work_queues - Get all work queues
INFO:prefect-mcp-test:Tool: get_work_queue - Get a work queue by ID
INFO:prefect-mcp-test:Tool: get_work_queue_by_name - Get a work queue by name
INFO:prefect-mcp-test:Tool: create_work_queue - Create a work queue
INFO:prefect-mcp-test:Tool: update_work_queue - Update a work queue
INFO:prefect-mcp-test:Tool: delete_work_queue - Delete a work queue
INFO:prefect-mcp-test:Tool: pause_work_queue - Pause a work queue
INFO:prefect-mcp-test:Tool: resume_work_queue - Resume a work queue
INFO:prefect-mcp-test:Tool: get_health - Get health status
INFO:prefect-mcp-test:Testing get_health tool...
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
INFO:prefect-mcp-test:Health check result: <Response [200 OK]>
INFO:prefect-mcp-test:Testing get_flows tool...
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
INFO:prefect-mcp-test:Flows result: {'flows': []}...
INFO:prefect-mcp-test:Testing get_flows with filter...
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
INFO:prefect-mcp-test:Filtered flows result: Error fetching flows: FlowAsyncClient.read_flows() got an unexpected keyword argument 'name'...
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
INFO:prefect-mcp-test:Skipping get_flow test - no flows available
INFO:prefect-mcp-test:Testing get_deployments tool...
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
INFO:prefect-mcp-test:Deployments result: {'deployments': []}...
INFO:prefect-mcp-test:Testing get_deployments with filter...
INFO:httpx:HTTP Request: POST http://localhost:8000/messages/?session_id=bfce341df9544e3a91daef4183f24710 "HTTP/1.1 202 Accepted"
...
```