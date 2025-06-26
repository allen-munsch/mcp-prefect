from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("Prefect MCP", 
              host='0.0.0.0',
              dependencies=[
                  "prefect>=3.2.15",
                  "uvicorn>=0.34.0"
              ])

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> Response:
    return JSONResponse({"status": "ok"})

# Run the server when executed directly
if __name__ == "__main__":
    from .main import main
    main()
