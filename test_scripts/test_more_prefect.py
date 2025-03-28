import asyncio
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

import httpx
from mcp.client import Client as MCPClient
from mcp.types import TextContent


async def get_flow_run_status(client, flow_run_id: str):
    """Get the status of a flow run."""
    result = await client.call_tool("get_flow_run", arguments={"flow_run_id": flow_run_id})
    content = result.get("content", [])
    if content:
        text = content[0].get("text", "")
        data = eval(text)
        return data.get("state", {}).get("type", "UNKNOWN")
    return "UNKNOWN"


async def wait_for_flow_run_completion(client, flow_run_id: str, timeout_seconds: int = 300):
    """Wait for a flow run to complete, with timeout."""
    start_time = time.time()
    status = await get_flow_run_status(client, flow_run_id)
    
    print(f"Initial flow run status: {status}")
    
    while status not in ["COMPLETED", "FAILED", "CANCELLED"] and (time.time() - start_time) < timeout_seconds:
        print(f"Waiting for flow run to complete. Current status: {status}")
        await asyncio.sleep(5)
        status = await get_flow_run_status(client, flow_run_id)
    
    if (time.time() - start_time) >= timeout_seconds:
        print(f"Timeout waiting for flow run completion. Last status: {status}")
        return False
    
    print(f"Flow run completed with status: {status}")
    return status == "COMPLETED"


async def run_prefect_workflow():
    """Run a complete Prefect workflow via MCP."""
    print("Starting Prefect MCP workflow example...")
    
    # Configure MCP client to connect to the server
    mcp_url = os.environ.get("MCP_URL", "http://localhost:8000")
    client = MCPClient(url=mcp_url)
    
    try:
        # Initialize connection
        print("Connecting to MCP server...")
        await client.initialize()
        print("Connected successfully!")
        
        # 1. Find a deployment to work with
        print("\nLooking for available deployments...")
        deployments_result = await client.call_tool("get_deployments")
        deployments_content = deployments_result.get("content", [])
        
        if not deployments_content:
            print("No deployments found. Please create a deployment in Prefect first.")
            return
            
        deployments_text = deployments_content[0].get("text", "")
        deployments_data = eval(deployments_text)
        deployments = deployments_data.get('deployments', [])
        
        if not deployments:
            print("No deployments found. Please create a deployment in Prefect first.")
            return
        
        selected_deployment = deployments[0]
        deployment_id = selected_deployment.get('id')
        deployment_name = selected_deployment.get('name')
        print(f"Selected deployment: {deployment_name} (ID: {deployment_id})")
        
        # 2. Create a flow run from the deployment
        print(f"\nCreating a flow run from deployment {deployment_name}...")
        create_result = await client.call_tool(
            "create_flow_run_from_deployment", 
            arguments={
                "deployment_id": str(deployment_id),
                "name": f"MCP Test Flow Run {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "tags": ["mcp-test", "automated"]
            }
        )
        create_content = create_result.get("content", [])
        
        if not create_content:
            print("Failed to create flow run.")
            return
            
        create_text = create_content[0].get("text", "")
        flow_run_data = eval(create_text)
        flow_run_id = flow_run_data.get('id')
        flow_run_url = flow_run_data.get('ui_url')
        
        print(f"Created flow run with ID: {flow_run_id}")
        print(f"Flow run URL: {flow_run_url}")
        
        # 3. Wait for the flow run to complete
        print("\nWaiting for flow run to complete...")
        completed = await wait_for_flow_run_completion(client, str(flow_run_id))
        
        if not completed:
            print("Flow run did not complete successfully within the timeout period.")
            return
        
        # 4. Get task runs for the flow run
        print("\nRetrieving task runs for the completed flow run...")
        task_runs_result = await client.call_tool(
            "get_task_runs_by_flow_run", 
            arguments={"flow_run_id": str(flow_run_id)}
        )
        task_runs_content = task_runs_result.get("content", [])
        
        if not task_runs_content:
            print("No task runs found for this flow run.")
            return
            
        task_runs_text = task_runs_content[0].get("text", "")
        task_runs_data = eval(task_runs_text)
        task_runs = task_runs_data.get('task_runs', [])
        
        print(f"Found {len(task_runs)} task runs for flow run {flow_run_id}")
        
        # 5. Summarize task run statuses
        statuses = {}
        for task_run in task_runs:
            status = task_run.get('state', {}).get('type', 'UNKNOWN')
            if status in statuses:
                statuses[status] += 1
            else:
                statuses[status] = 1
                
        print("\nTask run status summary:")
        for status, count in statuses.items():
            print(f"- {status}: {count} task(s)")
        
        # 6. Get flow run details after completion
        print("\nGetting final flow run details...")
        flow_run_result = await client.call_tool("get_flow_run", arguments={"flow_run_id": str(flow_run_id)})
        flow_run_content = flow_run_result.get("content", [])
        
        if not flow_run_content:
            print("Failed to get flow run details.")
            return
            
        flow_run_text = flow_run_content[0].get("text", "")
        flow_run_data = eval(flow_run_text)
        
        start_time = flow_run_data.get('start_time')
        end_time = flow_run_data.get('end_time')
        
        if start_time and end_time:
            # Convert string times to datetime objects
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            duration = (end_dt - start_dt).total_seconds()
            
            print(f"\nFlow run execution time: {duration:.2f} seconds")
        
        print("\nWorkflow completed successfully!")
        
    except Exception as e:
        print(f"Error during workflow: {e}")
    finally:
        # Cleanup
        await client.close()


if __name__ == "__main__":
    asyncio.run(run_prefect_workflow())