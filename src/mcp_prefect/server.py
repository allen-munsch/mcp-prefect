from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastmcp import FastMCP
from . import __version__
# Create the FastMCP server
mcp = FastMCP(f"MCP Prefect {__version__}")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> Response:
    return JSONResponse({"status": "ok"})

# Run the server when executed directly
if __name__ == "__main__":
    from .main import main
    main()
