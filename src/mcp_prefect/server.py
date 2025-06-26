from fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("Prefect MCP", 
              dependencies=[
                  "prefect>=3.2.15",
                  "uvicorn>=0.34.0"
              ])

# Run the server when executed directly
if __name__ == "__main__":
    from .main import main
    main()
