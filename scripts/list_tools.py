#!/usr/bin/env python3
"""MCP client using stdio transport - NO HTTP HEADERS ISSUES"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def list_tools_stdio():
    # Set environment variables for Prefect
    os.environ['PREFECT_API_URL'] = 'http://prefect-server:4200/api'
    os.environ['PREFECT_API_KEY'] = ''
    
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_prefect.main", "--transport", "stdio"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                init_result = await session.initialize()
                print("✅ Initialized successfully")
                print(f"Server: {init_result.serverInfo.name} {init_result.serverInfo.version}")
                
                # List available tools
                print("\n🔄 Listing tools...")
                tools_result = await session.list_tools()
                
                print(f"\n🎯 FOUND {len(tools_result.tools)} TOOLS:")
                print("=" * 80)
                
                # Show first 20 tools with categories
                categories = {}
                for tool in tools_result.tools:
                    if 'flow' in tool.name:
                        category = 'Flow'
                    elif 'deployment' in tool.name:
                        category = 'Deployment'
                    elif 'task' in tool.name:
                        category = 'Task'
                    elif 'work' in tool.name:
                        category = 'Work'
                    elif 'block' in tool.name:
                        category = 'Block'
                    elif 'variable' in tool.name:
                        category = 'Variable'
                    elif 'artifact' in tool.name:
                        category = 'Artifact'
                    elif 'log' in tool.name:
                        category = 'Log'
                    elif 'automation' in tool.name:
                        category = 'Automation'
                    elif 'concurrency' in tool.name:
                        category = 'Concurrency'
                    else:
                        category = 'Other'
                    
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(tool)
                
                # Print summary by category
                for category, tools in sorted(categories.items()):
                    print(f"\n📂 {category.upper()} ({len(tools)} tools)")
                    for tool in sorted(tools, key=lambda x: x.name)[:5]:  # Show first 5 per category
                        print(f"  🔧 {tool.name}")
                    if len(tools) > 5:
                        print(f"  ... and {len(tools) - 5} more")
                
                print(f"\n📊 TOTAL: {len(tools_result.tools)} tools across {len(categories)} categories")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("  - Make sure Prefect server is running at http://prefect-server:4200/api")
        print("  - Check if the MCP server starts without errors")
        print("  - Try running with: PREFECT_API_URL=http://prefect-server:4200/api python -m mcp_prefect.main --transport stdio")

if __name__ == "__main__":
    asyncio.run(list_tools_stdio())