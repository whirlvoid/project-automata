from fastmcp import FastMCP

from external.mcp_server.browser_controller import register_tools
from external.mcp_server.browser_manager import BrowserManager


mcp = FastMCP("playwright_server")
mcp = register_tools(mcp)


async def shutdown():
    service = BrowserManager()
    await service.cleanup()


if __name__ == "__main__":
    mcp.run(transport="stdio")
